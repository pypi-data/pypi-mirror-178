import os
from plaid2 import AsyncPlaidClient
from plaid2 import PlaidClient
from plaid2.model import *

access_token = "your access token"
account_id = "your account id"


def main():
    client = PlaidClient.from_env()
    response = client.processor_stripe_bank_account_token_create(access_token, account_id)
    print(f"{response!r}")


async def async_main():
    client = AsyncPlaidClient.from_env()
    response = await client.processor_stripe_bank_account_token_create(access_token, account_id)
    print(f"{response!r}")


if __name__ == "__main__":
    if os.environ.get("ASYNC"):
        import asyncio

        asyncio.run(async_main())
    else:
        main()
