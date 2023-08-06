import os
from plaid2 import AsyncPlaidClient
from plaid2 import PlaidClient
from plaid2.model import *

client_transaction_id = "your client transaction id"
return_code = "your return code"


def main():
    client = PlaidClient.from_env()
    response = client.signal_return_report(client_transaction_id, return_code)
    print(f"{response!r}")


async def async_main():
    client = AsyncPlaidClient.from_env()
    response = await client.signal_return_report(client_transaction_id, return_code)
    print(f"{response!r}")


if __name__ == "__main__":
    if os.environ.get("ASYNC"):
        import asyncio

        asyncio.run(async_main())
    else:
        main()
