import os
from plaid2 import AsyncPlaidClient
from plaid2 import PlaidClient
from plaid2.model import *

access_token = "your access token"
personal_finance_category = "your personal finance category"
rule_details = TransactionsRuleDetails(
    field="your field",
    type="your type",
    query="your query",
)


def main():
    client = PlaidClient.from_env()
    response = client.transactions_rules_create(access_token, personal_finance_category, rule_details)
    print(f"{response!r}")


async def async_main():
    client = AsyncPlaidClient.from_env()
    response = await client.transactions_rules_create(access_token, personal_finance_category, rule_details)
    print(f"{response!r}")


if __name__ == "__main__":
    if os.environ.get("ASYNC"):
        import asyncio

        asyncio.run(async_main())
    else:
        main()
