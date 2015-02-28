FH = open('p.txt')
ptext = FH.read()
FH.close()
pL = [ord(v) for v in ptext]

FH = open('kf','rb')
key = FH.read()
FH.close()
kL = [ord(v) for v in key]

cL = [p ^ k for p,k in zip(pL,kL)]
c = bytearray(cL)

FH = open('c','wb')
FH.write(c)
FH.close()