#!/usr/bin/python3

# Irene
from petrelic.multiplicative.pairing import GT, G1, G2
from genkey import KeyGen


# Hash functions as defined by KeyGen
def random_in_zp():
    rand = GT.order().random()
    return rand


def generate_trapdoor(skj, Q, m, params):
    liste_I = Q[0:m] # list of indexes to denote the location of wIj
    liste_w = Q[m:]  # list of keywords for the cunjunctive search

    # select a random value t in Zp*
    t = random_in_zp()

    # Tjq1 = g ** t ; g the generator of G1 as defined in KeyGen
    g = params['g']
    Tjq1 = g ** t

    # Tjq2 = (hI1... hIm)**t where hIj = h1(wIj)
    Tjq2 = 1
    for element in liste_w:
        Tjq2 = Tjq2 * (params['H1'](element) ** t)

    # Tjq3 = (fI1... fIm)**(t / xj) where fIj = h2(wIj) ; xj computed in KeyGen
    Tjq3 = 1
    for element in liste_w:
        Tjq3 = Tjq3 * (params['H2'](element) ** (t/skj))

    Tjq = [Tjq1, Tjq2, Tjq3] + liste_I
    return Tjq


if __name__ == "__main__":
    k = KeyGen(3)
    params = {"G1":G1, "G2":G2, "e":k.e, "H1":k.h1, "H2":k.h2, "g":k.g1}
    # TODO => Tjq = generate_trapdoor()