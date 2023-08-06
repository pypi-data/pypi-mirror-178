"""pynetsys is a collection of tools and malicious packets."""

from .error import PYNETSYS
from .constants import Protocol, Packets
from . import _tool, _packet
from requests import get
from socket import getfqdn

ERROR = PYNETSYS

__version__ = []
__author__ = "Andrea Vaccaro ANDRVV"

tool, packet = _tool, _packet

def hasSSLWebProtocol(Address: str):
    # RETURN
    if "https:\\" in Address:
        return True
    else:
        return False

def hasWebProtocol(Address: str):
    # RETURN
    if "http:\\" in Address:
        return True
    else:
        return False

def addWebProtocol(Address: str, SSL: int = False):
    # RETURN
    if hasWebProtocol(Address):
        raise ERROR("Already have a web protocol.")    
    else:
        if SSL == True:
            return f"https://{Address}/"
        else:
            return f"http://{Address}/"

def removeWebProtocol(Address: str):
    # RETURN
    if hasWebProtocol(Address) or hasSSLWebProtocol(Address):
        return Address.replace("http://", "").replace("https://", "").replace("/", "")
    else:
        raise ERROR("There is not a web protocol.")    

def isOnline(Address: str):
    # IMPORT
    from scapy.all import sr1
    from scapy.layers.inet import IP, ICMP
    import socket

    # RUN & RETURN
    try:
        if sr1(IP(dst = socket.gethostbyname(Address))/ICMP(), timeout = 1, verbose = 0) is None:
            return False
        else:
            return True
    except:
        return False
