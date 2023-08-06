import os
from plaid2 import AsyncPlaidClient
from plaid2 import PlaidClient
from plaid2.model import *

access_token = "your access token"
start_date = "your start date"
end_date = "your end date"


def main():
    client = PlaidClient.from_env()
    response = client.investments_transactions_get(access_token, start_date, end_date)
    print(f"{response!r}")


async def async_main():
    client = AsyncPlaidClient.from_env()
    response = await client.investments_transactions_get(access_token, start_date, end_date)
    print(f"{response!r}")


if __name__ == "__main__":
    if os.environ.get("ASYNC"):
        import asyncio

        asyncio.run(async_main())
    else:
        main()
