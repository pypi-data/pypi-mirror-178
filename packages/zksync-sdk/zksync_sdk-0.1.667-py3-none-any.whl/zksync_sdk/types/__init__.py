from enum import IntEnum

from .responses import *
from .signatures import *
from .transactions import *
from .auth_types import *


class ChainId(IntEnum):
    MAINNET = 1
    RINKEBY = 4
    GOERLI = 5
    ROPSTEN = 3
    LOCALHOST = 9
