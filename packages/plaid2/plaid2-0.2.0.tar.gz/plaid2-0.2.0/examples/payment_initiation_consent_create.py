import os
from plaid2 import AsyncPlaidClient
from plaid2 import PlaidClient
from plaid2.model import *


def main():
    client = PlaidClient.from_env()
    response = client.payment_initiation_consent_create(
        recipient_id="your recipient id",
        reference="your reference",
        scopes=["your scopes"],
        constraints=PaymentInitiationConsentConstraints(
            max_payment_amount=PaymentAmount(
                currency="your currency",
                value=1.0,
            ),
            valid_date_time=PaymentConsentValidDateTime(
                to="your to",
                from_="your from",
            ),
            periodic_amounts=[
                PaymentConsentPeriodicAmount(
                    amount=PaymentAmount(
                        currency="your currency",
                        value=1.0,
                    ),
                    interval="your interval",
                    alignment="your alignment",
                )
            ],
        ),
    )
    print(f"{response!r}")


async def async_main():
    client = AsyncPlaidClient.from_env()
    response = await client.payment_initiation_consent_create(
        recipient_id="your recipient id",
        reference="your reference",
        scopes=["your scopes"],
        constraints=PaymentInitiationConsentConstraints(
            max_payment_amount=PaymentAmount(
                currency="your currency",
                value=1.0,
            ),
            valid_date_time=PaymentConsentValidDateTime(
                to="your to",
                from_="your from",
            ),
            periodic_amounts=[
                PaymentConsentPeriodicAmount(
                    amount=PaymentAmount(
                        currency="your currency",
                        value=1.0,
                    ),
                    interval="your interval",
                    alignment="your alignment",
                )
            ],
        ),
    )
    print(f"{response!r}")


if __name__ == "__main__":
    if os.environ.get("ASYNC"):
        import asyncio

        asyncio.run(async_main())
    else:
        main()
