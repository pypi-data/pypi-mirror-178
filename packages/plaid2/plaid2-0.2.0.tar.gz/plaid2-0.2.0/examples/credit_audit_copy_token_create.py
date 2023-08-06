import os
from plaid2 import AsyncPlaidClient
from plaid2 import PlaidClient
from plaid2.model import *

report_tokens = [
    ReportToken(
        report_type="your report type",
        token="your token",
    )
]
auditor_id = "your auditor id"


def main():
    client = PlaidClient.from_env()
    response = client.credit_audit_copy_token_create(report_tokens, auditor_id)
    print(f"{response!r}")


async def async_main():
    client = AsyncPlaidClient.from_env()
    response = await client.credit_audit_copy_token_create(report_tokens, auditor_id)
    print(f"{response!r}")


if __name__ == "__main__":
    if os.environ.get("ASYNC"):
        import asyncio

        asyncio.run(async_main())
    else:
        main()
