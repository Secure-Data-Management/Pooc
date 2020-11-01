from typing import List

from PBC.ECC.element import Element


def optimal_pow_window_size(n: int):
    exp_bits: int = n.bit_length()
    # try to minimize 2 ^ k + n / (k+1).
    if exp_bits > 9065:
        return 8
    elif exp_bits > 3529:
        return 7
    elif exp_bits > 1324:
        return 6
    elif exp_bits > 474:
        return 5
    elif exp_bits > 157:
        return 4
    elif exp_bits > 47:
        return 3
    return 2


def build_pow_window(a: Element, k: int) -> List[Element]:
    if k < 1:
        return []
    # build 2^k lookup table.  lookup[i] = x^i.
    lookup_size: int = 1 << k
    lookup: List[Element] = [element_init(a.field)]
    for i in range(1, lookup_size):
        lookup.append(lookup[-1] * a)
    return lookup


class Field:
    def __init__(self, order: int, nqr: Element, name: str):
        self.order = order
        self.nqr: Element = nqr
        self.name: str = name
        self.elements = []

    def init(self, e: Element):
        self.elements.append(e)


def element_init(f: Field) -> Element:
    e: Element = Element(f, None)
    f.init(e)
    return e
