import base58
from solana.publickey import PublicKey

from metaplex.base import SolanaParser
from metaplex.enums import AuctionStates, AuctionTypes, DecoderTypes


class AuctionParser(SolanaParser):
    def __init__(self, client, transaction_hash):
        super().__init__(client, transaction_hash)
        self.data = self.client.get_account_info(
            PublicKey(self.auction_account)
        ).value.data
        self.i = 0
        self.auction_data = {}

    USER_AUCTION_STATES = [
        AuctionStates.PLATFORM_FEE_PAID,
        AuctionStates.BIDDED,
        AuctionStates.CLOSED
    ]

    def decode_bytes(
            self,
            decoder_type: DecoderTypes,
            number_of_bytes: int,
            name=None,
            enum_type=None,
            decoded_data=None
    ):
        data_bytes = self.data[self.i: self.i + number_of_bytes]
        if decoder_type == DecoderTypes.STRING:
            decoded_data = base58.b58encode(data_bytes).decode()
        elif decoder_type == DecoderTypes.INTEGER:
            decoded_data = int.from_bytes(data_bytes, "little")
        self.i += number_of_bytes
        self.auction_data[name] = enum_type(decoded_data) if enum_type else decoded_data
        return decoded_data

    def unpack_auction_data(self):
        # bumps
        self.decode_bytes(DecoderTypes.INTEGER, 8, "discriminator")
        self.decode_bytes(DecoderTypes.INTEGER, 1, "auction_bump")
        self.decode_bytes(DecoderTypes.INTEGER, 1, "wallet_bump")
        self.decode_bytes(DecoderTypes.INTEGER, 1, "vault_bump")
        self.decode_bytes(DecoderTypes.INTEGER, 8, "time_shift")

        # auction_house
        self.decode_bytes(DecoderTypes.STRING, 32, "auction_house")

        # state

        state = self.decode_bytes(DecoderTypes.INTEGER, 1, "state", AuctionStates)
        if state in self.USER_AUCTION_STATES:
            self.decode_bytes(DecoderTypes.INTEGER, 8, "amount")
            self.decode_bytes(DecoderTypes.STRING, 32, "user")

        # settings
        self.decode_bytes(DecoderTypes.STRING, 8, "auction_id")
        self.decode_bytes(DecoderTypes.STRING, 32, "owner")
        self.decode_bytes(DecoderTypes.INTEGER, 1, "creator_mask")
        self.decode_bytes(DecoderTypes.STRING, 32, "nft")
        self.decode_bytes(DecoderTypes.INTEGER, 8, "start_time")
        self.decode_bytes(DecoderTypes.INTEGER, 8, "end_time")
        auction_type = self.decode_bytes(
            DecoderTypes.INTEGER, 1, "type", AuctionTypes
        )
        if auction_type == AuctionTypes.BUY_NOW:
            self.decode_bytes(DecoderTypes.INTEGER, 8, "price")
        if auction_type == AuctionTypes.ENGLISH:
            self.decode_bytes(DecoderTypes.INTEGER, 8, "start_price")
            self.decode_bytes(DecoderTypes.INTEGER, 8, "minimum_price")
        elif auction_type == AuctionTypes.DUTCH:
            self.decode_bytes(DecoderTypes.INTEGER, 8, "start_price")
            self.decode_bytes(DecoderTypes.INTEGER, 8, "step")
            self.decode_bytes(DecoderTypes.INTEGER, 8, "step_interval")
            self.decode_bytes(DecoderTypes.INTEGER, 1, "step_count")
        self.decode_bytes(DecoderTypes.INTEGER, 2, "house_fee_basis_points")
        return self.auction_data
