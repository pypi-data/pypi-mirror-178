import os
from plaid2 import AsyncPlaidClient
from plaid2 import PlaidClient
from plaid2.model import *


def main():
    client = PlaidClient.from_env()
    response = client.link_token_create(
        client_name="your client name",
        language="your language",
        country_codes=["your country codes"],
        user=LinkTokenCreateRequestUser(
            name_=UserName(
                family_name="your family name",
                given_name="your given name",
            ),
            date_of_birth="your date of birth",
            client_user_id="your client user id",
            address=UserAddress(
                street="your street",
                city="your city",
                country="your country",
                region="your region",
                street_2="your street 2",
                postal_code="your postal code",
            ),
            phone_number_verified_time="your phone number verified time",
            id_number=UserIdNumber(
                type="your type",
                value="your value",
            ),
            legal_name="your legal name",
            email_address_verified_time="your email address verified time",
            phone_number="your phone number",
            ssn="your ssn",
            email_address="your email address",
        ),
    )
    print(f"{response!r}")


async def async_main():
    client = AsyncPlaidClient.from_env()
    response = await client.link_token_create(
        client_name="your client name",
        language="your language",
        country_codes=["your country codes"],
        user=LinkTokenCreateRequestUser(
            name_=UserName(
                family_name="your family name",
                given_name="your given name",
            ),
            date_of_birth="your date of birth",
            client_user_id="your client user id",
            address=UserAddress(
                street="your street",
                city="your city",
                country="your country",
                region="your region",
                street_2="your street 2",
                postal_code="your postal code",
            ),
            phone_number_verified_time="your phone number verified time",
            id_number=UserIdNumber(
                type="your type",
                value="your value",
            ),
            legal_name="your legal name",
            email_address_verified_time="your email address verified time",
            phone_number="your phone number",
            ssn="your ssn",
            email_address="your email address",
        ),
    )
    print(f"{response!r}")


if __name__ == "__main__":
    if os.environ.get("ASYNC"):
        import asyncio

        asyncio.run(async_main())
    else:
        main()
