import sys, random
import enigma_util as ut

alpha = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
seqA =  'EKMFLGDQVZNTOWYHXUSPAIBRCJ'
seqB =  'AJDKSIRUXBLHWTMCQGZNPYFVOE'
seqC =  'BDFHJLCPRTXVZNYEIWGAKMUSQO'
seqR =  'YRUHQSLDPXNGOKMIEBFZCWVJAT'

      # 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
      # 'OWUREZGPYLKJMQAHNDVTCSBXIF'
seqP =  ut.make_pb_seq()

class sub_cipher:
    def __init__(self,name,seq):
        self.seq = seq
        self.fD = dict(zip(alpha,seq))
        self.rD = ut.reverse_dict(self.fD)
    
    def printable_repr(self,d='fwd'):
        if d == 'fwd':
            D = self.fD
        else:
            D = self.rD
        s = self.name + ': '
        s += ut.dict_to_string(D)
        return s

pb = sub_cipher('pb', seqP)
r1 = sub_cipher('r1', seqA)
r2 = sub_cipher('r2', seqB)
r3 = sub_cipher('r3', seqC)
re = sub_cipher('re', seqR)

# order is pb.III.II.I.refl.I.II.III.pb

def do_sub(c,pb,rgroup,re):
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
    print ' -> '.join(rL)
    return c
    
rgroup = [r3,r2,r1]

def test():
    for m in alpha:
        do_sub(m,pb,rgroup,re)

test()