import sys, base64

def hexprint(L):
    L = [ord(b) for b in L]
    L = [hex(i)[2:].zfill(2) for i in L]
    return ' '.join(L)

c = sys.argv[1]
n = len(c)
while len(c) % 4:
    c += '='

print c
bL = base64.b64decode(c)
p = hexprint(bL)
print p
