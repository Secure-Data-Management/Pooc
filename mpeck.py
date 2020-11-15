#!/usr/bin/python3
import base64
import hashlib
import json
from typing import Optional

from Crypto.Cipher import AES

from genkey import *


def encrypt(message: Union[bytearray, bytes, str], key: Union[bytearray, bytes]) -> Tuple[bytes, bytes, bytes]:
    cipher = AES.new(key, AES.MODE_EAX)
    ciphertext, tag = cipher.encrypt_and_digest(message)
    return ciphertext, tag, cipher.nonce


def decrypt(message: Union[bytearray, bytes, str], key: Union[bytearray, bytes], tag: Union[bytearray, bytes], nonce: Union[bytearray, bytes]) -> Tuple[bytes, bool]:
    cipher = AES.new(key, AES.MODE_EAX, nonce=nonce)
    plaintext: bytes = cipher.decrypt(message)
    try:
        cipher.verify(tag)
        res = True
    except ValueError:
        res = False
    return plaintext, res


def xor(message: Union[bytearray, bytes, str], key: Union[bytearray, bytes]) -> bytearray:
    res: bytearray = bytearray()
    if type(message) == str:
        message = bytearray(message.encode())
    elif type(message) == bytes:
        message = bytearray(message)
    if type(key) == bytes:
        key = bytearray(key)
    if len(message) > len(key):
        for i in range(len(message)):
            res.append(message[i] ^ key[i % len(key)])
    else:
        for i in range(len(message)):
            res.append(key[i] ^ message[i % len(message)])
    return res


def mpeck(pk_list: List[Element], keyword_list: List[str], genkey: KeyGen, message: str = "") -> Tuple[bytearray, Element, List[Element], List[Element]]:
    s: Element = Element.random(genkey.pairing, Zr)
    r: Element = Element.random(genkey.pairing, Zr)
    A: Element = genkey.g ** r
    n = len(pk_list)
    B: List[Element] = []
    for j in range(n):
        yj: Element = genkey.pub_keys[j]
        B.append(yj ** s)
    C: List[Element] = []
    for i, kw in enumerate(keyword_list):
        h = genkey.h1(kw)
        f = genkey.h2(kw)
        temp1: Element = h ** r
        temp2: Element = f ** s
        C.append(temp1 * temp2)
    E: bytearray = bytearray()
    if len(message) > 0:
        e_g_g: Element = genkey.pairing.apply(genkey.g, genkey.g)
        e_r_s: Element = r * s
        e_g_g1: Element = e_g_g ** e_r_s
        e_g_g2: bytes = hashlib.sha256(e_g_g1.__str__().encode()).digest()
        ciphertext, tag, nonce = encrypt(message.encode(), e_g_g2)
        E: bytearray = bytearray(json.dumps({
            "ciphertext": base64.b64encode(ciphertext).decode(),
            "tag": base64.b64encode(tag).decode(),
            "nonce": base64.b64encode(nonce).decode(),
        }).encode())
    return E, A, B, C


def mdec(xj: Element, E: bytearray, Bj: Element, A: Element, k: KeyGen) -> Optional[str]:
    e_A_Bj: Element = k.e(A, Bj)
    res: Element = e_A_Bj ** (~xj)
    Xj = hashlib.sha256(res.__str__().encode()).digest()
    j = json.loads(E.decode())
    plaintext, verify = decrypt(base64.b64decode(j["ciphertext"]), Xj, base64.b64decode(j["tag"]), base64.b64decode(j["nonce"]))
    return plaintext.decode() if verify else None


if __name__ == "__main__":
    # number of participants
    _n = 3
    k = KeyGen(_n)
    # encryption of the message
    _message = "This is the message"
    _keywords = ["test", "encryption"]
    # there are 3 clients, only allow 0 and 1 to search and decrypt
    _recipients = [0, 1]
    _recipients_pk = [k.pub_keys[r] for r in _recipients]
    _E, _A, _B, _C = mpeck(_recipients_pk, _keywords, k, message=_message)
    print(f"Message \"{_message}\" encrypted, only recipients {_recipients} are allowed to decrypt")
    # decrypt as 0
    for _i in range(len(_recipients)):
        m = mdec(k.priv_keys[_i], _E, _B[_i], _A, k)
        print(f"Client {_i}: decryption is: {m}")
