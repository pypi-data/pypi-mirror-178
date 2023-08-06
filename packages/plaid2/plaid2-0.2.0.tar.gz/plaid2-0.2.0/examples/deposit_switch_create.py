import os
from plaid2 import AsyncPlaidClient
from plaid2 import PlaidClient
from plaid2.model import *

target_access_token = "your target access token"
target_account_id = "your target account id"


def main():
    client = PlaidClient.from_env()
    response = client.deposit_switch_create(target_access_token, target_account_id)
    print(f"{response!r}")


async def async_main():
    client = AsyncPlaidClient.from_env()
    response = await client.deposit_switch_create(target_access_token, target_account_id)
    print(f"{response!r}")


if __name__ == "__main__":
    if os.environ.get("ASYNC"):
        import asyncio

        asyncio.run(async_main())
    else:
        main()
