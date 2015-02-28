.. _n9:

#########
Interlude
#########

**Conversion to and from bytes**

Here are bytes <=> ints:

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


