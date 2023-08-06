from .account import Account
from .autodiscover import discover
from .configuration import Configuration
from .credentials import DELEGATE, IMPERSONATION, Credentials
from .ewsdatetime import EWSDateTime, EWSTimeZone
from .restriction import Restriction, Q
from .services import IdOnly, AllProperties, SHALLOW, DEEP
from .transport import NTLM, DIGEST, BASIC


def close_connections():
    from .autodiscover import close_connections as close_autodiscover_connections
    from .protocol import close_connections as close_protocol_connections
    close_autodiscover_connections()
    close_protocol_connections()
