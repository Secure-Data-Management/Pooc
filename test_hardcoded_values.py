#!/usr/bin/python3
from genkey import *
from mpeck import mpeck, mdec
import trapdoor


# Lucas


def Test(pub_key: Element, _A: Element, _B: List[Element], _C: List[Element], T: List[Union[int, Element]], j: int, genkey: KeyGen):
    #  S = [A, B, C]

    A = Element(genkey.pairing, G1, value= _A)  # g^r
    B = [Element(genkey.pairing, G1, value= el) for el in _B]  # pk^s
    C = [Element(genkey.pairing, G1, value= el) for el in _C]  # l total crypted keywords (h^r)(f^s)
    for i in range(3):
        T[i] = Element(genkey.pairing, G1, value= T[i])
    I: List[int] = T[3:]  # m indexes of keywords from the query

    # Intermediate computation
    keywords_product: Element = Element.one(genkey.pairing, G1)
    for i in I:
        keywords_product *= C[i]
    E1: Element = genkey.e(T[0], keywords_product)
    G3: Element = genkey.e(A, T[1])
    G2: Element = genkey.e(B[j], T[2])
    E2: Element = G3 * G2
    # Test verification
    if E1 == E2:
        return 1  # keywords match
    else:
        return 0  # keywords don't match


if __name__ == "__main__":
    # Keys generation


    # # mPeck
    # _message = "This is the message"
    # _keywords = ["test", "encryption"]
    # #parameters
    # public_key = k.pub_keys[0]
    # private_key = k.priv_keys[0]
    # k.g = k.g

    # _E, _A, _B, _C = mpeck([public_key], _keywords, k, message=_message)
    # m = mdec(private_key, _E, _B[0], _A, k)
    # # Test

    params = "type a q 5190226450145940880746663486308966347220639714045250223182499121249068575513554544422970314418344770379996438351407014419358038003225732626831022128438331 h 7102594095788614028758769623913839942835962504311385389572759256033849452424444030966227463924769974838212 r 730750818665452757176057050065048642452048576511 exp2 159 exp1 110 sign1 1 sign0 -1 "
    k: KeyGen = KeyGen(1, params)
    str_g = "03138C4D4FFBF34E2338783FF4968933C015AC8F34496A4BE5697D5C4BDE9F78B3E21306F3B4938C40571C9B9EDDE050DB8CE526FF1B8099E8DE790A8962E9443E"
    k.g = Element(k.pairing, G1, value=str_g)



    str_public_key = "0260448EC22BBB4E155F428C4AB548E505D884C179CD1F51DF96320AD1B107F66FCD3E6A9CEE6708B0588A0DC26D27BFDDEBAD5B5AB7F0CC8DF25147EE53AA7C91"
    int_private_key = 0x14AD40DADBD5DD842C3D740F8C5FD91BEDD60C55
    el_private_key = Element(k.pairing, Zr, value=int_private_key)
    el_public_key = Element(k.pairing, G1, value=str_public_key)

    _message = "This is the message."
    _keywords = ["test"]
    int_s = 0x1CF57D847CE6B7F5565B8E578A954513877DCAD0
    int_r = 0x61D70D8B9F955B27A593E7E6E2FDCB718BD2088F
    _E, _A, _B, _C = mpeck([el_public_key], _keywords, k, random_r=int_r, random_s=int_s, message=_message)

    # m = mdec(el_private_key, _E, _B[0], _A, k)

    print("A = ", _A)
    print("B = ", _B)
    print("C = ", _C)





    # TRAPDOOR
    # t = random element in trapdoor computation
    int_t = 0x624FD59064FD58C5E0D818B21CA0435FABB66539
    el_t = Element(k.pairing, Zr, value=int_t)

    T = trapdoor.generate_trapdoor(el_private_key, [0], _keywords, k, el_t)

    # print("TRAPDOOR = ", T)

    ## TEST
    # str_A = "0335E9C8E48AA50024F1F8B319FB34BD8254E6E755E4E80F1B39C02CC241957EF2BED0729E9A9A4402E8902689E49853444D82D6D8DE03DF4DD4A862458DFF052C"
    # str_B = ["0216A91D34134329A9FCD1FF8A488384A43306D4430CDF256E09F062A03082B3E235FED544AAA3D0EBA235F6C565A062032418FC119233031B44506B9861EE05CB"]
    # str_C = ["02205099813ABD5F47E13C21110995C60CB63E050C7FA55CCEE578EF9613FC99E8787912AA9BD206EF86C6EFA04514031D4B723214E6EB8489732F40A8395FBD27"]
    str_A = str(_A)
    str_B = [str(bi) for bi in _B]
    str_C = [str(ci) for ci in _C]
    el_A = Element(k.pairing, G1, value=str_A)
    el_B = [Element(k.pairing, G1, value= el) for el in str_B]  # pk^s
    el_C = [Element(k.pairing, G1, value= el) for el in str_C]  # l total crypted keywords (h^r)(f^s)
    print(Test(el_public_key, el_A, el_B, el_C, T, 0, k))