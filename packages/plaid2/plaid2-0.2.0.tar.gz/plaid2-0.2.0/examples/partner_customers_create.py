import os
from plaid2 import AsyncPlaidClient
from plaid2 import PlaidClient
from plaid2.model import *

company_name = "your company name"
is_diligence_attested = True
products = ["your products"]


def main():
    client = PlaidClient.from_env()
    response = client.partner_customers_create(company_name, is_diligence_attested, products)
    print(f"{response!r}")


async def async_main():
    client = AsyncPlaidClient.from_env()
    response = await client.partner_customers_create(company_name, is_diligence_attested, products)
    print(f"{response!r}")


if __name__ == "__main__":
    if os.environ.get("ASYNC"):
        import asyncio

        asyncio.run(async_main())
    else:
        main()
