.. _crypto1b:

######
Set 1b
######

**Set 1 No. 6:  Break repeating-key XOR**

We're given data in a file as base64.  I believed at first that I should remove the Unix newlines in the data

``crypto.py``

.. sourcecode:: python

    def remove_newlines(ifn,ofn):
        data = load_data(ifn)
        data = ''.join(data.split('\n'))
        FH = open(ofn,'w')
        FH.write(data)
        FH.close()
    
.. sourcecode:: bash

    >>> import crypto as ut
    >>> ut.remove_newlines('6.txt', '6m.txt')
    >>>

But that seems to cause a problem.  To decode base64, according to 

https://www.openssl.org/docs/apps/enc.html

(see examples).

.. sourcecode:: bash

    openssl base64 -d -in 6.txt -out 6.bin

where the ``-d`` flag means decode (and ``-e`` encode is the default).

Compare with our previous example above

.. sourcecode:: bash

    openssl enc -base64 -in x
    
I'm not sure yet, but I think the latter is an old format that is still supported.  

The problem with removing the newlines is that when we do that, the decode gives no output.  I am not sure why that should be.

In any case, this works

.. sourcecode:: bash

    > openssl base64 -d -in 6.txt -out 6.bin
    > hexdump -C -n 64 6.bin
    00000000  1d 42 1f 4d 0b 0f 02 1f  4f 13 4e 3c 1a 69 65 1f  |.B.M....O.N<.ie.|
    00000010  49 1c 0e 4e 13 01 0b 07  4e 1b 01 16 45 36 00 1e  |I..N....N...E6..|
    00000020  01 49 64 20 54 1d 1d 43  33 53 4e 65 52 06 00 47  |.Id T..C3SNeR..G|
    00000030  54 1c 0d 45 4d 07 04 0c  53 12 3c 0c 1e 08 49 1a  |T..EM...S.<...I.|
    00000040
    >

but I get no output with ``-in 6m.txt``.  If we look at the input data:

.. sourcecode:: bash

    > hexdump -C -n 80 6.txt
    00000000  48 55 49 66 54 51 73 50  41 68 39 50 45 30 34 38  |HUIfTQsPAh9PE048|
    00000010  47 6d 6c 6c 48 30 6b 63  44 6b 34 54 41 51 73 48  |GmllH0kcDk4TAQsH|
    00000020  54 68 73 42 46 6b 55 32  41 42 34 42 53 57 51 67  |ThsBFkU2AB4BSWQg|
    00000030  56 42 30 64 51 7a 4e 54  54 6d 56 53 0a 42 67 42  |VB0dQzNTTmVS.BgB|
    00000040  48 56 42 77 4e 52 55 30  48 42 41 78 54 45 6a 77  |HVBwNRU0HBAxTEjw|
    00000050
    >

The context of the newline ``0a`` is ``54 6d 56 53 0a 42 67 42 48`` or ``TmVS.BgBH``.  

We can analyze this using ``openssl`` and ``echo``.  The bytes before ``0a`` are:

.. sourcecode:: bash

    > echo "TmVS" | openssl base64 -d | hexdump -C
    00000000  4e 65 52                                          |NeR|
    00000003
    >
    
and following:

.. sourcecode:: bash

    > echo "BgBH" | openssl base64 -d | hexdump -C
    00000000  06 00 47                                          |..G|
    00000003
    >

Comparing this to the output above, we see that ``openssl base64 -d`` gave ``4e 65 52 06 00 47``, i.e. it simply ignored the newline, yet manually deleting the ``0a`` caused an error.

Next, we are advised to write a function ``hamming`` that computes a Hamming distance *between two strings*.  "The Hamming distance is just the number of differing bits."  Two test strings are given that should return ``37``.

    s1 = "this is a test"
    s2 = "wokka wokka!!!"
    
I first was tempted to just get the integer equivalent of each char using ``ord`` and then do XOR:

.. sourcecode:: python

    # for two chars
    def hamming(a,b):
        return ord(c1) ^ ord(c2)

The problem with this is that

    >>> 0 ^ 2
    2
    >>>
    
Even though there is only one bit that differs between ``bin(0)`` and ``bin(2)`` what we get back has the integer value ``2``

    0000 ^ 0010 = 0010 = 2

So here is a modified version:

    >>> bin(2)[2:].count('1')
    1
    >>>

.. sourcecode:: python

    def hamming_chars(c1,c2):
        x = ord(c1) ^ ord(c2)
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

Test:

    >>> import crypto as ut
    >>> ut.test_hamming()
    True
    >>>

At this point, the problem I notice is that we've constructed a function to work on strings, but the data is binary data.  So we make a small modification:

.. sourcecode:: python

    def hamming_bytes(b1,b2):
        x = b1 ^ b2
        return bin(x)[2:].count('1')

And test it:

    >>> ba = bytearray('\xff\x00')
    >>> len(ba)
    2
    >>> hamming_bytes(ba[0],ba[1])
    8
    >>>

That looks like what I want.  Remember that one can also do:

    >>> ba = bytearray([0,2])
    >>> ut.hamming_bytes(ba[0],ba[1])
    1
    >>> ut.hamming_bytes(0,2)
    1
    >>> ut.hamming_bytes(0,15)
    4
    >>>

Paste the code into ``crypto.py``.

Now to deal with the actual problem.  Recall that our binary data is in ``6.bin`` and it looks like this:

.. sourcecode:: bash

    > hexdump -C -n 64 6.bin
    00000000  1d 42 1f 4d 0b 0f 02 1f  4f 13 4e 3c 1a 69 65 1f  |.B.M....O.N<.ie.|
    00000010  49 1c 0e 4e 13 01 0b 07  4e 1b 01 16 45 36 00 1e  |I..N....N...E6..|
    00000020  01 49 64 20 54 1d 1d 43  33 53 4e 65 52 06 00 47  |.Id T..C3SNeR..G|
    00000030  54 1c 0d 45 4d 07 04 0c  53 12 3c 0c 1e 08 49 1a  |T..EM...S.<...I.|
    00000040
    >

So the first byte is ``1d``.  Its integer equivalent is 16 + 13 = 29.

    >>> import crypto as ut
    >>> 
    >>> FH = open('6.bin','rb')
    >>> data = bytearray(FH.read())
    >>> FH.close()
    >>> data = [int(b) for b in data]
    >>> print data[:5]
    [29, 66, 31, 77, 11]
    >>>

Looks good to me.  Put that into ``crypto.py``

.. sourcecode:: python

    def load_binary_data(fn):
        FH = open(fn,'rb')
        data = bytearray(FH.read())
        FH.close()
        return [int(b) for b in data]


We are told that we should break the encryption in two steps.  Step 1 is to find the size of the repeating key.  To test a given ``KEYSIZE`` we break the data into chunks of that length and then compute the Hamming distance (normalized to the chunk size).  The correct ``KEYSIZE`` should give a minimum average distance.

.. sourcecode:: python

    import crypto as ut
    data = ut.load_binary_data('6.bin')
    f = ut.hamming_bytes
    rL = list()

    for SZ in range(2,101):
        sL = list()
        for i in range(10):
            beg = i*SZ
            mid = beg + SZ
            end = beg + 2*SZ
            s1 = data[beg:mid]
            s2 = data[mid:end]
            score = ut.hamming(f,s1,s2)
            sL.append(score*1.0/SZ)
        rL.append((ut.mean(sL), SZ))

    rL.sort()
    for line in rL[:5]:
        print line

.. sourcecode:: bash

    > python script.py 
    (2.7586206896551717, 29)
    (2.804597701149425, 87)
    (2.84, 5)
    (2.889655172413793, 58)
    (2.986666666666667, 15)
    (3.1032258064516127, 31)
    (3.122222222222222, 9)
    (3.125, 8)
    (3.1333333333333333, 3)
    (3.1388888888888884, 18)
    >

Naively I would expect that multiples of ``KEYSIZE`` will also have low distances, and ``58`` and ``87`` are multiples of ``29``, so that is my best guess, at least to begin with.

Step 2 is then to break up the data into ``KEYSIZE`` bins, and find the key to each bin, using the method introduced in #3.  

``crypto.py``:

.. sourcecode:: python

    def make_ragged_array(iL,N):
        data = iL[:]
        L = list()
        for i in range(N):
            L.append([])
        i = 0
        while data:
            if i == SZ:
                i = 0
            L[i].append(data.pop(0))
            i += 1
        return L

.. sourcecode:: bash

    >>> import crypto as ut
    >>> s = ut.load_binary_data('6.bin')
    >>> SZ = 29 
    >>> L = ut.make_ragged_array(s,SZ)
    >>> print len(L), len(L[0]), len(L[-1])
    29 100 99
    >>>

``script.py``:

.. sourcecode:: python

    import crypto as ut

    s = ut.load_binary_data('6.bin')
    SZ = 29

    def get_key_list():
        # collect into SZ bins
        L = ut.make_ragged_array(s,SZ)

        kL = list()
        for i in range(SZ):
            data = L[i]
            rL = ut.test_all_keys(data,n=5)
            k = rL[0][1]
            kL.append(k)
        return kL

    def decode(kL):
        pL = list()
        for i,b in enumerate(s):
            j = i % SZ
            k = kL[j]
            p = k ^ b
            pL.append(chr(p))
        return pL

    kL = get_key_list()
    #kL[3] = 109

    print kL[:10]
    print kL[10:20]
    print kL[20:]
    print
    pL = decode(kL)
    print ''.join(pL)[:300]

.. sourcecode:: bash

    > python script.py 
    [84, 101, 114, 40, 105, 110, 97, 116, 111, 114]
    [32, 88, 58, 32, 66, 114, 105, 110, 103, 32]
    [116, 104, 101, 32, 110, 111, 105, 115, 101]

    I'meback and I'm ringin' the bel) 
    A rockin' on the mike whil  the fly girls yell 
    In ecst$sy in the back of me 
    Well t-at's my DJ Deshay cuttin' al) them Z's 
    Hittin' hard and 1he girlies goin' crazy 
    Vani)la's on the mike, man I'm no1 lazy. 

    I'm lettin' my drugekick in 
    It controls my mout- and I
    >
    
Well, all right!  Just one little problem.  That 4th character should be a space.  The 4th byte of data is

.. sourcecode:: bash

    > hexdump -C -n 16 6.bin 
    00000000  1d 42 1f 4d 0b 0f 02 1f  4f 13 4e 3c 1a 69 65 1f  |.B.M....O.N<.ie.|
    00000010
    >

``4d`` or ``M`` or ``77``.  The 4th byte of the key is 40.  

    >>> ord("M")
    77
    >>> chr(40 ^ 77)
    'e'
    >>>
    
That ``'e'`` should be a space, ``32`` as an integer.  So the 4th byte of the key should be:

    >>> 77 ^ 32 = 109
    
Insert a line to modify the key list:  ``kL[3] = 109``.  then we get:

    > python script.py 
    [84, 101, 114, 109, 105, 110, 97, 116, 111, 114]
    [32, 88, 58, 32, 66, 114, 105, 110, 103, 32]
    [116, 104, 101, 32, 110, 111, 105, 115, 101]

    I'm back and I'm ringin' the bell 
    A rockin' on the mike while the fly girls yell 
    In ecstasy in the back of me 
    Well that's my DJ Deshay cuttin' all them Z's 
    Hittin' hard and the girlies goin' crazy 
    Vanilla's on the mike, man I'm not lazy. 

    I'm lettin' my drug kick in 
    It controls my mouth and I
    >

I'm not going to print the whole thing here, but we did it!

=====================================================

**Set 1 No. 7:  AES in ECB mode**

The file ``7.txt`` is base64-encoded data.  It has been encrypted via AES-128 in ECB mode with the key ``YELLOW SUBMARINE``.  Decrypt the data.

pip install pycrypto

The code:

from Crypto.Cipher import AES
from Crypto import Random
k = b'YELLOW SUBMARINE'
cipher = AES.new(k, AES.MODE_ECB)

In the interpreter:

    >>> from Crypto.Cipher import AES
    >>> from Crypto import Random
    >>> k = b'YELLOW SUBMARINE'
    >>> iv = Random.new().read(AES.block_size)
    >>> cipher = AES.new(k, AES.MODE_ECB, iv)
    >>> msg = cipher.encrypt(b'Attack at dawn..')
    >>> 
    >>> msg
    '\xb8r\x9b\x02b\xa0\x12ky\xe4:+\xe6\x86p\xcf'
    >>> ba = bytearray(msg)
    >>> L = [int(b) for b in ba]
    >>> L[:8]
    [184, 114, 155, 2, 98, 160, 18, 107]
    >>>

Step 1 is to generate the binary data:

.. sourcecode:: bash

    > openssl enc -base64 -d -in 7.txt -out 7.bin
    > hexdump -C -n 64 7.bin
    00000000  09 12 30 aa de 3e b3 30  db aa 43 58 f8 8d 2a 6c  |..0..>.0..CX..*l|
    00000010  37 b7 2d 0c f4 c2 2c 34  4a ec 41 42 d0 0c e5 30  |7.-...,4J.AB...0|
    00000020  dd 31 b8 c2 30 3f ef 7a  75 03 5b d0 4b 3c 45 ce  |.1..0?.zu.[.K<E.|
    00000030  0d b9 3a 6b 8f 28 31 b0  18 e8 30 d9 b2 e2 db 73  |..:k.(1...0....s|
    00000040
    >
    
Then, in Python, we load the data:

    >>> import crypto as ut
    >>> data = ut.load_binary_data('7.bin')
    >>> data[:8]
    [9, 18, 48, 170, 222, 62, 179, 48]
    >>>
    
And then we try:

    >>> from Crypto.Cipher import AES
    >>> from Crypto import Random
    >>> k = b'YELLOW SUBMARINE'
    >>> cipher = AES.new(k, AES.MODE_ECB)
    >>> p = cipher.decrypt(str(bytearray(data)))
    >>> FH = open('out','w')
    >>> FH.write(p)
    >>> FH.close()
    >>> 
    [2]+  Stopped                 python
    > cat out
    I'm back and I'm ringin' the bell 
    A rockin' on the mike while the fly girls yell 
    In ecstasy in the back of me 
    Well that's my DJ Deshay cuttin' all them Z's 
    Hittin' hard and the girlies goin' crazy 
    Vanilla's on the mike, man I'm not lazy. 
    ..

Looks familiar.  So the question is, what does ``str(bytearray(data))`` do?

    >>> ba = bytearray('\x00CAt')
    >>> ba
    bytearray(b'\x00CAt')
    >>> str(ba)
    '\x00CAt'
    >>>

OK.  Not the same as print, that's for sure.

=====================================================

**Set 1 No. 8:  Detect AES in ECB mode**

Identify a ciphertext that has been encoded with ECB based on this:

    Remember that the problem with ECB is that it is stateless and deterministic; the same 16 byte plaintext block will always produce the same 16 byte ciphertext.
    
So I will just slide through each one looking for repeated 16-byte blocks.  First, code to break up into "chunks":

``crypto.py``:

.. sourcecode:: python

    def chunks(s,SZ=16):
        rL = list()
        while s:
            rL.append(s[:SZ])
            s = s[SZ:]
        return rL

``script.py``:

.. sourcecode:: python

    import crypto as ut
    data = ut.load_data('8.txt')
    data = data.strip().split('\n')

    for i,line in enumerate(data):
        line = line.strip()
        L = ut.chunks(line)
        if len(L) != len(set(L)):
            for e in L:
                print e, L.count(e)
            print i
        

.. sourcecode:: bash

    > python script.py 
    d880619740a8a19b 1
    7840a8a31c810a3d 1
    08649af70dc06f4f 4
    d5d2d69c744cd283 4
    e2dd052f6b641dbf 1
    9d11b0348542bb57 1
    08649af70dc06f4f 4
    d5d2d69c744cd283 4
    9475c9dfdbc1d465 1
    97949d9c7e82bf5a 1
    08649af70dc06f4f 4
    d5d2d69c744cd283 4
    97a93eab8d6aecd5 1
    66489154789a6b03 1
    08649af70dc06f4f 4
    d5d2d69c744cd283 4
    d403180c98c8f6db 1
    1f2a3f9c4040deb0 1
    ab51b29933f2c123 1
    c58386b06fba186a 1
    132
    >

Looks like a good candidate!
