from enum import IntEnum


class AuctionStates(IntEnum):
    INITIALIZED = 0
    CONFIGURED = 1
    BIDDED = 2
    PLATFORM_FEE_PAID = 3
    CLOSED = 4
    CANCELLED = 5


class AuctionTypes(IntEnum):
    BUY_NOW = 0
    ENGLISH = 1
    DUTCH = 2


class DecoderTypes(IntEnum):
    STRING = 1
    INTEGER = 2