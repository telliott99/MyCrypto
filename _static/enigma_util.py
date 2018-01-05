import random
random.seed(1337)

alpha = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
rev =   'ZYXWVUTSRQPONMLKJIHGFEDCBA'

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
    
def rotate_dict(D,n):
    # values are *unique*
    vL = [D[k] for k in alpha]
    vL = vL[n:] + vL[:n]
    rD = dict()
    for k,v in zip(alpha,vL):
        rD[k] = v
    return rD

if __name__ == "__main__":
    seqP = make_pb_seq()
    print seqP
    D = dict(zip(alpha,rev))
    rotate_dict(D,1)
    for k in sorted(D.keys()):
        print k, D[k]
    