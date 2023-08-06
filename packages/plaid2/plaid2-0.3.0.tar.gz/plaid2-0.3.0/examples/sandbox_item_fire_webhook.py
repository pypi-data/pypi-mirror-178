import os
from plaid2 import AsyncPlaidClient
from plaid2 import PlaidClient
from plaid2.model import *

access_token = "your access token"
webhook_code = "your webhook code"


def main():
    client = PlaidClient.from_env()
    response = client.sandbox_item_fire_webhook(access_token, webhook_code)
    print(f"{response!r}")


async def async_main():
    client = AsyncPlaidClient.from_env()
    response = await client.sandbox_item_fire_webhook(access_token, webhook_code)
    print(f"{response!r}")


if __name__ == "__main__":
    if os.environ.get("ASYNC"):
        import asyncio

        asyncio.run(async_main())
    else:
        main()
