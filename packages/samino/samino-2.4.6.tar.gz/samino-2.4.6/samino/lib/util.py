import base64
import hashlib
import hmac
from uuid import uuid4

# tapjoy = "https://ads.tapdaq.com/v4/analytics/reward"
webApi = "https://aminoapps.com/api{}".format
api = "https://service.aminoapps.com/api/v1{}".format


def generateSig(data: str):
    return base64.b64encode(
        bytes.fromhex("52") + hmac.new(bytes.fromhex("eab4f1b9e3340cd1631ede3b587cc3ebedf1afa9"),
        data.encode(),
        hashlib.sha1).digest()
    ).decode()

def generateDevice():
    data = uuid4().bytes
    return (
        "52" + data.hex() +
        hmac.new(bytes.fromhex("ae49550458d8e7c51d566916b04888bfb8b3ca7d"),
        bytes.fromhex("52") + data,
        hashlib.sha1).hexdigest()
        ).upper()

def uuidString():
    return str(uuid4())
