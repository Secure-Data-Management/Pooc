from PBC.ECC.field import Field


class AParams:
    def __init__(self, exp2: int, exp1: int, sign1: int, sign0: int, r: int, q: int, h: int):
        self.exp2: int = exp2
        self.exp1: int = exp1
        self.sign1: int = sign1
        self.sign0: int = sign0
        self.r: int = r
        self.q: int = q
        self.h: int = h

class APairingData:
    def __init__(self,Fq:Field,Fq2:Field,Eq:Field,exp2:int,exp1:int,sign1:int):
        self.Fq=Fq
        self.Fq2=Fq2
        self.Eq=Eq
        self.exp2: int = exp2
        self.exp1: int = exp1
        self.sign1: int = sign1