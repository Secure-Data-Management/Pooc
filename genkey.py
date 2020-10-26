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

import hashlib

from crypto.bn256 import *


class KeyGen:
    """ we are using RELIC as the underlying curve gen ( BLS-381 ) we will implement full parameter through charm like later
     when the dependency hell has been fixed read more here: https://petrelic.readthedocs.io/en/latest/petrelic.native.html """

    def __init__(self, n: int):
        # those are the hash function which hash to a G1Element using sha3 256 and 512
        self.h1: Callable[[Union[bytes, bytearray, str]], CurvePoint] = self.get_hash_function(hashlib.sha3_256)
        self.h2: Callable[[Union[bytes, bytearray, str]], CurvePoint] = self.get_hash_function(hashlib.sha3_512)
        # this is the element e (not sure tho)
        self.e: Callable[[CurveTwist, CurvePoint], gfp_12] = lambda e1, e2: optimal_ate(e1, e2)
        self.pub_keys: List[CurvePoint] = []
        self.keys: List[Tuple[int, CurvePoint]] = []
        self.priv_keys: List[int] = []
        self.g:CurvePoint = curve_G
        for _ in range(n):
            sk = rand_elem()
            pk = self.g.scalar_mul(sk)
            self.keys.append((sk, pk))
            self.pub_keys.append(pk)
            self.priv_keys.append(sk)
            print(pk,type(pk))
    def get_hash_function(self, hash_function: Callable[[Union[bytes, bytearray]], Any]) -> Callable[[Union[bytes, bytearray, str]], CurvePoint]:
        return lambda text: g1_hash_to_point(hash_function(text).digest()) if isinstance(text, (bytes, bytearray)) else g1_hash_to_point(hash_function(text.encode()).digest())

    @staticmethod
    def test():
        priv, pub = g2_random()
        m = b"Some message"
        signature = g1_hash_to_point(m).scalar_mul(priv)
        assert optimal_ate(pub, g1_hash_to_point(m)) == optimal_ate(twist_G, signature)
        print("test passed")

    def __str__(self):
        return f"\n".join([f"keys (s{i},p{i})=({self.keys[i][0]},{self.keys[i][1]})" for i, key in enumerate(self.keys)])


if __name__ == '__main__':
    KeyGen.test()
    print(KeyGen(3))
