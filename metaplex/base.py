from functools import cached_property
from solders.signature import Signature


class SolanaParser:
    def __init__(self, client, transaction_hash):
        self.client = client
        self.transaction_hash = Signature.from_string(transaction_hash)

    @cached_property
    def transactions(self):
        return self.client.get_transaction(self.transaction_hash)

    @cached_property
    def accounts(self):
        return self.transactions.value.transaction.transaction.message.account_keys

    @cached_property
    def auction_account(self):
        return self.accounts[3]  # auction account is 3rd in list
