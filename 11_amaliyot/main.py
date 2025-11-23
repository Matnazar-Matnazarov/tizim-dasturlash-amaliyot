"""
10 ta saytga aiohttp orqali parallel so‘rov yuborib, umumiy bajarilish vaqtini o‘lchang va tahlil qiling.
"""


import asyncio
import aiohttp
import time

URLS = [
    "https://www.google.com",
    "https://www.github.com",
    "https://www.python.org",
    "https://www.wikipedia.org",
    "https://www.stackoverflow.com",
    "https://www.reddit.com",
    "https://www.microsoft.com",
    "https://www.apple.com",
    "https://www.nasa.gov",
    "https://www.bbc.com",
]

async def fetch(session, url):
    start = time.perf_counter()
    async with session.get(url) as response:
        await response.text()  
        elapsed = time.perf_counter() - start
        return url, response.status, round(elapsed, 3)

async def main():
    start_time = time.perf_counter()

    async with aiohttp.ClientSession() as session:
        tasks = [fetch(session, url) for url in URLS]
        results = await asyncio.gather(*tasks)

    total_time = time.perf_counter() - start_time

    print(" Natijalar:")
    for url, status, t in results:
        print(f"{url:35} -> {status} ({t}s)")

    print(f"Bajarilish vaqti: {total_time:.3f} s")
if __name__ == "__main__":
    asyncio.run(main())
