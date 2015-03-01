import random, sys
random.seed(137)

class rotor:
    # manipulate lists of ints 0..25
    # rather than alphabet or dictionaries
    
    def __init__(self,s,i=0):
        self.L = [alpha.index(c) for c in s]
        self.current = i
    
    def fwd(self,i):
        return self.L[i]
    
    def rev(self,i):
        assert i in self.L
        for j,k in enumerate(self.L):
            if i == k:
                return j

    def rotate_fwd(self):
        self.L = self.L[1:] + self.L[:1]
        self.current += 1
        if self.current == 26:
            self.current = 0

    def rotate_rev(self):
        self.L = self.L[-1:] + self.L[:-1]
        self.current -= 1
        if self.current == -1:
            self.current = 25

class plugboard:
    def __init__(self):
        def swap(L,i,j):
            tmp = L[i]
            L[i] = L[j]
            L[j] = tmp
            return tmp
        iL = range(len(alpha))
        sL = iL[:]
        random.shuffle(sL)
        for i in range(0,10,2):
            swap(iL,sL[i],sL[i+1])
        self.L = iL[:]
    
    def fwd(self,i):
        return self.L[i]
    
    def rev(self,i):
        for j,k in enumerate(self.L):
            if i == k:
                return j

def pprint(t,L):
    L = [alpha[i] for i in L]
    print t, ' '.join(L)

def printall_fwd(pb,r1,r2,r3):
    print '   ' + ' '.join(list(alpha))
    pprint('pb',pb.L)
    pprint('r1',r1.L)
    pprint('r2',r2.L)
    pprint('r3',r3.L)
    print

def printall_rev(pb,r1,r2,r3):
    pprint('r3',r3.L)
    pprint('r2',r2.L)
    pprint('r1',r1.L)
    pprint('pb',pb.L)
    print '   ' + ' '.join(list(alpha))
    print

def rotate_all_fwd(r1,r2,r3):
    r1.rotate_fwd()
    if r1.current == 0:
        if r2.current == 25:
            r2.rotate_fwd()
            if r3.current == 25:
                r3.rotate_fwd()

def rotate_all_rev(r1,r2,r3):
    if r1.current == 0 and r2.current == 0:
        if r3.current == 0:
            r3.rotate_rev()
        r2.rotate_rev()
    r1.rotate_rev()
    
def encode(c, pb, r1, r2, r3,v=False):
    if v:  print 'encode: ', c, '\n'
    if v:  printall_fwd(pb,r1,r2,r3)
    i = alpha.index(c)
    w = pb.fwd(i)
    x = r1.fwd(w)
    y = r2.fwd(x)
    z = r3.fwd(y)
    if v:  
        for j in [i,w,x,y,z]:
            print alpha[j],
    if v:  print '...','\n'
    rotate_all_fwd(r1,r2,r3)
    
    if v:  printall_rev(pb,r1,r2,r3)
    y = r3.rev(z)
    x = r2.rev(y)
    w = r1.rev(x)
    i = pb.rev(w)
    if v:  
        for j in [z,y,x,w,i]:
            print alpha[j],
    if v:  print '=', alpha[i]
    if v:  print
    rotate_all_fwd(r1,r2,r3)
    
    if v:  print '-'*60
    return alpha[i]

def decode(c, pb, r1, r2, r3,v=False):
    if v:  print 'decode: ', c, '\n'
    if v:  printall_fwd(pb,r1,r2,r3)
    i = alpha.index(c)
    w = pb.fwd(i)
    x = r1.fwd(w)
    y = r2.fwd(x)
    z = r3.fwd(y)
    if v:  
        for j in [i,w,x,y,z]:
            print alpha[j],
    if v:  print '...','\n'
    rotate_all_rev(r1,r2,r3)
    
    if v:  printall_rev(pb,r1,r2,r3)
    y = r3.rev(z)
    x = r2.rev(y)
    w = r1.rev(x)
    i = pb.rev(w)
    if v:  
        for j in [z,y,x,w,i]:
            print alpha[j],
    if v:  print
    rotate_all_rev(r1,r2,r3)
    if v:  print '-'*60
    return alpha[i]
    
# when decoding,
# rotors need to be set to correct indexes!

def pre_set_rotors(MSG_LEN):
    n = MSG_LEN % 26 - 1
    r1 = rotor(s1,i=n)
    r1.L = r1.L[n:] + r1.L[:n]
    
    n = (MSG_LEN/26) % 26 - 1
    r2 = rotor(s2,i=n)
    r2.L = r2.L[n:] + r2.L[:n]
    
    n = (MSG_LEN / (26*26)) - 1
    r3 = rotor(s3,i=n)
    r3.L = r3.L[n:] + r3.L[:n]
    return r1,r2,r3


alpha = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
s1 =    'EKMFLGDQVZNTOWYHXUSPAIBRCJ'
s2 =    'AJDKSIRUXBLHWTMCQGZNPYFVOE'
s3 =    'BDFHJLCPRTXVZNYEIWGAKMUSQO'

msg = 'ATTACK'
if len(sys.argv) > 1:
    msg += 'ATDAWNIFYOUDAREYOUIDIOTS'
print 'msg:   \n', msg

pb = plugboard()
r1 = rotor(s1)
r2 = rotor(s2)
r3 = rotor(s3)

ctext = list()
for c in msg:
    ctext.append(encode(c, pb, r1, r2, r3, v=True))
print 'ctext: \n', ''.join(ctext)

MSG_LEN = len(msg)
r1,r2,r3 = pre_set_rotors(MSG_LEN)

ptext = list()
for c in ctext:
    ptext.append(decode(c, pb, r1, r2, r3, v=True))

print 'ptext: \n', ''.join(ptext)


    