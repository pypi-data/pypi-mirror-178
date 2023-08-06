import os
from plaid2 import AsyncPlaidClient
from plaid2 import PlaidClient
from plaid2.model import *


def main():
    client = PlaidClient.from_env()
    response = client.item_application_scopes_update(
        access_token="your access token",
        application_id="your application id",
        scopes=Scopes(
            product_access=ProductAccess(
                accounts_statements=True,
                accounts_tax_statements=True,
                customers_profiles=True,
                auth=True,
                transactions=True,
                identity=True,
                accounts_details_transactions=True,
                accounts_routing_number=True,
                statements=True,
            ),
            accounts=[
                AccountAccess(
                    unique_id="your unique id",
                    authorized=True,
                    account_product_access=AccountProductAccess(
                        account_data=True,
                        statements=True,
                        tax_documents=True,
                    ),
                )
            ],
            new_accounts=True,
        ),
        context="your context",
    )
    print(f"{response!r}")


async def async_main():
    client = AsyncPlaidClient.from_env()
    response = await client.item_application_scopes_update(
        access_token="your access token",
        application_id="your application id",
        scopes=Scopes(
            product_access=ProductAccess(
                accounts_statements=True,
                accounts_tax_statements=True,
                customers_profiles=True,
                auth=True,
                transactions=True,
                identity=True,
                accounts_details_transactions=True,
                accounts_routing_number=True,
                statements=True,
            ),
            accounts=[
                AccountAccess(
                    unique_id="your unique id",
                    authorized=True,
                    account_product_access=AccountProductAccess(
                        account_data=True,
                        statements=True,
                        tax_documents=True,
                    ),
                )
            ],
            new_accounts=True,
        ),
        context="your context",
    )
    print(f"{response!r}")


if __name__ == "__main__":
    if os.environ.get("ASYNC"):
        import asyncio

        asyncio.run(async_main())
    else:
        main()
