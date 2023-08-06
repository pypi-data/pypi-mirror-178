import os
from plaid2 import AsyncPlaidClient
from plaid2 import PlaidClient
from plaid2.model import *

target_account = DepositSwitchTargetAccount(
    account_number="your account number",
    account_subtype="your account subtype",
    routing_number="your routing number",
    account_name="your account name",
)
target_user = DepositSwitchTargetUser(
    phone="your phone",
    family_name="your family name",
    email="your email",
    tax_payer_id="your tax payer id",
    given_name="your given name",
    address=DepositSwitchAddressData(
        city="your city",
        region="your region",
        postal_code="your postal code",
        country="your country",
        street="your street",
    ),
)


def main():
    client = PlaidClient.from_env()
    response = client.deposit_switch_alt_create(target_account, target_user)
    print(f"{response!r}")


async def async_main():
    client = AsyncPlaidClient.from_env()
    response = await client.deposit_switch_alt_create(target_account, target_user)
    print(f"{response!r}")


if __name__ == "__main__":
    if os.environ.get("ASYNC"):
        import asyncio

        asyncio.run(async_main())
    else:
        main()
