#!/usr/bin/python3
from genkey import *
from mpeck import mpeck, mdec
import trapdoor


# Lucas


def Test(pub_key: Element, _A: Element, _B: List[Element], _C: List[Element], T: List[Union[int, Element]], j: int, genkey: KeyGen):
    #  S = [A, B, C]

    A = _A  # g^r
    B = _B  # pk^s
    C = _C  # l total crypted keywords (h^r)(f^s)
    I: List[int] = T[3:]  # m indexes of keywords from the query

    # Intermediate computation
    keywords_product: Element = Element.one(genkey.pairing, G1)
    for i in I:
        keywords_product *= C[i]
    E1: Element = genkey.e(T[0], keywords_product)
    G3: Element = genkey.e(A, T[1])
    G2: Element = genkey.e(B[j], T[2])
    E2: Element = G3 * G2
    print(E1)
    print(E2)
    # Test verification
    if E1 == E2:
        return 1  # keywords match
    else:
        return 0  # keywords don't match


if __name__ == "__main__":
    # number of users
    n = 3
    # number of keywords
    l = 2

    # Keys generation
    k: KeyGen = KeyGen(n)

    # mPeck
    _message = "This is the message"
    _keywords = ["test", "encryption"]
    # there are 3 clients, only allow 0 and 1 to search and decrypt
    _recipients = [0, 1]
    _recipients_pk = [k.pub_keys[r] for r in _recipients]

    _E, _A, _B, _C = mpeck(_recipients_pk, _keywords, k, message=_message)
    for _i in range(len(_recipients)):
        m = mdec(k.priv_keys[_i], _E, _B[_i], _A, k)
        print(f"Client {_i}: decryption is: {m}")
    user = 0
    keyword_index = 0
    # trapdoor generation (query from user j)
    T = trapdoor.generate_trapdoor(k.priv_keys[user], [keyword_index], [_keywords[keyword_index]], k)
    # Test
    print(Test(k.pub_keys[user], _A, _B, _C, T, 0, k))
