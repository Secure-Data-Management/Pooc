#!/usr/bin/python3
# - KeyGen(1k): Given the a security parameter 1k, it returns params = (G1, G2,
# eˆ, H1(·), H2(·), g) where H1:{0, 1}log w → G1 and H2:{0, 1}log w → G1 are
# two different collision-resistance hash functions and g is a generator of G1.
# It chooses n random values x1,...,xn in Z∗
# p and computes yi = gxi . The
# public/private key pairs (pk1, sk1),...,(pkn, skn) are given by
# (pki, ski)=(yi, xi).
# Erwan

from typing import Union, Tuple, List, Callable, Any

from petrelic.bn import Bn
# we are using multiplicative so we use  multiplicative for GT,G1 and G2
from petrelic.multiplicative.pairing import G1, G2, GT, G1Element, G2Element
import hashlib


class KeyGen:
    """ we are using RELIC as the underlying curve gen ( BLS-381 ) we will implement full parameter through charm like later
     when the dependency hell has been fixed read more here: https://petrelic.readthedocs.io/en/latest/petrelic.native.html """

    def __init__(self, n: int):
        # those are the generators we will not use them
        self.g1: G1Element = G1.generator()
        self.g2: G2Element = G2.generator()

        # those are the hash function which hash to a G1Element using sha3 256 and 512
        self.h1: Callable[[Union[bytes, bytearray, str]], G1Element] = self.get_hash_function(hashlib.sha3_256)
        self.h2: Callable[[Union[bytes, bytearray, str]], G1Element] = self.get_hash_function(hashlib.sha3_512)
        # this is the element e (not sure tho)
        self.e: Callable[[G1Element, G1Element], G2Element] = lambda e1, e2: e1.pair(e2)
        self.g: G1Element = G1.order().random()
        self.keys: List[Tuple[Bn, Bn]] = []
        for _ in range(n):
            sk = GT.order().random()  # hoping this is the actual field Zp, seems weird tbh
            pk = G1.generator() ** sk
            self.keys.append((sk, pk))

    def get_hash_function(self, hash_function: Callable[[Union[bytes, bytearray]], Any]) -> Callable[[Union[bytes, bytearray, str]], G1Element]:
        return lambda text: G1.hash_to_point(hash_function(text).digest()) if isinstance(text, (bytes, bytearray)) else G1.hash_to_point(hash_function.update(text.encode()).digest())

    @staticmethod
    def test():
        sk = G1.order().random()
        pk = G2.generator() ** sk
        m = b"Some message"
        signature = G1.hash_to_point(m) ** sk
        assert signature.pair(G2.generator()) == G1.hash_to_point(m).pair(pk)
        print("test passed")

    def __str__(self):
        return "\n".join([f"keys (s{i},p{i})=({self.keys[i][0]},{self.keys[i][1]})" for i, key in enumerate(self.keys)])


if __name__ == '__main__':
    KeyGen.test()
    print(KeyGen(3))
