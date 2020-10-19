#!/usr/bin/python3
from petrelic.multiplicative.pairing import G1, G2, GT, G1Element, G2Element
from genkey import KeyGen
from mpeck import  mPECK
import trapdoor as trapdoor

# Lucas


def Test(pk, S, T, j):
    A = S[0] # g^r
    B = S[1:n+1] # pk^s
    C = S[n+1:] # l total crypted keywords (h^r)(f^s)
    I = T[3:] # m indexes of keywords from the query

    #Intermediate computation
    keywords_product = 1
    for i in I:
        keywords_product *= C[i]

    #Test verification
    if(params["e"](T[0],keywords_product) == params["e"](A,T[1]) * params["e"](B[j], T[2])):
        return 1 #keywords match
    else:
        return 0 #keywords don't match



if __name__ == "__main__":
    #number of users
    n=3
    #number of keywords
    l=2

    #Keys generation
    k = KeyGen(n)  
    
    #mPeck    
    params = {"G1":G1, "G2":G2, "e":k.e, "H1":k.h1, "H2":k.h2, "g":k.g1}
    pk_list = [key[1] for key in k.keys]
    sk_list = [key[0] for key in k.keys]
    S = mPECK(pk_list, ["test", "encryption"], params, message='This is the message')[1:]

    #trapdoor generation (query from user j)
    # T = trapdoor.generate_trapdoor(sk_list[0], [1,"encryption"], 1, params)
        
    #Test
    #Test(pk_list, S, T, j)



