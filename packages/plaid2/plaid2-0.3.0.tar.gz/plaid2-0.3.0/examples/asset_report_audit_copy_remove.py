import os
from plaid2 import AsyncPlaidClient
from plaid2 import PlaidClient
from plaid2.model import *

audit_copy_token = "your audit copy token"


def main():
    client = PlaidClient.from_env()
    response = client.asset_report_audit_copy_remove(audit_copy_token)
    print(f"{response!r}")


async def async_main():
    client = AsyncPlaidClient.from_env()
    response = await client.asset_report_audit_copy_remove(audit_copy_token)
    print(f"{response!r}")


if __name__ == "__main__":
    if os.environ.get("ASYNC"):
        import asyncio

        asyncio.run(async_main())
    else:
        main()
