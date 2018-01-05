.. _bytes:

############################
Working with bytes in Python
############################

In this section, I want to do a brief review of operations with data as bytes (rather than say, ASCII strings) in Python.

The quick take on this is that ``int`` is a central type, so to convert from hexadecimal to binary or back again, we go through an ``int`` as an intermediate

For example, the function ``hex`` converts an integer to its hexadecimal equivalent.  The result has type ``str``:

>>> h = hex(65)
>>> type(h)
<type 'str'>
>>> h
'0x41'

since, as we can calculate:

.. math::

    65 = 4 \times 16^1 + 1 \times 16^0

According to the docs, ``hex`` will take as input an integer of any size:

>>> hex(65537)
'0x10001'
>>> import math
>>> n = math.factorial(10000)
>>> h = hex(n)
>>> len(h)
29618

They're not kidding.  Notice the result has ``'0x'`` only at the beginning of the string.

We convert the hexadecimal string back to an integer in a call to ``int``, but we must specify the appropriate base (base 16):

>>> h = hex(65537)
>>> int(h,16)
65537

In the same way, we can get the binary representation of an integer using ``bin``:

>>> bin(17)
'0b10001'
>>> bin(33)
'0b100001'
>>> b = bin(33)
>>> b
'0b100001'
>>> type(b)
<type 'str'>

As before with ``hex``, the output from ``bin`` is a string.  

The output loses leading one or more leading ``0``.  If you want to specify the padding, there are a couple of options.  One easy way is to use ``zfill``

>>> b
'0b01000001'
>>> b = bin(65)
>>> b
'0b1000001'
>>> b = '0b' + b[2:].zfill(8)
>>> b
'0b01000001'

Two other ways use fancy formatting

>>> '{:08b}'.format(65)
'01000001'
>>> format(65, '#010b')
'0b01000001'
>>> 

but I think that simpler is better if it is sufficient.

Having generated a binary string, we can go back to the equivalent integer by specifying base 2 in a call to ``int``, and then go on to hexadecimal from there if desired.

>>> b = bin(65)
>>> b
'0b1000001'
>>> int(b,2)
65
>>> hex(int(b,2))
'0x41'

Both of these examples so far are strings, representations of hexadecimal and binary numbers.  They are not really binary data.

A quick search turns up Python classes ``byte`` and ``bytearray``.  (Much more is available in Python 3.x, but we are just using 2.7).

The first one is just an alias for ``str``:

>>> L = [10, 32, 65]
>>> data = bytes(L)
>>> type(data)
<type 'str'>
>>> print data
[10, 32, 65]
>>> data
'[10, 32, 65]'
>>>

A ``bytearray`` can do more:

>>> L = [10, 32, 65]
>>> ba = bytearray(L)
>>> type(ba)
<type 'bytearray'>
>>> print ba


>>> for e in ba:
...     print e, type(e)
... 
10 <type 'int'>
32 <type 'int'>
65 <type 'int'>
>>>

An iterator over a ``bytearray`` returns ``int``.  But if we print a ``bytearray``, we get the string representation of the bytes, if possible, just as we did above.




http://stackoverflow.com/questions/7396849/convert-binary-to-ascii-and-vice-versa-python












Instead, an example of binary data might be obtained by entering the following:

>>> d = '\xff'
>>> d
'\xff'
>>> type(d)
<type 'str'>
>>> print d
?
>>> hex(255)
'0xff'

To enter binary data we use ``\xff``.  For a multibyte value each byte is preceded by ``\x``.

(To do:  explain the difference between ``print`` just evaluating the expression in the interpreter.)

The ``print`` function will use the printable character if there is one:

>>> print ('\x42')
B
>>> print ('\x0a')


>>>

It doesn't format correctly here, but the newline gave us two empty lines.  The interpreter starts output on a new blank line, then "prints" the newline (``LF``,'\x0a')  by moving to a second blank line, then finally gives us the interpreter prompt ``>>>`` after moving again to a new line.

An example of multiple bytes:

>>> data = '\x9b\x3c'
>>> data
'\x9b<'
>>> type(data)
<type 'str'>
>>> print data
?<

We still seem to be dealing with strings.  The hexadecimal value ``3c`` (``\x3c``) was printed as ``<`` in both tries.

>>> ord('<')
60
>>> hex(60)
'0x3c'
>>> type(hex(60))
<type 'str'>
>>> chr(60)
'<'
>>> print str(hex(60))
0x3c

The explanation is that ``<`` is the ASCII representation of the integer value 60, which is equal to the hexadecimal value ``3c``.  Since ``<`` is a printable character, that is what Python shows us.  This has been a point of confusion for me in dealing with binary data in Python.  Curiously, if we convert explicitly to string and then print, we don't get the quotes.

>>> print hex(60)
0x3c
>>> hex(60)
'0x3c'

Here is a second example:

>>> import hashlib
>>> m = hashlib.md5()
>>> m.update('hello')
>>> d = m.digest()
>>> len(d)
16
>>> type(d)
<type 'str'>
>>> d
']A@*\xbcK*v\xb9q\x9d\x91\x10\x17\xc5\x92'

As before, if a printable character is available, Python will print that.  Otherwise it prints ``\x`` plus the hex representation.  In the above string, there are eight printable characters, each one byte (]A@*K*vq), plus another eight explicit bytes.

If you want the hexadecimal representation for all 16 of them, you could use ``ord`` to convert each value to an integer:

>>> L = [ord(y) for y in d]
>>> len(L)
16
>>> L[:4]
93
>>> L[:4]
[93, 65, 64, 42]

The last four are non-printing, and their integer values are > 128:

>>> L[-4:]
[16, 23, 197, 146]
>>> s = ''.join([hex(i) for i in L])
>>> s[:4]
'0x5d0x410x400x2a0xbc0x4b0x2a0x760xb90x710x9d0x910x100x170xc50x92'

If we write the data to disk

>>> FH = open('x.bin','wb')
>>> FH.write(d)
>>> FH.close()

If we examine this from the shell:

.. sourcecode:: bash

    > hexdump -C x.bin
    00000000  5d 41 40 2a bc 4b 2a 76  b9 71 9d 91 10 17 c5 92  |]A@*.K*v.q......|
    00000010

And if we read it back in as binary data:

>>> FH = open('x.bin','rb')
>>> data = FH.read()
>>> data
']A@*\xbcK*v\xb9q\x9d\x91\x10\x17\xc5\x92'
>>> data == d
True

We can generate binary data from integers using the function ``ord``.  As an example, the last byte of the data above

>>> c = chr(146)
>>> type(c)
<type 'str'>
>>> c
'\x92'

This only works one byte at a time:

>>> chr(256)
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
ValueError: chr() arg not in range(256)

In summary, integers seem to be the unifying type.  From integers we can go to hexadecimal (``hex``), 0s and `s (``bin``) or binary data (``chr``).  The complementary functions which return us to integers are ``int`` (with the appropriate base), or in the last case, ``ord``.

We can use the ``struct`` module to look at multibyte data.  

>>> L = [65,146]
>>> d = ''.join([chr(i) for i in L])
>>> d
'A\x92'
>>> len(d)
2

The last result should not be a surprise any more.  If we want to go through the bytes one at a time, the reasonable way is to use ``ord``.  But another way would be:

>>> from struct import unpack
>>> unpack('B',d[0])
(65,)
>>> unpack('B',d[1])
(146,)

The advantage of this approach is we can get an integer (encoded in binary) in one step:

>>> h = '\x01\x00\x00\x01'
>>> h
'\x01\x00\x00\x01'
>>> type(h)
<type 'str'>
>>> unpack('I',h)
(16777217,)

We can check it:

>>> 256**3 + 1
16777217

Or just use ``ord``:

>>> for c in h:
...     print ord(c)
... 
1
0
0
1

