import aiohttp
import asyncio
import logging


from core.checker import check_account
from fake_useragent import UserAgent
from os.path import exists
from os import mkdir


logging.basicConfig(filename="zksync_checker_logs.log", filemode="a", format="%(asctime)s %(levelname)s %(message)s",
                    level=logging.INFO)


async def main():
    loader = asyncio.Semaphore(threads)

    async with aiohttp.ClientSession(
        connector=aiohttp.TCPConnector(
            verify_ssl=None,
            ssl=False,
            use_dns_cache=False,
            ttl_dns_cache=300,
            limit=None
        ),
        headers={
            'accept': '*/*',
            'accept-language': 'ru,en;q=0.9',
            'content-type': 'application/json',
            'origin': 'https://claim.zknation.io',
            'referer': 'https://claim.zknation.io/',
            'x-api-key': '46001d8f026d4a5bb85b33530120cd38',
            'user-agent': UserAgent().random,
        }
    ) as client:
        tasks: list[asyncio.Task] = [
            asyncio.create_task(
                coro=check_account(client=client, address=address))
            for address in wallets_list
        ]

        await asyncio.gather(*tasks)


if __name__ == '__main__':
    if not exists("result"):
        mkdir("result")

    with open(file=f"wallets.txt",
              mode="r", encoding="utf-8") as file:
        wallets_list: list[str] = [row.rstrip() for row in file]

    logging.info(f"Successfully added {len(wallets_list)} accounts")
    threads = int(input("Threads: "))

    asyncio.run(main())
    print("The work has been Successfully finished!")
    input("Press any button to exit...")
