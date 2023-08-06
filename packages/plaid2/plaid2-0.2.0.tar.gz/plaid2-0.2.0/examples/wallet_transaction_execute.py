import os
from plaid2 import AsyncPlaidClient
from plaid2 import PlaidClient
from plaid2.model import *


def main():
    client = PlaidClient.from_env()
    response = client.wallet_transaction_execute(
        idempotency_key="your idempotency key",
        wallet_id="your wallet id",
        counterparty=WalletTransactionCounterparty(
            name_="your name",
            numbers=WalletTransactionCounterpartyNumbers(
                international="your international",
                bacs=RecipientBacs(
                    sort_code="your sort code",
                    account="your account",
                ),
            ),
        ),
        amount=WalletTransactionAmount(
            value=1.0,
            iso_currency_code="your iso currency code",
        ),
        reference="your reference",
    )
    print(f"{response!r}")


async def async_main():
    client = AsyncPlaidClient.from_env()
    response = await client.wallet_transaction_execute(
        idempotency_key="your idempotency key",
        wallet_id="your wallet id",
        counterparty=WalletTransactionCounterparty(
            name_="your name",
            numbers=WalletTransactionCounterpartyNumbers(
                international="your international",
                bacs=RecipientBacs(
                    sort_code="your sort code",
                    account="your account",
                ),
            ),
        ),
        amount=WalletTransactionAmount(
            value=1.0,
            iso_currency_code="your iso currency code",
        ),
        reference="your reference",
    )
    print(f"{response!r}")


if __name__ == "__main__":
    if os.environ.get("ASYNC"):
        import asyncio

        asyncio.run(async_main())
    else:
        main()
