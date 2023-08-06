import os
from plaid2 import AsyncPlaidClient
from plaid2 import PlaidClient
from plaid2.model import *

account_number = "your account number"
routing_number = "your routing number"
account_type = "your account type"


def main():
    client = PlaidClient.from_env()
    response = client.bank_transfer_migrate_account(account_number, routing_number, account_type)
    print(f"{response!r}")


async def async_main():
    client = AsyncPlaidClient.from_env()
    response = await client.bank_transfer_migrate_account(account_number, routing_number, account_type)
    print(f"{response!r}")


if __name__ == "__main__":
    if os.environ.get("ASYNC"):
        import asyncio

        asyncio.run(async_main())
    else:
        main()
