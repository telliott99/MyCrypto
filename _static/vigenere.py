import sys

alpha = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'

D = dict()
for i,c in enumerate(alpha):
    values = alpha[i:] + alpha[:i]
    eD = dict(zip(alpha,values))
    D[c] = eD
    
def pretty_repr(D):
    kL = sorted(D.keys())
    k_str = ''.join(kL)
    vL = [D[k] for k in kL]
    v_str = ''.join(vL)
    return k_str,v_str

def vigenere_generator(key):
    L = [D[c] for c in key]
    i = 0
    while True:
        yield L[i]
        i += 1
        if i == len(L):
            i = 0

def test():
    for c in alpha:
        eD = D[c]
        ks,vs = pretty_repr(eD)
        print c, ':', vs

def encrypt(msg,key):
    gen = vigenere_generator(key)
    rL = list()
    for m in msg:
        eD = gen.next()
        c = eD[m]
        rL.append(c)
    return ''.join(rL)

def decrypt(ctext,key):
    gen = vigenere_generator(key)
    rL = list()
    for c in ctext:
        eD = gen.next()
        for p in eD:
            if eD[p] == c:
                break 
        rL.append(p)
    return ''.join(rL)

if len(sys.argv) == 1:
    test()
    sys.exit()

msg = sys.argv[1]
key = "WHITE"
ctext = encrypt(msg,key)
print ctext
ptext = decrypt(ctext,key)
print ptext



        