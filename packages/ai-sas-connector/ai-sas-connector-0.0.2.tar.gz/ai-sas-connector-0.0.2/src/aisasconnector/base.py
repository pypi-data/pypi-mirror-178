import base64
from Crypto.Cipher import AES
from Crypto import Random


key = [0x10, 0x01, 0x15, 0x1B, 0xA1, 0x11, 0x57, 0x72, 0x6C, 0x21, 0x56, 0x57, 0x62, 0x16, 0x05, 0x3D,
       0xFF, 0xFE, 0x11, 0x1B, 0x21, 0x31, 0x57, 0x72, 0x6B, 0x21, 0xA6, 0xA7, 0x6E, 0xE6, 0xE5, 0x3F]
BS = 16

pad = lambda s: s + (BS - len(s.encode()) % BS) * chr(BS - len(s.encode()) % BS)
unpad = lambda s: s[0 :-s[-1]]

class Configuration:
    def __init__(self):
        self.key = bytes(key)
        self.sc = None
        self.descure_str()

    def enscure(self, enc):
        enc = pad(enc)
        iv = Random.new().read(AES.block_size)
        cipher = AES.new(self.key, AES.MODE_CFB, iv)
        return base64.b64encode(iv + cipher.encrypt(enc.encode("utf--8")))

    def descure(self, enc):
        enc = base64.b64decode(enc)
        iv = enc[:16]
        cipher = AES.new(self.key, AES.MODE_CFB, iv)
        return unpad(cipher.decrypt(enc[16:]))

    def enscure_str(self, raw):
        return self.enscure(raw).decode("utf-8")

    def descure_str(self):
        enc = "1Y7wpHCAfNYwSP5n3DqFFjZbrxRidpH25zBeVmX3cjl6ckipHTXaiESobIiW3ECVbBaZpZT47x+OvLQyVow2lQ=="
        if type(enc) == str:
            enc = str.encode(enc)
        self.sc = self.descure(enc).decode("utf-8")


test = Configuration()
print(test.sc)