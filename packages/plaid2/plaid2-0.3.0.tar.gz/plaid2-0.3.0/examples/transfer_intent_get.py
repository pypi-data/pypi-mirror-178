import os
from plaid2 import AsyncPlaidClient
from plaid2 import PlaidClient
from plaid2.model import *

transfer_intent_id = "your transfer intent id"


def main():
    client = PlaidClient.from_env()
    response = client.transfer_intent_get(transfer_intent_id)
    print(f"{response!r}")


async def async_main():
    client = AsyncPlaidClient.from_env()
    response = await client.transfer_intent_get(transfer_intent_id)
    print(f"{response!r}")


if __name__ == "__main__":
    if os.environ.get("ASYNC"):
        import asyncio

        asyncio.run(async_main())
    else:
        main()
