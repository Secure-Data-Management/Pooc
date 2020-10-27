#!/usr/bin/python3
from petrelic.bn import Bn

from genkey import *
from mpeck import mpeck
import trapdoor


# Lucas


def Test(pk, S, T, j):
    #  S = [A, B, C]

    A = S[0]  # g^r
    B = S[1]  # pk^s
    C = S[2]  # l total crypted keywords (h^r)(f^s)
    I = T[3:]  # m indexes of keywords from the query

    # Intermediate computation
    keywords_product: G1Element = G1.neutral_element()
    for i in I:
        keywords_product *= C[i]

    # Test verification
    if (params["e"](T[0], keywords_product) == params["e"](A, T[1]) * params["e"](B[j], T[2])):
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
    S = mpeck(_recipients_pk, _keywords, k, message=_message)[1]

    # trapdoor generation (query from user j)
    T = trapdoor.generate_trapdoor(sk_list[0], [1, "encryption"], 1, params)

    # Test
    print(Test(pk_list, S, T, 1))
