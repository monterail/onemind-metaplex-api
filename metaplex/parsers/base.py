import logging

from solders.signature import Signature
from solana.exceptions import SolanaRpcException


class SolanaParser:
    def __init__(self, client, transaction_hash):
        self.client = client
        self.transaction_hash = Signature.from_string(transaction_hash)

    @property
    def transactions(self):
        try:
            return self.client.get_transaction(self.transaction_hash)
        except SolanaRpcException as e:
            logging.error(f"SOLANA RPC ERROR: {e}")
            return

    @property
    def account_keys(self):
        return self.transactions.value.transaction.transaction.message.account_keys

    @property
    def inner_instructions(self):
        return self.transactions.value.transaction.meta.inner_instructions

    @property
    def pre_token_balances(self):
        return self.transactions.value.transaction.meta.pre_token_balances

    @property
    def post_token_balances(self):
        return self.transactions.value.transaction.meta.post_token_balances

    @property
    def auction_account(self):
        return [
            o.owner for o in self.post_token_balances
            if int(o.ui_token_amount.amount) > 0
        ][0]

