import sys, random
import enigma_util as ut

alpha = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'

# rotors
seqA =  'EKMFLGDQVZNTOWYHXUSPAIBRCJ'
seqB =  'AJDKSIRUXBLHWTMCQGZNPYFVOE'
seqC =  'BDFHJLCPRTXVZNYEIWGAKMUSQO'

# reflector
seqR =  'YRUHQSLDPXNGOKMIEBFZCWVJAT'

# plugboard
seqP =  ut.make_pb_seq()
      # 'OWUREZGPYLKJMQAHNDVTCSBXIF'
      # 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'

class sub_cipher:
    def __init__(self,name,seq):
        self.name = name
        self.seq = seq
        self.reset()
    
    def reset(self):
        self.fD = dict(zip(alpha,self.seq))
        self.rD = ut.reverse_dict(self.fD)
        self.i = 0
    
    def printable_repr(self,d='fwd'):
        if d == 'fwd':
            D = self.fD
        else:
            D = self.rD
        s = self.name + ': '
        s += ut.dict_to_string(D)
        return s
    
    def rotate(self,n=1):
        D = ut.rotate_dict(self.fD,n)
        self.fD = D
        self.rD = ut.reverse_dict(self.fD)
        self.i += n
        if self.i > 25:
            self.i -= 25

def init_components():
    pb = sub_cipher('pb', seqP)
    # order is pb.III.II.I.refl.I.II.III.pb
    # physical order is refl.I.II.III.pb <- input
    left = sub_cipher('r1', seqA)
    mid = sub_cipher('r2', seqB)
    right = sub_cipher('r3', seqC)
    grp = [right,mid,left]
    re = sub_cipher('re', seqR)
    return pb,grp,re

def do_sub(c,pb,rgroup,re,v=False):
    rL = [c]
    # fD is forward
    c = pb.fD[c];  rL.append(c)
    for g in rgroup:
        c = g.fD[c];  rL.append(c)
    # now reflect
    c = re.fD[c];  rL.append(c)
    # rD is reverse
    for g in rgroup[::-1]:
        c = g.rD[c];  rL.append(c)
    c = pb.rD[c];  rL.append(c)
    if v:  print ' -> '.join(rL)
    return c

# doesn't work properly yet
def rotate_all(grp):
    # rotation in order
    # 0-th rotor turns fastest
    right,mid,left = grp
    MAX = len(alpha) - 1
    if right.i == MAX:
        if mid.i == MAX:
            if left.i == MAX:
                left.rotate()
            mid.rotate()
        right.rotate()

def test():
    for m in alpha:
        do_sub(m,pb,grp,re,v=True)

if __name__ == "__main__":
    #test()
    msg = sys.argv[1]
    print 'input: ', msg
    pb,grp,re = init_components()
    right,mid,left = grp
    
    ctext = list()
    for m in msg:
        c = do_sub(m,pb,grp,re)
        # rotate_all not working
        right.rotate()
        ctext.append(c)
    print 'ctext: ', ''.join(ctext)

    for g in grp:
        g.reset()

    ptext = list()
    for c in ctext:
        p = do_sub(c,pb,grp,re)
        right.rotate()
        ptext.append(p)
    print 'ptext: ', ''.join(ptext)
