.. _crypto2a:

######
Set 2a
######

**Set 2 No. 9:  PKCS#7 padding**

http://cryptopals.com/sets/2/challenges/9/

Before we start 2-9 I want to explore Python bytes a little.  We've used both ``"0xff"`` and ``"\xff"`` above.  The first one looks like hex, but it's just a string.  For example

    >>> b = "0xff"
    >>> FH = open('x','wb')
    >>> FH.write(b)
    >>> FH.close()
    >>> 
    >>>

.. sourcecode:: bash

    > hexdump -C x
    00000000  30 78 66 66                                       |0xff|
    00000004
    >
    
With the ``"0xff"`` construct, the 4-byte string was written to file.  On the other hand

    >>> b = "\xff"
    >>> FH = open('x','wb')
    >>> FH.write(b)
    >>> FH.close()
    >>> 
    >>>

.. sourcecode:: bash

    > hexdump -C x
    00000000  ff                                                |.|
    00000001
    >

This time we got the actual byte ``ff``.  The ``hex`` built-in method gives the string, not the byte:

    >>> hex(15)
    '0xf'
    >>> hex(255)
    '0xff'
    >>>

So, in this problem, we want to pad with real bytes.  A problem that comes up is that we can't assemble a byte:

    >>> b = '\x0' + '3'
    ValueError: invalid \x escape
    >>>

Although we could do:

    >>> b = '\xff0' + '3'
    >>> b
    '\xff03'
    >>>

But this is deceptive.  The ``open``, ``write``, ``close`` sequence shows why:

.. sourcecode:: bash

    > hexdump -C x
    00000000  ff 30 33                                          |.03|
    00000003
    >

As does

    >>> len(b)
    3
    >>>

The variable ``b`` prints as ``'\xff03'`` but when we write it to file, we see that it is the byte ``ff`` followed by the byte ``"0"`` (hex ``30`` or int 48), followed by ``"3"`` (hex ``33`` or int 51).

Instead, what we want is  ``b = '\xff\x03'`` and then what we will get is

.. sourcecode:: bash

    > hexdump -C x
    00000000  ff 03                                             |..|
    00000002
    >

So that's important to remember.  We used the ``bytearray.fromhex`` constructor before.  The ``b'\xff\x03'`` construct is a shorthand for this method.

    >>> ba = bytearray.fromhex('ff03')
    >>> ba
    bytearray(b'\xff\x03')
    >>> ba2 = b'\xff\x03'
    >>> ba == ba2
    True
    >>>
    

This gives us an actual array of bytes that writes to file as we expect.

    >>> ba = bytearray.fromhex('eebb')
    >>> for c in ba:
    ...     print c
    ... 
    238
    187
    >>>>>> FH = open('x','wb')
    >>> FH.write(ba)
    >>> FH.close()
    >>>

Implement CB

.. sourcecode:: bash

    > hexdump -C x
    00000000  ee bb                                             |..|
    00000002
    >
    
So, having written all this, how to pad out a variable with a number of bytes of to be determined at run time.  The ``PKCS#7`` approach is to count the number of bytes needed to reach ``8`` or ``16``, and then pad with that number of the same byte.  But we cannot do something like:

    >>> '\x0' + 3
    ValueError: invalid \x escape
    >>>

One way that works, but seems rather inelegant:

L = ['\x00','\x01','\x02','\x03',
     '\x04','\x05','\x06','\x07',
     '\x08','\x09','\x0a','\x0b',
     '\x0c','\x0d','\x0e','\x0f' ]

     >>> L = ['\x00','\x01','\x02','\x03',
     ...      '\x04','\x05','\x06','\x07',
     ...      '\x08','\x09','\x0a','\x0b',
     ...      '\x0c','\x0d','\x0e','\x0f' ]
     >>> 
     >>> L[:8]
     ['\x00', '\x01', '\x02', '\x03', '\x04', '\x05', '\x06', '\x07']
     >>> L[8:]
     ['\x08', '\t', '\n', '\x0b', '\x0c', '\r', '\x0e', '\x0f']
     >>>



     >>> k = "YELLOW SUBMAR"
     >>> diff = 16 - (len(k) % 16)
     >>> diff
     3
     >>> k = bytearray(k) + diff * L[diff]
     >>> k
     bytearray(b'YELLOW SUBMAR\x03\x03\x03')
     >>>

So, here is 

``script.py``:

.. sourcecode:: python

    def pad(s,n=8):
        L = ['\x00','\x01','\x02','\x03',
             '\x04','\x05','\x06','\x07',
             '\x08','\x09','\x0a','\x0b',
             '\x0c','\x0d','\x0e','\x0f' ]
        diff = n - (len(k) % n)
        return bytearray(s) + diff * L[diff]

    k = "YELLOW SUBMARINE"
    n = 20
    print `pad(k,n)`

.. sourcecode:: bash

    > python script.py 
    bytearray(b'YELLOW SUBMARINE\x04\x04\x04\x04')
    >

This will crash if ``diff`` is too large.  But we can predict the needed size. 

=====================================================

**Interlude**

Conversion to and from bytes.  Here are bytes <=> ints:

    >>> bytes = b'\xff\x00CAt!'
    >>> bytes
    '\xff\x00CAt!'
    >>> iL = [ord(c) for c in bytes]
    >>> iL
    [255, 0, 67, 65, 116, 33]
    >>> import array
    >>> array.array('B',iL).tostring()
    '\xff\x00CAt!'
    >>>

That second one comes from Alex Martelli:

http://stackoverflow.com/questions/3470398/list-of-integers-into-string-byte-array-python

For bytes => hex, I would go through ints in the forward direction:
    
    >>> bytes
    '\xff\x00CAt!'
    >>> iL = [ord(c) for c in bytes]
    >>> hL = [hex(i) for i in iL]
    >>> hL
    ['0xff', '0x0', '0x43', '0x41', '0x74', '0x21']
    >>> h = ''.join([c[2:] for c in hL])
    >>> h
    'ff043417421'
    >>>
    
For hex => bytes, the simplest approach is:

    >>> s = "deadbeef"
    >>> s.decode("hex")
    '\xde\xad\xbe\xef'
    >>>

We could use the bytearray method, but we need to take care about the dropping of leading zeros.  Compare:

    >>> h = 'ff0043417421'
    >>> bytearray.fromhex(h)
    bytearray(b'\xff\x00CAt!')
    >>> h = 'ff043417421'
    >>> bytearray.fromhex(h)
    Traceback (most recent call last):
      File "<stdin>", line 1, in <module>
    ValueError: non-hexadecimal number found in fromhex() arg at position 10
    >>>

``fromhex`` is complaining because the number of characters is odd, but the error has come from dropping the leading ``'0'`` on the byte ``'\x00'``.

The way to fix this is ``zfill``, though it's a bit awkward because we must remove the leading ``'0x'``

    >>> h = hex(0)
    >>> h
    '0x0'
    >>> h = '0x' + h[2:].zfill(2)
    >>> h
    '0x00'
    >>> bytearray.fromhex(h)
    Traceback (most recent call last):
      File "<stdin>", line 1, in <module>
    ValueError: non-hexadecimal number found in fromhex() arg at position 0
    >>> bytearray.fromhex(h[2:])
    bytearray(b'\x00')
    >>>
    
Note that ``fromhex`` above doesn't like the ``'0x'``.

    
And of course hex => int is just ``int(h,16)``

    >>> bytes
    '\xff\x00CAt!'
    >>> hL = [hex(ord(c)) for c in bytes]
    >>> hL
    ['0xff', '0x0', '0x43', '0x41', '0x74', '0x21']
    >>> [int(h,16) for h in hL]
    [255, 0, 67, 65, 116, 33]
    >>>


=====================================================

**Set 2 No. 10:  Implement CBC**

http://cryptopals.com/sets/2/challenges/10/

I found two libraries for cryptography for Python.  One is here:

https://cryptography.io/en/latest/

It can be obtained with ``pip install cryptography`` and

    >>> from cryptography.fernet import Fernet
    
The other one is here:

https://pypi.python.org/pypi/pycrypto

I'm not sure how I installed it.  :)  But I have it:

from Crypto.Cipher import AES
from Crypto import Random
random = Random.new()

    >>> from Crypto.Cipher import AES
    >>> from Crypto import Random
    >>> random = Random.new()
    

Basic usage in ECB mode does not use an initialization vector, but we will need this later:

iv = random.read(AES.block_size)
iv

    >>> iv = random.read(AES.block_size)
    >>> iv
    '\xd6\xee\x8c0\xde\x10\x07\xa6\x87\x1d\x82*\x86i\xd8\xf0'
    >>> 
    >>> AES.block_size
    16
    >>>

msg = "Attack at dawn.."
key = b'YELLOW SUBMARINE'
cp = AES.new(key, AES.MODE_ECB)
ct = cp.encrypt(msg)
ct

    >>> 
    >>> key = b'YELLOW SUBMARINE'
    >>> 
    >>> cp = AES.new(key, AES.MODE_ECB)
    >>> 
    >>> ct = cp.encrypt(msg)
    >>> ct
    'J\x0f\xe7\x11x\xb5\x04\xad$<\xf5\xdd}\x16\xeb\xf8'
    >>>


p = cp.decrypt(ct)
print p

    >>> p = cp.decrypt(ct)
    >>> print p
    Attack at dawn..
    >>>

All we need is the key.  And it's deterministic.  If we make a new instance

    >>> cp2 = AES.new(key, AES.MODE_ECB)
    >>> cp2.encrypt(msg)
    'J\x0f\xe7\x11x\xb5\x04\xad$<\xf5\xdd}\x16\xeb\xf8'
    >>>
    
The ciphertext is the same.  My original example had the initialization vector:

    >>> cp = AES.new(k, AES.MODE_ECB, iv)

But it is neither required nor used for the encryption.

For CBC mode, we use a single key as in ECB, and encrypt the message in blocks of 16 bytes.  The trick is to XOR the message block and the iv for the first step before encrypting, then XOR the message block and the previous ciphertext for each subsequent round.

Here is a new function to put in ``crypto.py``:

    def xor_block(ba1,ba2):
        """Data comes in as bytes, leaves as bytes
        """
        iL1 = [ord(c) for c in ba1]
        iL2 = [ord(c) for c in ba2]
        xL = [x1 ^ x2 for x1,x2 in zip(iL1,iL2)]
        return array.array('B',xL).tostring()

``script.py``:

.. sourcecode:: python

    import crypto as ut
    xor = ut.xor_block

    msg = b'Attack at dawn..'
    key = b'YELLOW SUBMARINE'

    ba = xor(msg,key)
    print `ba`

    print `xor(key,ba)`
    print `xor(msg,ba)`

.. sourcecode:: bash

    > python script.py 
    "\x1818-,<\x002!b) %'`k"
    'Attack at dawn..'
    'YELLOW SUBMARINE'
    >


XOR msg block + iv for first step
then encrypt against key

Recall:

``crypto.py``:

.. sourcecode:: python

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
    
    def xor_block(ba1,ba2):
        import array
        """Data comes in as bytes, leaves as bytes
        """
        iL1 = [ord(c) for c in ba1]
        iL2 = [ord(c) for c in ba2]
        xL = [x1 ^ x2 for x1,x2 in zip(iL1,iL2)]
        return array.array('B',xL).tostring()
    
    def myCBC_encode(data,key,iv):
        """Data comes in as bytes, leaves as bytes
        """
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
    
    
``script.py``:

.. sourcecode:: bash

    import crypto as ut
    from Crypto.Cipher import AES

    key = b'YELLOW SUBMARINE'
    msg = b'Attack at dawn, await my signal'
    msg = ut.pad(msg,n=16)

    iv = b'\x00\x01'*8
    cL = [iv]
    L = ut.chunks(msg)

    # chunks converts to bytearray
    L = [str(ch) for ch in L]
    for e in L:
        print `e`
    #========================================

    ct = ut.myCBC_encode(L,key,iv)
    ct = ''.join(ct)
    print `ct`

    cp2 = AES.new(key, AES.MODE_CBC, iv)
    ct2 = cp2.encrypt(str(msg))
    print `ct2`
    
    

    > python script.py 
    'Attack at dawn, '
    'await my signal\x01'
    'k\xbd.\x8d[o\x01d\x98\x0fc\x11,\xbb;\xf5\x1a\x94J\xe1;\n0t\x16oai\xbbE\xedI'
    'k\xbd.\x8d[o\x01d\x98\x0fc\x11,\xbb;\xf5\x1a\x94J\xe1;\n0t\x16oai\xbbE\xedI'
    >

Looks like we have implemented CBC mode for encryption!

How about decryption?  We will start with the last block, decrypt in ECB mode, and then?  What to XOR with?  With the previous block!  For the first block, XOR with the initialization vector ``iv``.

.. sourcecode:: python

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

and add this to ``script.py``:

.. sourcecode:: python

    L = ut.chunks(ct)
    L = [str(ch) for ch in L]
    
    pt = ut.myCBC_decode(L,key,iv)
    print ''.join(pt)
    
and now we get:

.. sourcecode:: bash

    > python script.py 
    'Attack at dawn, '
    'await my signal\x01'
    'k\xbd.\x8d[o\x01d\x98\x0fc\x11,\xbb;\xf5\x1a\x94J\xe1;\n0t\x16oai\xbbE\xedI'
    'k\xbd.\x8d[o\x01d\x98\x0fc\x11,\xbb;\xf5\x1a\x94J\xe1;\n0t\x16oai\xbbE\xedI'
    Attack at dawn, await my signal
    >

For the actual problem, convert the data to a binary file:

.. sourcecode:: bash

    > openssl enc -base64 -d -in 10.txt -out 10.bin
    > hexdump -C -n 32 10.bin
    00000000  09 12 30 aa de 3e b3 30  db aa 43 58 f8 8d 2a 6c  |..0..>.0..CX..*l|
    00000010  d5 cf 83 55 cb 68 23 39  7a d4 39 06 df 43 44 55  |...U.h#9z.9..CDU|
    00000020
    >

``script.py``:

.. sourcecode:: python

    import array
    import crypto as ut
    from Crypto.Cipher import AES

    key = b'YELLOW SUBMARINE'
    msg = b'Attack at dawn, await my signal'
    msg = ut.pad(msg,n=16)
    
    data = ut.load_binary_data('10.bin')
    
    L = array.array('B',data).tostring()
    L = ut.chunks(L)
    
    iv = '\x00'*16
    pt = ut.myCBC_decode(L,key,iv)
    print ''.join(pt)

.. sourcecode:: bash

    > python script.py 
    I'm back and I'm ringin' the bell 
    A rockin' on the mike while the fly girls yell 
    In ecstasy in the back of me 
    Well that's my DJ Deshay cuttin' all them Z's 
    Hittin' hard and the girlies goin' crazy 
    Vanilla's on the mike, man I'm not lazy. 
    ..

Looks like we did it.

=====================================================

**Set 2 No. 11:  An ECB/CBC detection oracle**

http://cryptopals.com/sets/2/challenges/11/

I admit I cheated slightly on this one.  I was looking for a way to detect whether *any* plaintext encoded by ECB v. CBC.  It turns out that it is OK to use the fact that we control the message.

Our message is encoded each time by a random key (with a random ``iv`` for CBC), and is padded by random bytes of relatively random length.  But, if the plaintext has a repeat with block size, then the ciphertext generated by ECB will also have a repeat of block size, and this is easy to detect since (as stated in #8):

    Remember that the problem with ECB is that it is stateless and deterministic; the same 16 byte plaintext block will always produce the same 16 byte ciphertext.
    
The random padding bytes mean that we need a triple repeat to ensure that we will have at least a simple repeat spanning two blocks.

Add to ``crypto.py``:

.. sourcecode:: python

    def has_repeated_items(L):
        return len(L) != len(set(L))

    def bytes_to_hex(src):
        """src can be bytes or a list of ints
        """
        L = [hex(ord(c))[2:] for c in src]
        L = [h.zfill(2) for h in L]
        return ''.join(L)

``script.py``:

.. sourcecode:: python

    import crypto as ut
    from Crypto.Cipher import AES
    from Crypto import Random
    r = Random.new()
    from Crypto.Random import random

    def encrypt(msg,key,iv,cbc):
        if not cbc:
            cp = AES.new(key, AES.MODE_ECB)
        else:
            cp = AES.new(key, AES.MODE_CBC, iv)
        return cp.encrypt(msg)

    def cbc_detected(ct):
        pL = list()
        for item in ut.chunks(ct,8):
            h = ut.bytes_to_hex(item)
            pL.append(h)
        reps = ut.has_repeated_items(pL)
        return reps

    def testOne(ct):
        reps = cbc_detected(ct)
        if reps and cbc:
            print 'false neg'
        elif not reps and not cbc:
            print 'false pos'

    msg = b'We need a repeatWe need a repeatWe need a repeat'

    N = 5
    R = range(5,10+1)
    L = list()

    for i in range(100):
        m = random.choice(R)
        n = random.choice(R)
        msg = r.read(m) + msg + r.read(n)

        msg = str(ut.pad(msg,n=16))
        key = r.read(16)
        iv = r.read(16)

        cbc = random.choice([0,1])
        ct = encrypt(msg,key,iv,cbc)
        testOne(ct)

And this is what we generate:

.. sourcecode:: bash

    > python script.py 
    >

=====================================================

**Set 2 No. 12:  Byte-at-a-time ECB decryption (Simple)**

http://cryptopals.com/sets/2/challenges/12/

We are given a string (in base64) and asked to decode it only in code.

We are also asked to generate a random but consistent key for repeated use.  Then, varying the message, we will append the string from above, and encode it using ECB mode with the key.

The first step is then to detect the block size by feeding the encryption function varying messages.  We recall from the previous problem that we will detect repeating ciphertext blocks when the message reaches a multiple of 2 times the block size.

Add to ``crypto.py``:

.. sourcecode:: python

    def cbc_detected(ct):
        pL = list()
        for item in chunks(ct,8):
            h = bytes_to_hex(item)
            pL.append(h)
        reps = has_repeated_items(pL)
        return reps

And here is my ``script.py``:

.. sourcecode:: python

    import array, base64
    import crypto as ut
    from Crypto.Cipher import AES
    from Crypto import Random
    r = Random.new()
    
    # random but consistent key
    N = AES.block_size
    key = r.read(N)
    cp = AES.new(key, AES.MODE_ECB)
    
    # data has 3 lines of 60 each + 4 bytes more
    data = ut.load_data('12.txt')
    s = base64.b64decode(data)
    
    # if newlines are ignored we should have 
    # 3*45 + 3 = 138, and we do
    # print len(s)
    
    def weird_encode(msg):
        msg += s
        msg = str(ut.pad(msg,n=AES.block_size))
        return cp.encrypt(msg)
    
    i = 0
    while True:
        i += 1
        msg = b'A' * i
        ct = weird_encode(msg)
        if ut.cbc_detected(ct):
            print i
            break

.. sourcecode:: bash

    > python script.py 
    32
    >

We deduce that the block size is half that, or 16.

Now the trick is this:  if we make our message have 31 bytes (one byte short of a repeat), the 32nd byte will come from the unknown string.

We vary the 16th byte of the input until we see a repeat in the ciphertext.  That byte is the first byte of the unknown string.

Replace the code below ``weird_encode`` in ``script.py``:

.. sourcecode:: python

    def discover_byte(pos,master):
        found = False
        for j in range(256):
            b = array.array('B',[j]).tostring()
            msg = master[:]
            msg[pos] = b
            msg = str(bytearray(msg))
            ct = weird_encode(msg)
            if ut.cbc_detected(ct):
                found = True
                break
        return found, b
    
    i = 15
    master = ['A'] * (i + N)
    print discover_byte(i,master)

.. sourcecode:: bash

    > python script.py 
    (True, 'R')
    >

We can read 16 bytes in this way.  Now it seems unlikely that we would have control of the string, but perhaps so.  If we have that we can read the whole thing.

.. sourcecode:: python

    import array, base64
    import crypto as ut
    from Crypto.Cipher import AES
    from Crypto import Random
    r = Random.new()

    # random but consistent key
    N = AES.block_size
    key = r.read(N)
    cp = AES.new(key, AES.MODE_ECB)

    # data has 3 lines of 60 each + 4 bytes more
    data = ut.load_data('12.txt')
    s = base64.b64decode(data)

    # if newlines are ignored we should have 
    # 3*45 + 3 = 138, and we do
    # print len(s)

    def weird_encode(msg,s):
        msg += s
        msg = str(ut.pad(msg,n=AES.block_size))
        return cp.encrypt(msg)

    def discover_byte(s, master):
        n = 15  # position to match last entry
        found = False
        for i in range(256):
            b = array.array('B',[i]).tostring()
            msg = master[:]
            msg[n] = b
            msg = str(bytearray(msg))
            ct = weird_encode(msg,s)
            if ut.cbc_detected(ct):
                found = True
                break
        return found, b

    def read16(s):
        master = ['A'] * N * 2
        for i in range(N):
            master.pop(0)
            flag, b = discover_byte(s,master)
            if not flag:
                print 'error', i, ''.join(master)
                start = N - (i+1)
                stop = i + 3
                master = master[start:stop]
                break
            else:
                print 'found', str(i).rjust(2),
                print b, ''.join(master)
                master[15] = b
        return ''.join(master)

    pL = list()
    while s:
        result = read16(s)
        pL.append(result)
        s = s[16:]

    print ''.join(pL)

.. sourcecode:: bash

    > python script.py 
    found  0 R AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
    found  1 o AAAAAAAAAAAAAARAAAAAAAAAAAAAAA
    found  2 l AAAAAAAAAAAAARoAAAAAAAAAAAAAA
    found  3 l AAAAAAAAAAAARolAAAAAAAAAAAAA
    found  4 i AAAAAAAAAAARollAAAAAAAAAAAA
    found  5 n AAAAAAAAAARolliAAAAAAAAAAA
    found  6 ' AAAAAAAAARollinAAAAAAAAAA
    found  7   AAAAAAAARollin'AAAAAAAAA
    found  8 i AAAAAAARollin' AAAAAAAA
    found  9 n AAAAAARollin' iAAAAAAA
    found 10   AAAAARollin' inAAAAAA
    found 11 m AAAARollin' in AAAAA
    found 12 y AAARollin' in mAAAA
    found 13   AARollin' in myAAA
    found 14 5 ARollin' in my AA
    found 15 . Rollin' in my 5A
    ..
    found  0   AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
    found  1 d AAAAAAAAAAAAAA AAAAAAAAAAAAAAA
    found  2 r AAAAAAAAAAAAA dAAAAAAAAAAAAAA
    found  3 o AAAAAAAAAAAA drAAAAAAAAAAAAA
    found  4 v AAAAAAAAAAA droAAAAAAAAAAAA
    found  5 e AAAAAAAAAA drovAAAAAAAAAAA
    found  6   AAAAAAAAA droveAAAAAAAAAA
    found  7 b AAAAAAAA drove AAAAAAAAA
    found  8 y AAAAAAA drove bAAAAAAAA
    found  9 
    AAAAAA drove byAAAAAAA
    found 10  AAAAA drove by
    AAAAAA
    error 11 AAAA drove by
    AAAAA
    Rollin' in my 5.0
    With my rag-top down so my hair can blow
    The girlies on standby waving just to say hi
    Did you stop? No, I just drove by

    >

    
    


