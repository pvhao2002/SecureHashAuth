#!/usr/bin/env python3
"""Đo thời gian hash_password / verify_password — xuất CSV cho báo cáo."""

from __future__ import annotations

import argparse
import csv
import platform
import statistics
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from app.auth.hashing import HashAlgorithm, hash_password, verify_password  # noqa: E402

SAMPLE_PASSWORD = "Secret123!"
DEFAULT_ITERATIONS = 10
RESULTS_DIR = ROOT / "results"


def _bench(fn, iterations: int) -> tuple[float, float, float]:
    times: list[float] = []
    for _ in range(iterations):
        t0 = time.perf_counter()
        fn()
        times.append(time.perf_counter() - t0)
    return (
        statistics.mean(times) * 1000,
        min(times) * 1000,
        max(times) * 1000,
    )


def main() -> None:
    parser = argparse.ArgumentParser(description="Benchmark password hashing")
    parser.add_argument(
        "-n",
        "--iterations",
        type=int,
        default=DEFAULT_ITERATIONS,
        help=f"Số lần lặp mỗi thuật toán (mặc định {DEFAULT_ITERATIONS}; báo cáo có thể dùng 50)",
    )
    args = parser.parse_args()
    iterations = max(1, args.iterations)

    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    rows: list[dict[str, str | float | int]] = []
    env = {
        "python": sys.version.split()[0],
        "platform": platform.platform(),
        "iterations": iterations,
        "sample_password_len": len(SAMPLE_PASSWORD),
        "recorded_at_utc": datetime.now(timezone.utc).isoformat(),
    }

    params = {
        HashAlgorithm.BCRYPT: "rounds=20",
        HashAlgorithm.SCRYPT: "rounds=14, block_size=8, parallelism=1",
        HashAlgorithm.ARGON2: "time_cost=3, memory_cost=65536, parallelism=2, type=ID",
    }

    for algo in (HashAlgorithm.BCRYPT, HashAlgorithm.SCRYPT, HashAlgorithm.ARGON2):
        digest, _ = hash_password(SAMPLE_PASSWORD, algo)
        mean_h, min_h, max_h = _bench(
            lambda a=algo: hash_password(SAMPLE_PASSWORD, a)[0],
            iterations,
        )
        mean_v, min_v, max_v = _bench(
            lambda d=digest: verify_password(SAMPLE_PASSWORD, d),
            iterations,
        )
        rows.append(
            {
                "algorithm": algo.value,
                "params": params[algo],
                "hash_mean_ms": round(mean_h, 3),
                "hash_min_ms": round(min_h, 3),
                "hash_max_ms": round(max_h, 3),
                "verify_mean_ms": round(mean_v, 3),
                "verify_min_ms": round(min_v, 3),
                "verify_max_ms": round(max_v, 3),
            }
        )

    out = RESULTS_DIR / "benchmark_hash.csv"
    fieldnames = list(rows[0].keys())
    with out.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames)
        w.writeheader()
        w.writerows(rows)

    meta = RESULTS_DIR / "benchmark_environment.txt"
    meta.write_text(
        "\n".join(f"{k}={v}" for k, v in env.items()),
        encoding="utf-8",
    )
    print(f"Wrote {out}")
    print(f"Wrote {meta}")
    for r in rows:
        print(
            f"{r['algorithm']}: hash avg {r['hash_mean_ms']} ms, "
            f"verify avg {r['verify_mean_ms']} ms"
        )


if __name__ == "__main__":
    main()
