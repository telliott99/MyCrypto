.. _base64:

###################
Working with base64
###################

In this section, I want to do a brief review of base64 encoding in Python.

The idea is to transform standard binary data, representable as integers in the range [0..255], to the base64 format, which uses a 64 character set.  One reason to do that is the restricted set is safe for sending in URLs, while binary data is not.

64 characters require 6 bits.  To do the encoding, we will transform a 3-byte (18 bit) sequence to 4 characters of 6 bits each.

The wikipedia example is a good place to start:

http://en.wikipedia.org/wiki/Base64

we should convert "Man" to "TWFu".

As we said, it may be easiest to think of binary data as a sequence of integers in the range [0..255], though we can also think of it as a sequence of hexadecimal digit pairs in the range ['00'..'ff'], or even the ASCII equivalent, for those values that have a printable equivalent.

Thus 'M' has the value 77

    >>> ord('M')
    77
    >>> ord('a')
    97
    >>> ord('n')
    110
    >>>

so 'Man' is really (77,97,110).

Now 77 is equal to 64 + 8 + 4 + 1 or '0b01001101'.

    >>> bin(77)
    '0b1001101'
    >>>

Notice that Python strips the high value bits if they are equal to '0', and prepends '0b'.  We can fix that with ``zfill``:

    >>> bin(77)[2:].zfill(8)
    '01001101'
    >>>

So

    >>> def f(c):
    ...     return bin(c)[2:].zfill(8)
    ... 
    >>> ''.join([f(c) for c in [77,97,110]])
    '010011010110000101101110'
    >>> ' '.join([f(ord(c)) for c in 'Man'])
    '01001101 01100001 01101110'
    >>>

Now we take those as four 6-bit chunks:

    010011 010110 000101 101110

And converting to decimal equivalent (base 10) we obtain:  19,22,5,46.  

Now we just need to encode these digits.  To get 64 characters, we use A..Z + a..z + 0..9 plus two more.  The standard two additions are '+/', but sometimes others are used.

The 19th letter (counting from 0) is 'T', the 22nd is 'W', the 5th is 'F', and if you look up in the table you will find that 46 is 'u'.

So the base64 version of 'Man' is 'TWFu'

The only complication when encoding is if the binary data is not a multiple of 3.  In that case, we add either one or two instances of the character '=' (decimal 61, binary '00111101).

With this background, it should be clear what the code below does.  The basic routine converts a triplet of 3 integers [0..255] to a sequence of four integers [0..64].  

We use that one to build up routines that take an ASCII string or a three-byte string in hexadecimal (6 digits).

Finally, I show routines from the ``base64`` module that do the encoding for us, starting from a string or hex data.

The code is really simple:

    >>> import base64
    >>> base64.b64encode('Man')
    'TWFu'
    >>> h = '0x4d616e'[2:].decode('hex')
    >>> h
    'Man'
    >>> base64.b64encode(h)
    'TWFu'
    >>>

If the decode step above generates a non-printable letter, you will get something like this:

    >>> 'ff'.decode('hex')
    '\xff'
    >>> '4d'.decode('hex')
    'M'

One of the stumbling blocks that I had with this topic is that examples often take hex data (such as '0x4d616e') and encode it as if it were ASCII.  This is OK, but wasteful.

.. sourcecode:: python

    import random, base64

    lc = 'abcdefghijklmnopqrstuvwxyz'
    uc = lc.upper()
    dg = '0123456789'
    L = list(uc + lc + dg + '+/')
    b64_dict = dict(zip(range(len(L)),L))

    def binary_repr(n):
        # strip out the '0b', pad to 8 bits
        b = bin(n)[2:].zfill(8)
        return b

    # takes   3 ints [0,255]
    # returns 4 ints [0,63]
    def group_bits_3to4(t):
        x,y,z = t
        x = binary_repr(x)
        y = binary_repr(y)
        z = binary_repr(z)

        a = x[:6]
        b = x[-2:] + y[:4]
        c = y[-4:] + z[:2]
        d = z[-6:]
        assert x + y + z == a + b + c + d

        a = int(a,2)
        b = int(b,2)
        c = int(c,2)
        d = int(d,2)
        return (a,b,c,d)

    # t is a triplet of ints [0,255] (bytes)
    def b64encode_ints(t):
        a,b,c,d = group_bits_3to4(t)
        A = b64_dict[a]
        B = b64_dict[b]
        C = b64_dict[c]
        D = b64_dict[d]
        return A + B + C + D

    # t is ASCII string, ignores extra values
    def b64encode_ascii_str(s):
        while len(s) < 3:
            s += '='
        x = ord(s[0])
        y = ord(s[1])
        z = ord(s[2])
        return b64encode_ints((x,y,z))

    # h is a triplet of bytes in hex
    def b64encode_hex(h):
        if h[:2] == '0x':  h = h[2:]
        assert len(h) == 6
        x = int(h[:2],16)
        y = int(h[2:4],16)
        z = int(h[4:6],16)
        return b64encode_ints((x,y,z))

    print b64encode_ascii_str('Man')
    print b64encode_hex('0x4d616e')

    print base64.b64encode('Man')
    h = '0x4d616e'[2:].decode('hex')
    print base64.b64encode(h)

When this script is run with ``python script.py``, I obtain:

.. sourcecode:: bash

    $ python script.py 
    TWFu
    TWFu
    TWFu
    TWFu
    $
