import base58
from metaplex.parsers.base import SolanaParser


class BidParser(SolanaParser):

    def __init__(self, client, transaction_hash):
        super().__init__(client, transaction_hash)
        self.instructions = self.inner_instructions[0].instructions

    @property
    def bidder_wallet_address(self):
        return self.account_keys[self.instructions[0].accounts[0]]

    @property
    def auction_contract_address(self):
        return self.account_keys[self.instructions[0].accounts[1]]

    @property
    def amount(self):
        return sum(
            [
                int.from_bytes(
                    base58.b58decode(i.data)[4:12], "little"
                ) for i in self.instructions
            ]
        )
