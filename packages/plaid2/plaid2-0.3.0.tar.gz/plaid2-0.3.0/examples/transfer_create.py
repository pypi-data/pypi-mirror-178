import os
from plaid2 import AsyncPlaidClient
from plaid2 import PlaidClient
from plaid2.model import *


def main():
    client = PlaidClient.from_env()
    response = client.transfer_create(
        authorization_id="your authorization id",
        type="your type",
        network="your network",
        amount="your amount",
        description="your description",
        ach_class="your ach class",
        user=TransferUserInRequest(
            legal_name="your legal name",
            address=TransferUserAddressInRequest(
                postal_code="your postal code",
                region="your region",
                country="your country",
                street="your street",
                city="your city",
            ),
            email_address="your email address",
            phone_number="your phone number",
        ),
    )
    print(f"{response!r}")


async def async_main():
    client = AsyncPlaidClient.from_env()
    response = await client.transfer_create(
        authorization_id="your authorization id",
        type="your type",
        network="your network",
        amount="your amount",
        description="your description",
        ach_class="your ach class",
        user=TransferUserInRequest(
            legal_name="your legal name",
            address=TransferUserAddressInRequest(
                postal_code="your postal code",
                region="your region",
                country="your country",
                street="your street",
                city="your city",
            ),
            email_address="your email address",
            phone_number="your phone number",
        ),
    )
    print(f"{response!r}")


if __name__ == "__main__":
    if os.environ.get("ASYNC"):
        import asyncio

        asyncio.run(async_main())
    else:
        main()
