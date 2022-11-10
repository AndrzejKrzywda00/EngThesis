from enum import Enum


# Status of data packet
class Status(Enum):
    EMPTY = 0
    SENT = 1
    RECEIVED = 2
