import os
from plaid2 import AsyncPlaidClient
from plaid2 import PlaidClient
from plaid2.model import *

deposit_switch_id = "your deposit switch id"


def main():
    client = PlaidClient.from_env()
    response = client.deposit_switch_token_create(deposit_switch_id)
    print(f"{response!r}")


async def async_main():
    client = AsyncPlaidClient.from_env()
    response = await client.deposit_switch_token_create(deposit_switch_id)
    print(f"{response!r}")


if __name__ == "__main__":
    if os.environ.get("ASYNC"):
        import asyncio

        asyncio.run(async_main())
    else:
        main()
