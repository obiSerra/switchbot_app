from dataclasses import dataclass
import time
import hashlib
import hmac
import base64


@dataclass
class AuthData:
    token: str
    t: int
    sign: str
    nonce: str

    def to_headers(self):
        return {"Authorization": self.token, "sign": self.sign, "nonce": self.nonce, "t": self.t}


def authenticate(token, secret):
    nonce = ""
    t = int(round(time.time() * 1000))
    string_to_sign = "{}{}{}".format(token, t, nonce)

    string_to_sign = bytes(string_to_sign, "utf-8")
    secret = bytes(secret, "utf-8")

    sign = base64.b64encode(hmac.new(secret, msg=string_to_sign, digestmod=hashlib.sha256).digest())
    return AuthData(**{"token": token, "t": str(t), "sign": sign, "nonce": nonce})
