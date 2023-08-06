import os
from plaid2 import AsyncPlaidClient
from plaid2 import PlaidClient
from plaid2.model import *

count = 1
offset = 1
country_codes = ["your country codes"]


def main():
    client = PlaidClient.from_env()
    response = client.institutions_get(count, offset, country_codes)
    print(f"{response!r}")


async def async_main():
    client = AsyncPlaidClient.from_env()
    response = await client.institutions_get(count, offset, country_codes)
    print(f"{response!r}")


if __name__ == "__main__":
    if os.environ.get("ASYNC"):
        import asyncio

        asyncio.run(async_main())
    else:
        main()
