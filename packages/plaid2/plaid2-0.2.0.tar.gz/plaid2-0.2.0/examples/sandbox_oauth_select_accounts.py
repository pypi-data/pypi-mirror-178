import os
from plaid2 import AsyncPlaidClient
from plaid2 import PlaidClient
from plaid2.model import *

oauth_state_id = "your oauth state id"
accounts = ["your accounts"]


def main():
    client = PlaidClient.from_env()
    response = client.sandbox_oauth_select_accounts(oauth_state_id, accounts)
    print(f"{response!r}")


async def async_main():
    client = AsyncPlaidClient.from_env()
    response = await client.sandbox_oauth_select_accounts(oauth_state_id, accounts)
    print(f"{response!r}")


if __name__ == "__main__":
    if os.environ.get("ASYNC"):
        import asyncio

        asyncio.run(async_main())
    else:
        main()
