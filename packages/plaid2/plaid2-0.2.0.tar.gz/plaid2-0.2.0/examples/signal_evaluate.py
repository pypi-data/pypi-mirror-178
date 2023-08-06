import os
from plaid2 import AsyncPlaidClient
from plaid2 import PlaidClient
from plaid2.model import *


def main():
    client = PlaidClient.from_env()
    response = client.signal_evaluate(
        access_token="your access token",
        account_id="your account id",
        client_transaction_id="your client transaction id",
        amount=1.0,
    )
    print(f"{response!r}")


async def async_main():
    client = AsyncPlaidClient.from_env()
    response = await client.signal_evaluate(
        access_token="your access token",
        account_id="your account id",
        client_transaction_id="your client transaction id",
        amount=1.0,
    )
    print(f"{response!r}")


if __name__ == "__main__":
    if os.environ.get("ASYNC"):
        import asyncio

        asyncio.run(async_main())
    else:
        main()
