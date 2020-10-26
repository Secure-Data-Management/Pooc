#!/usr/bin/python3
from typing import Callable, List, Tuple

from crypto.bn256 import *
from genkey import KeyGen
# Antoine
import hashlib

xor: Callable[[bytes, bytes], bytearray] = lambda part1, part2: bytearray([e1 ^ e2 for (e1, e2) in zip(part1, part2)])


def hash_G2_to_M(g: str, length=64) -> bytes:
    """Takes an element of G2, and hashes it to a bytes object"""
    g_bytes: bytes = g.encode()
    g_hash: bytes = hashlib.sha3_512(g_bytes).digest()
    result: bytes = g_hash
    # TODO: find a way to generate a hash of length equal to the given length
    while len(result) < length:
        result += g_hash
    result: bytes = result[:length]
    return result


def mpeck(pk_list:List[CurvePoint], W:List[str], genkey: KeyGen, message:str="")-> Tuple[bytearray,CurvePoint, List[CurvePoint], List[CurvePoint]]:
    """
    multi Public key Encryption with Conjuctive Keyword. Encrypts both message and keywords !
    Performs the encryption of the keywords and of the message, using the mPECK model. Encrypts the keywords in W using the public keys in pk_list
    Parameters:
        pk: list of keys (from Keygen.keys)
        W: set of keywords
        params: a dictionary containing the security parameters
    Returns:
        [E, A, B, C] as in the paper, E=b"" if there was no message
            [A, B, C] with A=g^r, B=[B1, ..., Bn] and C=[C1, ..., Cl]
    """
    # TODO: to remove if hashes accept strings
    # convert keywords to bytes:
    # for i, kw in enumerate(W):
    # if isinstance(kw, str):
    #     kw_bytes = kw.encode("utf-8")
    #     W[i] = kw_bytes

    # selects two random values in Zp*
    s: int = rand_elem()
    r: int = rand_elem()
    # computes the A=g^r
    A:CurvePoint = g1_scalar_base_mult(r)
    # computes B = pk**s for each public key
    n = len(pk_list)
    B :List[CurvePoint]= []
    for j in range(n):
        yj: CurvePoint = genkey.pub_keys[j]
        B.append(yj.scalar_mul(s))
    # computes C = (h^r)(f^s) for each keyword
    l = len(W)
    C: List[CurvePoint]= []
    for i, kw in enumerate(W):
        h = genkey.h1(kw)
        f = genkey.h2(kw)
        # ** -> * ; * -> +
        temp1: CurvePoint = h.scalar_mul(r)
        temp2: CurvePoint = f.scalar_mul(s)
        C.append(temp1.add(temp2))
    # encode the message
    E: bytearray = bytearray()
    if len(message) > 0:
        # TODO: to remove if hashes accept strings
        # if not isinstance(message, bytes):
        #     message = message.encode("utf-8")
        e_g_g: gfp_12 = genkey.e(twist_G, genkey.g)
        e_r_s = r * s
        e_g_g1: gfp_12 = e_g_g.exp(e_r_s)
        e_g_g2: bytes = hash_G2_to_M(e_g_g1.__repr__())
        E: bytearray = xor(e_g_g2, message.encode())
        print(E)
    # FIXME: e n'est pas de la bonne forme, elle ne peut pas prendre (g,g) comme argument donc impossible de faire le chiffrement du message

    return E, A, B, C


def mdec(xj: int, E: bytearray, Bj:CurvePoint, A:CurvePoint, k:KeyGen):
    """Decrypts the cipher E, using private key xj, Bj and A"""
    print(A.x,A.y,A.z)
    e_A_Bj: gfp_12 = k.e(A,Bj)
    Xj = hash_G2_to_M(e_A_Bj.mul_scalar(1 / xj))
    m = xor(E, Xj)
    m = m.decode()
    return m


if __name__ == "__main__":
    # number of participants
    n = 3
    k = KeyGen(n)
    # encryption of the message
    message = "This is the message"
    keywords = ["test", "encryption"]
    # there are 3 clients, only allow 0 and 1 to search and decrypt
    recipients = [0, 1]
    recipients_pk = [k.pub_keys[r] for r in recipients]
    E, A, B, C = mpeck(recipients_pk, keywords, k, message=message)
    print(f"Message \"{message}\" encrypted, only recipients {recipients} are allowed to decrypt")
    # decrypt as 0
    for i in range(n):
        m = mdec(k.priv_keys[i], E, B[i], A, k)
        print(f"Client {i}: decryption is: {m}")
