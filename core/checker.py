import aiohttp
import asyncio
import logging


from utils.append_file import append_file


class Checker:
    def __init__(self, address: str | None):
        self.address = address
        if not self.address:
            logging.warning(f"The address is not found in wallets.txt")

    async def check_account(self,
                            client: aiohttp.ClientSession) -> None:
        try:
            response: aiohttp.ClientResponse = await client.get(
                url=f"https://api.zknation.io/eligibility",
                params={
                    "id": self.address
                }
            )
            response_text: str = await response.text()
            response_json: dict = await response.json()

            if not response_json.get("allocations"):
                logging.info(f"Address {self.address} is not eligible for zkSync")
                async with asyncio.Lock():
                    await append_file(
                        file_path='result/not_eligible.txt',
                        file_content=f"Is not eligible: {self.address}\n"
                    )
            else:
                amount: int = int(response_json["allocations"][0]["tokenAmount"])
                amount /= 10**18
                logging.info(f"Address {self.address} is eligible for zkSync with {amount} ZK")
                async with asyncio.Lock():
                    await append_file(
                        file_path='result/eligible.txt',
                        file_content=f"Eligible: {self.address} {amount}\n"
                    )
        except Exception as error:
            logging.error(f"Error while checking {self.address} with {error}")


async def check_account(address: str,
                        client: aiohttp.ClientSession) -> None:
    await Checker(address=address).check_account(client=client)
