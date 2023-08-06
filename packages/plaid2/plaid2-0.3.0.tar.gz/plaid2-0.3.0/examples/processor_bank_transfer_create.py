import os
from plaid2 import AsyncPlaidClient
from plaid2 import PlaidClient
from plaid2.model import *


def main():
    client = PlaidClient.from_env()
    response = client.processor_bank_transfer_create(
        idempotency_key="your idempotency key",
        processor_token="your processor token",
        type="your type",
        network="your network",
        amount="your amount",
        iso_currency_code="your iso currency code",
        description="your description",
        user=BankTransferUser(
            email_address="your email address",
            routing_number="your routing number",
            legal_name="your legal name",
        ),
    )
    print(f"{response!r}")


async def async_main():
    client = AsyncPlaidClient.from_env()
    response = await client.processor_bank_transfer_create(
        idempotency_key="your idempotency key",
        processor_token="your processor token",
        type="your type",
        network="your network",
        amount="your amount",
        iso_currency_code="your iso currency code",
        description="your description",
        user=BankTransferUser(
            email_address="your email address",
            routing_number="your routing number",
            legal_name="your legal name",
        ),
    )
    print(f"{response!r}")


if __name__ == "__main__":
    if os.environ.get("ASYNC"):
        import asyncio

        asyncio.run(async_main())
    else:
        main()
