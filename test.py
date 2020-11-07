#!/usr/bin/python3
import genkey
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
    params = "type a q 5190226450145940880746663486308966347220639714045250223182499121249068575513554544422970314418344770379996438351407014419358038003225732626831022128438331 h 7102594095788614028758769623913839942835962504311385389572759256033849452424444030966227463924769974838212 r 730750818665452757176057050065048642452048576511 exp2 159 exp1 110 sign1 1 sign0 -1 "
    k: KeyGen = KeyGen(n, params)

    # mPeck
    _message = "This is the message"
    _keywords = ["test", "encryption"]
    # there are 3 clients, only allow 0 and 1 to search and decrypt
    _recipients = [1, 2]
    _recipients_pk = [k.pub_keys[r] for r in _recipients]

    int_s = 0x1CF57D847CE6B7F5565B8E578A954513877DCAD0
    int_r = 0x61D70D8B9F955B27A593E7E6E2FDCB718BD2088F
    _E, _A, _B, _C = mpeck(_recipients_pk, _keywords, k, random_r=int_r, random_s=int_s, message=_message)
    for _i, _r in enumerate(_recipients):
        m = mdec(k.priv_keys[_r], _E, _B[_i], _A, k)
        print(f"Client {_r}: decryption is: {m}")
    user = 1
    keyword_index = 0
    t: Element = Element(k.pairing, Zr,value=0x7424D84332FA1367EB82D66D6829E8D651AF2F58)
    # trapdoor generation (query from user j)
    T = trapdoor.generate_trapdoor(k.priv_keys[user], [keyword_index], [_keywords[keyword_index]], k,t)
    # Test
    print(Test(k.pub_keys[user], _A, _B, _C, T, 0, k))
