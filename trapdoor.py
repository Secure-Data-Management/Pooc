#!/usr/bin/python3
from genkey import *


def generate_trapdoor(priv_key: Element, index_list: List[int], keyword_list: List[str], genkey: KeyGen) -> List[Union[Element, int]]:
    t: Element = Element.random(genkey.pairing, Zr)
    Tjq1 = genkey.g ** t
    Tjq2: Element = Element.one(genkey.pairing, G1)
    for keyword in keyword_list:
        Tjq2 = Tjq2 * genkey.h1(keyword)
    Tjq2 **= t
    Tjq3: Element = Element.one(genkey.pairing, G1)
    for keyword in keyword_list:
        Tjq3 = Tjq3 * genkey.h2(keyword)
    Tjq3 **= t.__ifloordiv__(priv_key)
    return [Tjq1, Tjq2, Tjq3] + index_list


if __name__ == "__main__":
    k = KeyGen(3)
    Tjq = generate_trapdoor(k.priv_keys[0], [1], ["encryption"], k)
    print(Tjq)
