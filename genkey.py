#!/usr/bin/python3
from typing import Union, Tuple, List, Callable, Any
from pypbc import *
import hashlib

class KeyGen:
    def __init__(self, n: int):
        self.params: Parameters = Parameters(qbits=512, rbits=160)
        self.pairing: Pairing = Pairing(self.params)
        self.h1: Callable[[Union[bytes, bytearray, str]], Element] = self.get_hash_function(self.pairing, hashlib.sha3_256)
        self.h2: Callable[[Union[bytes, bytearray, str]], Element] = self.get_hash_function(self.pairing, hashlib.sha3_512)
        self.e: Callable[[Element, Element], Element] = lambda e1, e2: self.pairing.apply(e1, e2)
        self.pub_keys: List[Element] = []
        self.keys: List[Tuple[Element, Element]] = []
        self.priv_keys: List[Element] = []
        self.g = Element.random(self.pairing, G1)
        for _ in range(n):
            sk: Element = Element.random(self.pairing, Zr)
            pk: Element = Element(self.pairing, G1, value=self.g ** sk)
            self.keys.append((sk, pk))
            self.pub_keys.append(pk)
            self.priv_keys.append(sk)

    def get_hash_function(self, pairing, hash_function: Callable[[Union[bytes, bytearray]], Any]) -> Callable[[Union[bytes, bytearray, str]], Element]:
        return lambda text: Element.from_hash(pairing, G1, hash_function(text).digest()) if isinstance(text, (bytes, bytearray)) else \
            Element.from_hash(pairing, G1, hash_function(text.encode()).digest())

    def __str__(self):
        return f"\n".join([f"keys (s{i},p{i})=({self.keys[i][0]},{self.keys[i][1]})" for i, key in enumerate(self.keys)])


if __name__ == '__main__':
    print(KeyGen(3))
