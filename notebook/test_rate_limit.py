#!/usr/bin/env python3
"""
test_api_rate_limit.py

Send N concurrent requests to your FastAPI /carparks/{facility_id} endpoint
and report each response’s status code (especially 429).
"""
import os
import asyncio
from collections import Counter

import httpx

# ─── Configuration ─────────────────────────────────────────────────────────────
API_BASE     = os.getenv("API_BASE", "http://localhost:8000/carparks")
FACILITY_ID  = os.getenv("FACILITY_ID", "487")
TOTAL_REQUESTS = int(os.getenv("TOTAL_REQUESTS", "100"))
CONCURRENCY    = int(os.getenv("CONCURRENCY", str(TOTAL_REQUESTS)))

# ─── Worker ────────────────────────────────────────────────────────────────────
semaphore = asyncio.Semaphore(CONCURRENCY)

async def call_endpoint(client: httpx.AsyncClient, idx: int):
    url = f"{API_BASE}/{FACILITY_ID}"
    async with semaphore:
        try:
            resp = await client.get(url, timeout=10.0)
            code = resp.status_code
            if code == 200:
                print(f"[{idx:02d}] ✅ 200 OK")
            elif code == 429:
                print(f"[{idx:02d}] ⚠️ 429 Too Many Requests")
            else:
                print(f"[{idx:02d}] ❌ {code}")
            return code
        except Exception as e:
            print(f"[{idx:02d}] ❌ Exception: {e!r}")
            return None

# ─── Main ───────────────────────────────────────────────────────────────────────
async def main():
    print(f"→ Sending {TOTAL_REQUESTS} concurrent requests to {API_BASE}/{FACILITY_ID}\n")

    async with httpx.AsyncClient() as client:
        tasks = [asyncio.create_task(call_endpoint(client, i)) for i in range(TOTAL_REQUESTS)]
        results = await asyncio.gather(*tasks)

    # Summarize
    print("\nSummary:")
    counts = Counter(results)
    for code, cnt in sorted(counts.items(), key=lambda x: (str(x[0]))):
        label = f"{code}" if code is not None else "Error"
        print(f"  {label:>5}: {cnt}")

    print("\nDone.")

if __name__ == "__main__":
    asyncio.run(main())
