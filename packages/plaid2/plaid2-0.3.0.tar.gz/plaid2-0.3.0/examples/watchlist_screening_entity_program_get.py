import os
from plaid2 import AsyncPlaidClient
from plaid2 import PlaidClient
from plaid2.model import *

entity_watchlist_program_id = "your entity watchlist program id"


def main():
    client = PlaidClient.from_env()
    response = client.watchlist_screening_entity_program_get(entity_watchlist_program_id)
    print(f"{response!r}")


async def async_main():
    client = AsyncPlaidClient.from_env()
    response = await client.watchlist_screening_entity_program_get(entity_watchlist_program_id)
    print(f"{response!r}")


if __name__ == "__main__":
    if os.environ.get("ASYNC"):
        import asyncio

        asyncio.run(async_main())
    else:
        main()
