#!/usr/bin/python3

# Irene

from genkey import *


# Hash functions as defined by KeyGen
def random_in_zp():
    rand = GT.order().random()
    return rand


def generate_trapdoor(priv_key: Element, index_list: List[int], keyword_list: List[str], genkey: KeyGen) -> List[Union[Element, int]]:
    """

    :param genkey:
    :param priv_key:
    :param index_list: list of indexes to denote the location of wIj
    :param keyword_list: list of keywords for the cunjunctive search
    :param params:
    :return:
    """

    # select a random value t in Zp*
    t: Element = Element.random(genkey.pairing, Zr)

    # Tjq1 = g ** t ; g the generator of G1 as defined in KeyGen
    Tjq1 = genkey.g ** t

    # Tjq2 = (hI1... hIm)**t where hIj = h1(wIj)
    Tjq2: Element = Element.one(genkey.pairing, G1)
    for keyword in keyword_list:
        Tjq2 = Tjq2 * genkey.h1(keyword)
    Tjq2 **= t
    # Tjq3 = (fI1... fIm)**(t / xj) where fIj = h2(wIj) ; xj computed in KeyGen
    Tjq3: Element = Element.one(genkey.pairing, G1)
    for keyword in keyword_list:
        Tjq3 = Tjq3 * genkey.h2(keyword)
    Tjq3 **= t.__ifloordiv__(priv_key)

    return [Tjq1, Tjq2, Tjq3] + index_list


if __name__ == "__main__":
    k = KeyGen(3)
    Tjq = generate_trapdoor(k.priv_keys[0], [1], ["encryption"], k)
    print(Tjq)
