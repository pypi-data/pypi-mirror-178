import os
from plaid2 import AsyncPlaidClient
from plaid2 import PlaidClient
from plaid2.model import *

confirmed_hits = ["your confirmed hits"]
dismissed_hits = ["your dismissed hits"]
watchlist_screening_id = "your watchlist screening id"


def main():
    client = PlaidClient.from_env()
    response = client.watchlist_screening_individual_review_create(
        confirmed_hits, dismissed_hits, watchlist_screening_id
    )
    print(f"{response!r}")


async def async_main():
    client = AsyncPlaidClient.from_env()
    response = await client.watchlist_screening_individual_review_create(
        confirmed_hits, dismissed_hits, watchlist_screening_id
    )
    print(f"{response!r}")


if __name__ == "__main__":
    if os.environ.get("ASYNC"):
        import asyncio

        asyncio.run(async_main())
    else:
        main()
