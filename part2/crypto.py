import base64

english_char_freqs = '''
a	8.167   b	1.492   c	2.782   d	4.253   e	12.702
f	2.228   g	2.015   h	6.094   i	6.966   j	0.153
k	0.772   l	4.025   m	2.406   n	6.749   o	7.507
p	1.929   q	0.095   r	5.987   s	6.327   t	9.056
u	2.758   v	0.978   w	2.360   x	0.150   y	1.974
z	0.074
'''

def load_data(fn):
    """Return data from file "fn"
    """
    FH = open(fn)
    data = FH.read()
    FH.close()
    return data
    
def load_binary_data(fn):
    """Return data from file "fn"
    as a list of ints
    """
    FH = open(fn,'rb')
    data = bytearray(FH.read())
    FH.close()
    return [int(b) for b in data]
    
def write_hex_bytes(fn,ofn):
    """Input text file "fn" with hex string
    write as bytes to "ofn"
    """
    data = load_data(fn)
    b = bytearray.fromhex(data)
    FH = open(ofn,'wb')
    FH.write(b)
    FH.close()
    
def get_all_hex_bytes():
    dg = "0123456789abcdef"
    return [k1+k2 for k1 in dg for k2 in dg]

def mean(L):
    return 1.0*sum(L)/len(L)

def has_repeated_items(L):
    return len(L) != len(set(L))
    
def bytes_to_hex(src):
    """src can be bytes or a list of ints
    """
    L = [hex(ord(c))[2:] for c in src]
    L = [h.zfill(2) for h in L]
    return ''.join(L)

def remove_newlines(ifn,ofn):
    data = load_data(ifn)
    data = ''.join(data.split('\n'))
    FH = open(ofn,'w')
    FH.write(data)
    FH.close()

def get_english_char_freq_dict():
    data = english_char_freqs.strip().split()
    D = dict()
    while data:
        char, percent = data.pop(0), data.pop(0)
        D[char] = float(percent)
    for k in D.keys():
        u = k.upper()
        D[u] = D[k]
    return D

def score(L,penalty=10):
    """Input L is bytes (as int)
    score w/penalty for non-standard, plus English freqs
    """
    D = get_english_char_freq_dict()
    score = 0
    for i in L:
        if i > 127:
            score -= penalty
        elif i < 32 and not (i == 10 or i == 13):
            score += -5
        else:
            # ignore punctuation
            c = chr(i)
            if c in D:
                score +=(D[c])
    return score*1.0/len(L)

def test_all_keys(data,kL=range(256),n=5):
    rL = list()
    for k in kL:
        L = [k ^ i for i in data]
        sc = score(L)
        # printable repr
        s = ''.join([chr(i) for i in L])
        tmp = [sc,k,s,L]
        rL.append(tmp)
    rL.sort(reverse=True)
    return rL[:n]

def xor_hex_chars(c1,c2):
    """Input two hex characters as strings
    return an integer result from XOR
    """
    x = int(c1,16)
    y = int(c2,16)
    return x ^ y

def hamming_chars(c1,c2):
    return hamming_bytes(ord(c1),ord(c2))
    
def hamming_bytes(b1,b2):
    x = b1 ^ b2
    return bin(x)[2:].count('1')

# pass in a scoring function
def hamming(f,s,t):
    score = 0
    for c1,c2 in zip(s,t):
        score += f(c1,c2)
    return score

def test_hamming():
    s = "this is a test"
    t = "wokka wokka!!!"
    f = hamming_chars
    print hamming (f,s,t) == 37

def make_ragged_array(iL,N):
    data = iL[:]
    L = list()
    for i in range(N):
        L.append([])
    i = 0
    while data:
        if i == N:
            i = 0
        L[i].append(data.pop(0))
        i += 1
    return L

def chunks(s,SZ=16):
    rL = list()
    while s:
        rL.append(s[:SZ])
        s = s[SZ:]
    return rL

def xor_block(ba1,ba2):
    import array
    """Data comes in as bytes, leaves as bytes
    """
    iL1 = [ord(c) for c in ba1]
    iL2 = [ord(c) for c in ba2]
    xL = [x1 ^ x2 for x1,x2 in zip(iL1,iL2)]
    return array.array('B',xL).tostring()

def pad(s,n=8):
    L = ['\x00','\x01','\x02','\x03',
         '\x04','\x05','\x06','\x07',
         '\x08','\x09','\x0a','\x0b',
         '\x0c','\x0d','\x0e','\x0f' ]
    extra = len(s) % n
    if not extra:
        return s
    diff = n - extra
    return bytearray(s) + diff * L[diff]
    
def myCBC_encode(data,key,iv):
    from Crypto.Cipher import AES
    xor = xor_block
    cp = AES.new(key, AES.MODE_ECB)
    
    cL = [iv]
    tL = data[:]
    while tL:
        next = tL.pop(0)
        x = xor(next,cL[-1])
        ct = cp.encrypt(x)
        cL.append(ct)
    return cL[1:]

def myCBC_decode(data,key,iv):
    from Crypto.Cipher import AES
    xor = xor_block
    cp = AES.new(key, AES.MODE_ECB)

    cL = [iv] + data[:]
    rL = list()
    next = cL.pop()  # from the end
    while cL:
        x = cp.decrypt(next)
        pt = xor(x, cL[-1])
        rL.insert(0,pt)
        next = cL.pop()
    return rL

def cbc_detected(ct):
    pL = list()
    for item in chunks(ct,8):
        h = bytes_to_hex(item)
        pL.append(h)
    reps = has_repeated_items(pL)
    return reps
