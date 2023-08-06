import os
from plaid2 import AsyncPlaidClient
from plaid2 import PlaidClient
from plaid2.model import *


def main():
    client = PlaidClient.from_env()
    response = client.identity_verification_create(
        is_shareable=True,
        template_id="your template id",
        gave_consent=True,
        user=IdentityVerificationRequestUser(
            email_address="your email address",
            phone_number="your phone number",
            client_user_id="your client user id",
            date_of_birth="your date of birth",
            name_=UserName(
                family_name="your family name",
                given_name="your given name",
            ),
            address=UserAddress(
                street="your street",
                city="your city",
                country="your country",
                region="your region",
                street_2="your street 2",
                postal_code="your postal code",
            ),
            id_number=UserIdNumber(
                type="your type",
                value="your value",
            ),
        ),
    )
    print(f"{response!r}")


async def async_main():
    client = AsyncPlaidClient.from_env()
    response = await client.identity_verification_create(
        is_shareable=True,
        template_id="your template id",
        gave_consent=True,
        user=IdentityVerificationRequestUser(
            email_address="your email address",
            phone_number="your phone number",
            client_user_id="your client user id",
            date_of_birth="your date of birth",
            name_=UserName(
                family_name="your family name",
                given_name="your given name",
            ),
            address=UserAddress(
                street="your street",
                city="your city",
                country="your country",
                region="your region",
                street_2="your street 2",
                postal_code="your postal code",
            ),
            id_number=UserIdNumber(
                type="your type",
                value="your value",
            ),
        ),
    )
    print(f"{response!r}")


if __name__ == "__main__":
    if os.environ.get("ASYNC"):
        import asyncio

        asyncio.run(async_main())
    else:
        main()
