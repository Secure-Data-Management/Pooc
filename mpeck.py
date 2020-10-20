#!/usr/bin/python3
from petrelic.multiplicative.pairing import G1, G2, GT, G1Element, G2Element
from genkey import KeyGen
# Antoine
import hashlib


def hash_G2_to_M(g, length=64):
    """Takes an element of G2, and hashes it to a bytes object"""
    g_bytes = g.to_binary()
    g_hash = hashlib.sha3_512(g_bytes).digest()
    result = g_hash
    #TODO: find a way to generate a hash of length equal to the given length
    while len(result) < length:
        result += g_hash
    result = result[:length]
    return result


def mPECK(pk_list, W, params, message=""):
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
    #TODO: to remove if hashes accept strings
    # convert keywords to bytes:
    # for i, kw in enumerate(W):
        # if isinstance(kw, str):
        #     kw_bytes = kw.encode("utf-8")
        #     W[i] = kw_bytes

    # selects two random values in Zp*
    s = GT.order().random()
    r = GT.order().random()
    # computes the A=g^r
    A = params["g"] ** r
    # computes B = pk**s for each public key
    n = len(pk_list)
    B = [0 for i in range(n)]
    for j in range(n):
        yj = pk_list[j]
        B[j] = yj ** s
    # computes C = (h^r)(f^s) for each keyword
    l = len(W)
    C = [0 for i in range(l)]
    for i, kw in enumerate(W):
        h = params["H1"](kw)
        f = params["H2"](kw)
        C[i] = h**r * f**s

    #encode the message
    E = b""
    if len(message) > 0:
        #TODO: to remove if hashes accept strings
        # if not isinstance(message, bytes):
        #     message = message.encode("utf-8")
        E = hash_G2_to_M(params["e"](params["g"], params["g"]) ** (r*s)) ^ message
        print(E)
    #FIXME: e n'est pas de la bonne forme, elle ne peut pas prendre (g,g) comme argument donc impossible de faire le chiffrement du message

    return [E, A, B, C]



def mDEC(xj, E, Bj, A):
    """Decrypts the cipher E, using private key xj, Bj and A"""
    Xj = hash_G2_to_M(params["e"](A, Bj)**(1/xj))
    m = E ^Xj
    m = m.decode()
    return m



if __name__ == "__main__":
    # number of participants
    n = 3
    k = KeyGen(n)
    params = {"G1":G1, "G2":G2, "e":k.e, "H1":k.h1, "H2":k.h2, "g":k.g1}
    pk_list = [key[1] for key in k.keys]
    sk_list = [key[0] for key in k.keys]
    #encryption of the message
    message = "This is the message"
    keywords = ["test", "encryption"]
    # there are 3 clients, only allow 0 and 1 to search and decrypt
    recipients = [0, 1]
    recipients_pk = [pk_list[r] for r in recipients]
    E, A, B, C = mPECK(recipients_pk, keywords, params, message=message)
    print(f"Message \"{message}\" encrypted, only recipients {recipients} are allowed to decrypt")
    # decrypt as 0
    for i in range(n):
        m = mDEC(sk_list[i], E, B[i], A)
        print(f"Client {i}: decryption is: {m}")