import random
random.seed(1337)

alpha = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'

def make_pb_seq():
    L = range(len(alpha))
    pL = list(alpha)
    random.shuffle(L)
    for i in range(10):
        j = L.pop()
        k = L.pop()
        pL[j],pL[k] = pL[k],pL[j]
    return ''.join(pL)

def reverse_dict(D):
    rD = dict()
    for k in D:
        v = D[k]
        rD[v] = k
    return rD

def dict_to_string(D):
    L = [D[k] for k in alpha]
    return ''.join(L)

if __name__ == "__main__":
    seqP = make_pb_seq()
    print seqP