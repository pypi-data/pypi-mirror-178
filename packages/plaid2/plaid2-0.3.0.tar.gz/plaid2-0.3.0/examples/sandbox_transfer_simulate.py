import os
from plaid2 import AsyncPlaidClient
from plaid2 import PlaidClient
from plaid2.model import *

transfer_id = "your transfer id"
event_type = "your event type"


def main():
    client = PlaidClient.from_env()
    response = client.sandbox_transfer_simulate(transfer_id, event_type)
    print(f"{response!r}")


async def async_main():
    client = AsyncPlaidClient.from_env()
    response = await client.sandbox_transfer_simulate(transfer_id, event_type)
    print(f"{response!r}")


if __name__ == "__main__":
    if os.environ.get("ASYNC"):
        import asyncio

        asyncio.run(async_main())
    else:
        main()
