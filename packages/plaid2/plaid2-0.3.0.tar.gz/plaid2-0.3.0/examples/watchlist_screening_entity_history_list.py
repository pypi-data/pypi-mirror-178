import os
from plaid2 import AsyncPlaidClient
from plaid2 import PlaidClient
from plaid2.model import *

entity_watchlist_screening_id = "your entity watchlist screening id"


def main():
    client = PlaidClient.from_env()
    response = client.watchlist_screening_entity_history_list(entity_watchlist_screening_id)
    print(f"{response!r}")


async def async_main():
    client = AsyncPlaidClient.from_env()
    response = await client.watchlist_screening_entity_history_list(entity_watchlist_screening_id)
    print(f"{response!r}")


if __name__ == "__main__":
    if os.environ.get("ASYNC"):
        import asyncio

        asyncio.run(async_main())
    else:
        main()
