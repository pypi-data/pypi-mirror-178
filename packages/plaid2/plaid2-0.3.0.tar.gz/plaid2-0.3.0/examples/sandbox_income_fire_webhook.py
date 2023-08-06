import os
from plaid2 import AsyncPlaidClient
from plaid2 import PlaidClient
from plaid2.model import *

item_id = "your item id"
webhook = "your webhook"
verification_status = "your verification status"


def main():
    client = PlaidClient.from_env()
    response = client.sandbox_income_fire_webhook(item_id, webhook, verification_status)
    print(f"{response!r}")


async def async_main():
    client = AsyncPlaidClient.from_env()
    response = await client.sandbox_income_fire_webhook(item_id, webhook, verification_status)
    print(f"{response!r}")


if __name__ == "__main__":
    if os.environ.get("ASYNC"):
        import asyncio

        asyncio.run(async_main())
    else:
        main()
