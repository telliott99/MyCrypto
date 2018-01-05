import sys

alpha = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
o = int(sys.argv[1]) % 26
msg = ' '.join(sys.argv[2:])

vL = alpha[o:] + alpha[:o]
D = dict(zip(alpha,vL))

pL = list()
for m in msg:
    if m in D:
        pL.append(D[m])
    else:
        pL.append(' ')
        
print ''.join(pL)