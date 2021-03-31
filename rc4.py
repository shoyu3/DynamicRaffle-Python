import base64
import hashlib
import os
from io import BytesIO


class RC4(object):
    def __init__(self, key=None):
        self.key = hashlib.md5(key.encode("utf-8")).hexdigest()

    def encode(self, in_stream, out_stream):
        sbox = self.sbox()
        while 1:
            chunk = in_stream.read(8)

            if not chunk:
                break

            out_chuck = bytearray()
            for bt in chunk:
                out_chuck.append(bt ^ next(sbox))
            out_stream.write(bytes(out_chuck))

    def sbox(self):
        keylength = len(self.key)

        s = list(range(256))  # init S box

        j = 0
        for i in range(255):
            j = (j + s[i] + ord(self.key[i % keylength])) % 256
            s[i], s[j] = s[j], s[i]

        i = 0
        j = 0
        while 1:
            i = (i + 1) % 256
            j = (j + s[i]) % 256
            s[i], s[j] = s[j], s[i]
            yield s[(s[i] + s[j]) % 256]


def encrypt(in_stream: BytesIO, out_stream: BytesIO, pwd: str):
    rc4_cryptor = RC4(pwd)
    rc4_cryptor.encode(in_stream, out_stream)

# 下面都是锦上添花的东西，和rc4没啥关系
def encrypt_str(data: str, pwd: str):
    in_stream = BytesIO()
    out_stream = BytesIO()

    data_bytes = data.encode("utf-8")

    # 魔改 引入随机IV打乱原文，不喜欢的话就删之吧。：）
    iv = os.urandom(1)[0]
    tp_v = iv

    data_xor_iv = bytearray()
    for bt in data_bytes:
        data_xor_iv.append(bt ^ tp_v)
        tp_v = bt ^ tp_v

    in_stream.write(data_xor_iv)
    in_stream.seek(0)

    encrypt(in_stream, out_stream, pwd)

    enc_bytes = bytes([iv]) + out_stream.getvalue()
    b64_str = base64.urlsafe_b64encode(enc_bytes)
    return b64_str.decode("utf-8")


def decrypt_str(data: str, pwd: str):
    data_bytes = base64.urlsafe_b64decode(data)
    in_stream = BytesIO()
    out_stream = BytesIO()

    iv = data_bytes[:1][0]

    in_stream.write(data_bytes[1:])
    in_stream.seek(0)

    encrypt(in_stream, out_stream, pwd)
    dec_bytes = out_stream.getvalue()

    data_xor_iv = bytearray()
    for bt in dec_bytes:
        data_xor_iv.append(bt ^ iv)
        iv = bt

    return data_xor_iv.decode('utf-8')

'''
if __name__ == "__main__":
    test_byte_data = "hello world 世界你好"
    ret = encrypt_str(test_byte_data, 'yzh')
    print(ret)

    ret = decrypt_str(ret, 'yzh')
    print(ret)
    assert test_byte_data == ret

    ret = encrypt_str("1#1500000000", 'yzh')
    print(ret, len(ret))

    ret = encrypt_str("111111#1500000000", 'yzh')
    print(ret, len(ret))

    ret = encrypt_str("99999999#1500000000", 'yzh')
    print(ret, len(ret))'''

