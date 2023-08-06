import os
from plaid2 import AsyncPlaidClient
from plaid2 import PlaidClient
from plaid2.model import *

client_user_id = "your client user id"
template_id = "your template id"
strategy = "your strategy"


def main():
    client = PlaidClient.from_env()
    response = client.identity_verification_retry(client_user_id, template_id, strategy)
    print(f"{response!r}")


async def async_main():
    client = AsyncPlaidClient.from_env()
    response = await client.identity_verification_retry(client_user_id, template_id, strategy)
    print(f"{response!r}")


if __name__ == "__main__":
    if os.environ.get("ASYNC"):
        import asyncio

        asyncio.run(async_main())
    else:
        main()
