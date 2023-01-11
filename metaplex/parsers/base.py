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
    def account_keys(self):
        return self.transactions.value.transaction.transaction.message.account_keys

    @cached_property
    def inner_instructions(self):
        return self.transactions.value.transaction.meta.inner_instructions

    @cached_property
    def token_balances(self):
        return self.transactions.value.transaction.meta.post_token_balances

    @cached_property
    def auction_account(self):
        return [
            o.owner for o in self.token_balances
            if int(o.ui_token_amount.amount) > 0
        ][0]

