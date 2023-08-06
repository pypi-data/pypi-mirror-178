import os
from plaid2 import AsyncPlaidClient
from plaid2 import PlaidClient
from plaid2.model import *

search_terms = EntityWatchlistSearchTerms(
    email_address="your email address",
    country="your country",
    entity_watchlist_program_id="your entity watchlist program id",
    phone_number="your phone number",
    url="your url",
    document_number="your document number",
    legal_name="your legal name",
)


def main():
    client = PlaidClient.from_env()
    response = client.watchlist_screening_entity_create(search_terms)
    print(f"{response!r}")


async def async_main():
    client = AsyncPlaidClient.from_env()
    response = await client.watchlist_screening_entity_create(search_terms)
    print(f"{response!r}")


if __name__ == "__main__":
    if os.environ.get("ASYNC"):
        import asyncio

        asyncio.run(async_main())
    else:
        main()
