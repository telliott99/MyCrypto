.. _formats:

####################
Standard key formats
####################

In this chapter we make a start on exploring the detailed structure of RSA public/private key pairs used for asymmetric cryptography.  As we saw in a previous chapter, this method uses two large prime numbers *p* and *q* and their product *n*, and two exponents called the public exponent *e* (a small prime, usually 65537), and the private exponent *d*.

An RSA public key consists of 

* *n* -- the RSA *modulus*
* *e* -- RSA public exponent

An RSA private key consists of these values in order:

* *n*
* *e*
* *d* -- the RSA private exponent
* *p* -- prime1, prime factor of *n*
* *q* -- prime2, prime factor of *n*
* exponent 1 :math:`d\ mod (p-1)`
* exponent 2 :math:`d\ mod (q-1)`
* CRT coefficient
    
PKCS is a family of standards called *Public Key Cryptography Standards* (PKCS):

http://en.wikipedia.org/wiki/PKCS
https://tools.ietf.org/html/rfc3447

PKCS #1 defines the cryptographic protocol---how to use the various components of private and public keys.  PKCS #8 is the *Private-Key Information Syntax Standard*.

Previously we saw examples of using th

Keys may be written in several different formats, and generally, the data is `base64` encoded so it can be transmitted over a network.  Formats include ASN.1 and pem.  It seems pretty complicated, so maybe it's better to just look at the two we commonly encounter.

I am going to give these formats my own short names to distinguish them, and we'll see how far we get.

**SSH Format**

This format is what ``ssh-keygen`` gives, and is sometimes called Open SSH

http://en.wikipedia.org/wiki/Ssh-keygen

The public key generated by this method is distinguished by the text ``ssh-rsa`` in plain ASCII encoding at the beginning of the public key file, before the base64 starts.

As we saw before, to generate such a key from the command line with ``openssh`` installed:

.. sourcecode:: bash

    > ssh-keygen -t rsa -b 1024 -f ./kf -C "te"
    ..
    > hexdump -C -n 64 kf
    00000000  2d 2d 2d 2d 2d 42 45 47  49 4e 20 52 53 41 20 50  |-----BEGIN RSA P|
    00000010  52 49 56 41 54 45 20 4b  45 59 2d 2d 2d 2d 2d 0a  |RIVATE KEY-----.|
    00000020  4d 49 49 43 58 51 49 42  41 41 4b 42 67 51 43 33  |MIICXQIBAAKBgQC3|
    00000030  72 4c 62 74 6b 2b 79 54  35 6b 66 41 2f 4e 42 2f  |rLbtk+yT5kfA/NB/|
    00000040
    >
    > hexdump -C kf.pub
    00000000  73 73 68 2d 72 73 61 20  41 41 41 41 42 33 4e 7a  |ssh-rsa AAAAB3Nz|
    00000010  61 43 31 79 63 32 45 41  41 41 41 44 41 51 41 42  |aC1yc2EAAAADAQAB|
    00000020  41 41 41 41 67 51 43 33  72 4c 62 74 6b 2b 79 54  |AAAAgQC3rLbtk+yT|
    00000030  35 6b 66 41 2f 4e 42 2f  59 69 48 78 2f 44 53 74  |5kfA/NB/YiHx/DSt|
    00000040  66 51 6e 70 4e 58 63 47  31 38 6a 31 6e 74 4b 4a  |fQnpNXcG18j1ntKJ|
    00000050  6f 79 72 78 79 38 72 5a  57 4f 64 74 62 4f 77 35  |oyrxy8rZWOdtbOw5|
    00000060  41 62 32 50 56 46 74 4a  67 49 55 6a 78 74 52 4a  |Ab2PVFtJgIUjxtRJ|
    00000070  68 4d 47 66 53 53 73 32  5a 2b 78 38 70 6c 46 57  |hMGfSSs2Z+x8plFW|
    00000080  68 70 4d 32 66 51 57 2f  77 34 43 34 6c 46 2f 49  |hpM2fQW/w4C4lF/I|
    00000090  34 6b 48 6c 31 48 36 43  34 47 34 62 44 72 33 51  |4kHl1H6C4G4bDr3Q|
    000000a0  73 2f 57 6c 39 6a 4e 6f  46 33 39 53 62 43 39 59  |s/Wl9jNoF39SbC9Y|
    000000b0  49 6f 42 4e 56 55 2b 6b  61 57 6d 2b 2f 59 36 78  |IoBNVU+kaWm+/Y6x|
    000000c0  58 7a 36 5a 34 63 50 6f  31 49 65 7a 42 50 52 61  |Xz6Z4cPo1IezBPRa|
    000000d0  6f 51 3d 3d 20 74 65 0a                           |oQ== te.|
    000000d8
    >

The default key size is 2048 bits.  Here we've chosen a key size of 1024 bits.  Altogether, this public key file ``kf.pub`` contains 216 bytes or 1728 bits:

.. sourcecode:: bash

    > ls -al kf.pub
    -rw-r--r--  1 telliott_admin  staff  216 Feb 27 10:06 kf.pub
    >

The part up to and including ``AAADAQAB`` in the third line is common to all such keys.  ``AAADAQAB`` actually encodes *e* (see below).  The data after the first 8 characters is encoded in base64.  The file ends with the comment " te" (without quotes) in ASCII encoding, separated by a space from the key data.

According to the man page:

The type of key to be generated is specified with the -t option. If invoked without any arguments, ``ssh-keygen`` will generate an RSA key for use in SSH protocol 2 connections.

Take a look at the public key.  We can use Python, or use the command line.  Let's start with the latter.  After fooling around, I find the correct parameters to strip off the excess characters:

.. sourcecode:: bash

    > cat kf.pub | tail -c +9 | head -c +204 > x.b64
    > hexdump -C x.b64
    00000000  41 41 41 41 42 33 4e 7a  61 43 31 79 63 32 45 41  |AAAAB3NzaC1yc2EA|
    00000010  41 41 41 44 41 51 41 42  41 41 41 41 67 51 43 33  |AAADAQABAAAAgQC3|
    00000020  72 4c 62 74 6b 2b 79 54  35 6b 66 41 2f 4e 42 2f  |rLbtk+yT5kfA/NB/|
    00000030  59 69 48 78 2f 44 53 74  66 51 6e 70 4e 58 63 47  |YiHx/DStfQnpNXcG|
    00000040  31 38 6a 31 6e 74 4b 4a  6f 79 72 78 79 38 72 5a  |18j1ntKJoyrxy8rZ|
    00000050  57 4f 64 74 62 4f 77 35  41 62 32 50 56 46 74 4a  |WOdtbOw5Ab2PVFtJ|
    00000060  67 49 55 6a 78 74 52 4a  68 4d 47 66 53 53 73 32  |gIUjxtRJhMGfSSs2|
    00000070  5a 2b 78 38 70 6c 46 57  68 70 4d 32 66 51 57 2f  |Z+x8plFWhpM2fQW/|
    00000080  77 34 43 34 6c 46 2f 49  34 6b 48 6c 31 48 36 43  |w4C4lF/I4kHl1H6C|
    00000090  34 47 34 62 44 72 33 51  73 2f 57 6c 39 6a 4e 6f  |4G4bDr3Qs/Wl9jNo|
    000000a0  46 33 39 53 62 43 39 59  49 6f 42 4e 56 55 2b 6b  |F39SbC9YIoBNVU+k|
    000000b0  61 57 6d 2b 2f 59 36 78  58 7a 36 5a 34 63 50 6f  |aWm+/Y6xXz6Z4cPo|
    000000c0  31 49 65 7a 42 50 52 61  6f 51 3d 3d              |1IezBPRaoQ==|
    000000cc
    >

The next step is to decode the base64.  I wasn't able to do it from the command line yet.  So I did ``cat x.b64`` and then in Python

>>> import base64
>>> s = 'AAAA..oQ=='
>>> s
'AAAA..oQ=='
>>> base64.b64decode(s)
'\x00\x00\x00\x07ssh-rsa..'
>>> FH = open('x.bin','wb')
>>> FH.write(base64.b64decode(s))
>>> FH.close()

Now

.. sourcecode:: bash

    > hexdump -C x.bin
    00000000  00 00 00 07 73 73 68 2d  72 73 61 00 00 00 03 01  |....ssh-rsa.....|
    00000010  00 01 00 00 00 81 00 b7  ac b6 ed 93 ec 93 e6 47  |...............G|
    00000020  c0 fc d0 7f 62 21 f1 fc  34 ad 7d 09 e9 35 77 06  |....b!..4.}..5w.|
    00000030  d7 c8 f5 9e d2 89 a3 2a  f1 cb ca d9 58 e7 6d 6c  |.......*....X.ml|
    00000040  ec 39 01 bd 8f 54 5b 49  80 85 23 c6 d4 49 84 c1  |.9...T[I..#..I..|
    00000050  9f 49 2b 36 67 ec 7c a6  51 56 86 93 36 7d 05 bf  |.I+6g.|.QV..6}..|
    00000060  c3 80 b8 94 5f c8 e2 41  e5 d4 7e 82 e0 6e 1b 0e  |...._..A..~..n..|
    00000070  bd d0 b3 f5 a5 f6 33 68  17 7f 52 6c 2f 58 22 80  |......3h..Rl/X".|
    00000080  4d 55 4f a4 69 69 be fd  8e b1 5f 3e 99 e1 c3 e8  |MUO.ii...._>....|
    00000090  d4 87 b3 04 f4 5a a1                              |.....Z.|
    00000097
    >

What we see is the decoded base64 data repeats the ``ssh-rsa`` designation.  The very beginning is four bytes ``00 00 00 07`` which tells us that the next 7 bytes is a group (namely ``ssh-rsa`` in ASCII).  Following that we have four bytes ``00 00 00 03`` which tell us that the next 3 bytes is a group:  ``01 00 01``.  Remember this is ``hex``.  The binary is ``0000 0001 0000 0000 0000 0001`` which is :math 2^{16} + 1 = 65537, and of course, that is the standard choice for *e*, the public exponent.

Following that, we have the four bytes ``00 00 00 81``.  Now, ``81`` which is hex for ``129`` indicating that 129 bytes of data follow.  I count 8 rows of 16 with one extra character.  That sounds right.  We just have to turn the hex into a decimal number.

>>> FH = open('x.bin','rb')
>>> data = FH.read()
>>> FH.close()
>>> data
'\x00\x00\x00\x07ssh-rsa\x00\x00\x00\x03\x01\x00\x01\x00\x00\x00\x81..'
>>> data[21]
'\x81'
>>> data = data[22:]
>>> len(data)
129
>>> L = [ord(b) for b in data]
>>> L
[0, 183, 172, ..

Just keep popping from the end of the list and accumulate a sum:

>>> sum = 0
>>> f = 1
>>> while L:
...     x = L.pop()
...     sum += f*x
...     f *= 256
... 
>>> sum
128980736947015960265564665097305727982458360210534686614046332729859457631658252973666506687544914417019074768634756860351656837379525566046400305369636987778810104215227872161118604102816375795453159636784411149607478923884056569787045540814171306335534498909187861683699979842695714915021585262043072846497L
>>>

This is *n*.  How do we check to see if we're right?  Well

.. sourcecode:: bash

    > openssl rsa -text -in kf.pub
    unable to load Private Key
    2210:error:0906D06C:PEM routines:PEM_read_bio:no start line:/SourceCache/OpenSSL098/OpenSSL098-52.10.1/src/crypto/pem/pem_lib.c:648:Expecting: ANY PRIVATE KEY
    > openssl rsa -text -in kf
    Private-Key: (1024 bit)
    modulus:
        00:b7:ac:b6:ed:93:ec:93:e6:47:c0:fc:d0:7f:62:
        21:f1:fc:34:ad:7d:09:e9:35:77:06:d7:c8:f5:9e:
        d2:89:a3:2a:f1:cb:ca:d9:58:e7:6d:6c:ec:39:01:
        bd:8f:54:5b:49:80:85:23:c6:d4:49:84:c1:9f:49:
        2b:36:67:ec:7c:a6:51:56:86:93:36:7d:05:bf:c3:
        80:b8:94:5f:c8:e2:41:e5:d4:7e:82:e0:6e:1b:0e:
        bd:d0:b3:f5:a5:f6:33:68:17:7f:52:6c:2f:58:22:
        80:4d:55:4f:a4:69:69:be:fd:8e:b1:5f:3e:99:e1:
        c3:e8:d4:87:b3:04:f4:5a:a1
    publicExponent: 65537 (0x10001)

It's in hex.  Maybe just match it against the data!

>>> FH = open('x.bin','rb')
>>> data = FH.read()
>>> FH.close()
>>> data[22:]
'\x00\xb7\xac\xb6\xed\x93\xec\x93\xe6G\xc0\xfc\xd0\x7fb!\xf1\xfc4\xad}\t\xe95w\x06\xd7\xc8\xf5\x9e\xd2\x89\xa3*\xf1\xcb\xca\xd9X\xe7ml\xec9\x01\xbd\x8fT[I\x80\x85#\xc6\xd4I\x84\xc1\x9fI+6g\xec|\xa6QV\x86\x936}\x05\xbf\xc3\x80\xb8\x94_\xc8\xe2A\xe5\xd4~\x82\xe0n\x1b\x0e\xbd\xd0\xb3\xf5\xa5\xf63h\x17\x7fRl/X"\x80MUO\xa4ii\xbe\xfd\x8e\xb1_>\x99\xe1\xc3\xe8\xd4\x87\xb3\x04\xf4Z\xa1'
>>>

Another way is to convert the hex modulus to a decimal.  Paste ``00:b7:ac:..`` into Python as a multiline string variable *t* and then do:

>>> tL = [c for c in t if not c in ' .:\n']
>>> h = '0x' + ''.join(tL)
>>> int(h,16)
128980736947015960265564665097305727982458360210534686614046332729859457631658252973666506687544914417019074768634756860351656837379525566046400305369636987778810104215227872161118604102816375795453159636784411149607478923884056569787045540814171306335534498909187861683699979842695714915021585262043072846497L
>>>

Looks like a match!

**SSL Format**

This format is distinguished by the text BEGIN PUBLIC KEY, (i.e. lacking the word RSA). It is also called X.509, according to 

http://www.cryptosys.net/pki/rsakeyformats.html

and is the same as PKCS #1 (PKCS #1/X.509), according to

http://www.cryptopp.com/wiki/Keys_and_Formats.

It is also called Open SSL format and is what ``openssl`` generates for public keys by default, starting with a private key generated by either ``openssh`` or ``openssl``.

.. sourcecode:: bash

    $ openssl genrsa -out privkey.pem 2048
    Generating RSA private key, 2048 bit long modulus
    ........................+++
    ......................................................+++
    e is 65537 (0x10001)

.. sourcecode:: bash

    $ openssl rsa -in privkey.pem -pubout > pubkey.pub
    writing RSA key
    $ hexdump -C pubkey.pub
    00000000 2d 2d 2d 2d 2d 42 45 47 49 4e 20 50 55 42 4c 49 |-----BEGIN PUBLI|
    00000010 43 20 4b 45 59 2d 2d 2d 2d 2d 0a 4d 49 49 42 49 |C KEY-----.MIIBI|
    00000020 6a 41 4e 42 67 6b 71 68 6b 69 47 39 77 30 42 41 |jANBgkqhkiG9w0BA|
    ..

Here, we used the flag ``genrsa`` with ``openssl`` to generate a private key, and then derived the public key from that.

According to the Python ``rsa`` module docs

http://stuvel.eu/files/python-rsa-doc/reference.html#functions 

this is a PKCS#1.5 PEM-encoded public key file from OpenSSL.  PEM-encoding should not be confused with the key type. PEM and binary format DER are alternatives. What they call PEM encoding is the default. This phrase refers to the fact that there is a header and a footer and base64-encoded data in between. However, different key formats may all be PEM-encoded.

As mentioned above these files can be recognized because they contain the phrase BEGIN PUBLIC KEY.  We can also use the conversion utility on the private key file generated in part A by ``ssh-keygen``.

.. sourcecode:: bash

    > openssl rsa -in kf -pubout > kf.pub.pem
    writing RSA key
    > hexdump -C kf.pub.pem
    00000000  2d 2d 2d 2d 2d 42 45 47  49 4e 20 50 55 42 4c 49  |-----BEGIN PUBLI|
    00000010  43 20 4b 45 59 2d 2d 2d  2d 2d 0a 4d 49 47 66 4d  |C KEY-----.MIGfM|
    00000020  41 30 47 43 53 71 47 53  49 62 33 44 51 45 42 41  |A0GCSqGSIb3DQEBA|
    00000030  51 55 41 41 34 47 4e 41  44 43 42 69 51 4b 42 67  |QUAA4GNADCBiQKBg|
    00000040  51 43 33 72 4c 62 74 6b  2b 79 54 35 6b 66 41 2f  |QC3rLbtk+yT5kfA/|
    00000050  4e 42 2f 59 69 48 78 2f  44 53 74 0a 66 51 6e 70  |NB/YiHx/DSt.fQnp|
    00000060  4e 58 63 47 31 38 6a 31  6e 74 4b 4a 6f 79 72 78  |NXcG18j1ntKJoyrx|
    00000070  79 38 72 5a 57 4f 64 74  62 4f 77 35 41 62 32 50  |y8rZWOdtbOw5Ab2P|
    00000080  56 46 74 4a 67 49 55 6a  78 74 52 4a 68 4d 47 66  |VFtJgIUjxtRJhMGf|
    00000090  53 53 73 32 5a 2b 78 38  70 6c 46 57 0a 68 70 4d  |SSs2Z+x8plFW.hpM|
    000000a0  32 66 51 57 2f 77 34 43  34 6c 46 2f 49 34 6b 48  |2fQW/w4C4lF/I4kH|
    000000b0  6c 31 48 36 43 34 47 34  62 44 72 33 51 73 2f 57  |l1H6C4G4bDr3Qs/W|
    000000c0  6c 39 6a 4e 6f 46 33 39  53 62 43 39 59 49 6f 42  |l9jNoF39SbC9YIoB|
    000000d0  4e 56 55 2b 6b 61 57 6d  2b 2f 59 36 78 0a 58 7a  |NVU+kaWm+/Y6x.Xz|
    000000e0  36 5a 34 63 50 6f 31 49  65 7a 42 50 52 61 6f 51  |6Z4cPo1IezBPRaoQ|
    000000f0  49 44 41 51 41 42 0a 2d  2d 2d 2d 2d 45 4e 44 20  |IDAQAB.-----END |
    00000100  50 55 42 4c 49 43 20 4b  45 59 2d 2d 2d 2d 2d 0a  |PUBLIC KEY-----.|
    00000110
    >
    
This public key format is referred to in the ``rsa`` module as a ”PKCS#1.5 PEM-encoded public key file from OpenSSL.” I'm not sure about the difference between 1 and 1.5.

Compare with ``SSH``

.. sourcecode:: bash

    > hexdump -C kf.pub
    00000000  73 73 68 2d 72 73 61 20  41 41 41 41 42 33 4e 7a  |ssh-rsa AAAAB3Nz|
    00000010  61 43 31 79 63 32 45 41  41 41 41 44 41 51 41 42  |aC1yc2EAAAADAQAB|
    00000020  41 41 41 41 67 51 43 33  72 4c 62 74 6b 2b 79 54  |AAAAgQC3rLbtk+yT|
    00000030  35 6b 66 41 2f 4e 42 2f  59 69 48 78 2f 44 53 74  |5kfA/NB/YiHx/DSt|
    00000040  66 51 6e 70 4e 58 63 47  31 38 6a 31 6e 74 4b 4a  |fQnpNXcG18j1ntKJ|
    00000050  6f 79 72 78 79 38 72 5a  57 4f 64 74 62 4f 77 35  |oyrxy8rZWOdtbOw5|
    00000060  41 62 32 50 56 46 74 4a  67 49 55 6a 78 74 52 4a  |Ab2PVFtJgIUjxtRJ|
    00000070  68 4d 47 66 53 53 73 32  5a 2b 78 38 70 6c 46 57  |hMGfSSs2Z+x8plFW|
    00000080  68 70 4d 32 66 51 57 2f  77 34 43 34 6c 46 2f 49  |hpM2fQW/w4C4lF/I|
    00000090  34 6b 48 6c 31 48 36 43  34 47 34 62 44 72 33 51  |4kHl1H6C4G4bDr3Q|
    000000a0  73 2f 57 6c 39 6a 4e 6f  46 33 39 53 62 43 39 59  |s/Wl9jNoF39SbC9Y|
    000000b0  49 6f 42 4e 56 55 2b 6b  61 57 6d 2b 2f 59 36 78  |IoBNVU+kaWm+/Y6x|
    000000c0  58 7a 36 5a 34 63 50 6f  31 49 65 7a 42 50 52 61  |Xz6Z4cPo1IezBPRa|
    000000d0  6f 51 3d 3d 20 74 65 0a                           |oQ== te.|
    000000d8
    >

There appears to be a match following the ``AAAA`` on line 3 of the second one to line 5 of the first.  Let's just match it all up by hand

.. sourcecode:: bash

    SSH     gQC3rLbtk+yT    5kfA/NB/YiHx/DSt    fQnpNXcG18j1ntKJ    oyrxy8rZWOdtbOw5
    SSL     g
    --------QC3rLbtk+yT    5kfA/
    -----------------------------NB/YiHx/DSt   .fQnp
    ------------------------------------------------NXcG18j1ntKJ    oyrx
    --------------------------------------------------------------------y8rZWOdtbOw5
             
             
    SSH Ab2PVFtJgIUjxtRJ    hMGfSSs2Z+x8plFW    hpM2fQW/w4C4lF/I    4kHl1H6C4G4bDr3Q
    SSL Ab2P
    --------VFtJgIUjxtRJ    hMGf
    ----------------------------SSs2Z+x8plFW   .hpM
    -----------------------------------------------2fQW/w4C4lF/I    4kH
    -------------------------------------------------------------------l1H6C4G4bDr3Q
    
    SSH s/Wl9jNoF39SbC9Y    IoBNVU+kaWm+/Y6x    Xz6Z4cPo1IezBPRa    oQ== te.
    SSL s/W
    -------l9jNoF39SbC9Y    IoB
    ---------------------------NVU+kaWm+/Y6x   .Xz
    ----------------------------------------------6Z4cPo1IezBPRa    oQIDAQAB

Perfect match except for 3 extra bytes in ``SSL``.  These are just the newlines that give nice printing for the ``kf.pub.pem`` version.

The match starts with ``gQC3``.  Since we haven't decoded the base64 yet it's hard to tell what this is but we can do:

>>> import base64
>>> 
>>> def f(input):
...     data = base64.b64decode(input)
...     print `data`
...     L = [ord(b) for b in data]
...     print L
...     print ' '.join([hex(h)[2:].zfill(2) for h in L])
... 
>>> 
>>> 
>>> f('gQC3')
'\x81\x00\xb7'
[129, 0, 183]
81 00 b7
>>>

The match starts with the last of the four bytes that shows the size of *n* (correct since the first three are ``00 00 00`` ), followed by the data for it.  Where is *e* in ``SSL`` format?

``SSH`` end of line 2:  

>>> f('AAADAQAB')
'\x00\x00\x03\x01\x00\x01'
[0, 0, 3, 1, 0, 1]
00 00 03 01 00 01
>>>

We are looking for ``AAADAQAB`` in ``SSL``.  You can find it in the non-matching tail above, or at least the ``DAQAB``.  So ``SSH`` has *e* first, and ``SSL`` has it after *n*.

**RSA Format**

The private key from above is distinguished by the text BEGIN RSA PRIVATE KEY and I refer to it here as RSA for this reason.

It is PKCS #8, according to

http://www.cryptopp.com/wiki/Keys_and_Formats 

**private key format**

Finally, we can also get some idea about private key structure using the Python code we had above:

``x.py``:

.. sourcecode:: python

    import base64

    def f(input):
        data = base64.b64decode(input)
        print `data`
        L = [ord(b) for b in data]
        print L
        for i in range(0,len(L),32):
            print ' '.join([hex(h)[2:].zfill(2) for h in L[i:i+32]])

First, on the command line

.. sourcecode:: bash

    > cat kf
    -----BEGIN RSA PRIVATE KEY-----
    MIICXwIBAAKBgQDXqfCjR00CtE1cCxPrtyl1wUgGj80oB3P/a42CouLUsmVD9oj4
    vAopoKurel4XgNbCVV7QfEnukhiqB/Sf7YaJPY9yVKjuCN2J5mgxaEV3hLrrU2zT
    E1gh/tA+sJDotsgapac9wRTIyqhGzMh+8deCa/CjOpjqQ/oBOpelU1UIvwIDAQAB
    AoGBANMznPL6H6P3WQ871g1weYzVdSjf6SU7b1EDTjlSNVvhPSS6qlcVJ8qui5BK
    LR1NUoRMQKdiILEfqEHTurBoV+gAwkme9XPq6P2V6A85KXsE7DQJqR9RcstwOj9W
    XesdAF23jdORL4M4cN0G+2hi7iiGE4TF3jmCEC+fjf+rR+fhAkEA8xfHBq9JcJtV
    Cu/9PNs6agbYus5vxp7QKzF5PKjPxLCILArEO6QgELRZHFLFslJVe6igZBDeadp8
    m9iExT78DwJBAOMdVcoZjqOvyV2fdM1KVhBpYETf+Xf+Oq0QADVIYA+VL6B9uJ9s
    GjOe08h+gFb3vNvPnsN0Ebz9oIzWuDR8OFECQQCvrHI/KXOYNhjaI57NWNy4/KOp
    NEBguCpV3JXxuUkUqkJuGYXAWBZ4G+z94+9Ms+VkzPLD/dDNjIBam7kvVhoPAkEA
    ra82d2saGXYKkc2rHoAV11Eu7R04BBrpNoaBEj56MBCQLrVWppyeYRG6tp5/eYLV
    7GgX6zNtiVGRIYPntUO2MQJBAJBEN4VgKAtVZ8ISmU7qWAk3yDSQ2mPNJFhLLhdV
    YGU1dNjAEKIsiagGhJxvxW46ojs1IwDUTpMWj0BHljb4T+g=
    -----END RSA PRIVATE KEY-----
    >

Then copy and paste the data into the Python interpreter and do:

>>> s = ''.join([c for c in s if not c in ' \n'])
>>> s
'MIICXwIBAAKBgQDXqfCjR00CtE1cCxPrtyl1wUgGj80oB3P/a42CouLUsmVD9oj4vAopoKurel4XgNbCVV7QfEnukhiqB/Sf7YaJPY9yVKjuCN2J5mgxaEV3hLrrU2zTE1gh/tA+sJDotsgapac9wRTIyqhGzMh+8deCa/CjOpjqQ/oBOpelU1UIvwIDAQABAoGBANMznPL6H6P3WQ871g1weYzVdSjf6SU7b1EDTjlSNVvhPSS6qlcVJ8qui5BKLR1NUoRMQKdiILEfqEHTurBoV+gAwkme9XPq6P2V6A85KXsE7DQJqR9RcstwOj9WXesdAF23jdORL4M4cN0G+2hi7iiGE4TF3jmCEC+fjf+rR+fhAkEA8xfHBq9JcJtVCu/9PNs6agbYus5vxp7QKzF5PKjPxLCILArEO6QgELRZHFLFslJVe6igZBDeadp8m9iExT78DwJBAOMdVcoZjqOvyV2fdM1KVhBpYETf+Xf+Oq0QADVIYA+VL6B9uJ9sGjOe08h+gFb3vNvPnsN0Ebz9oIzWuDR8OFECQQCvrHI/KXOYNhjaI57NWNy4/KOpNEBguCpV3JXxuUkUqkJuGYXAWBZ4G+z94+9Ms+VkzPLD/dDNjIBam7kvVhoPAkEAra82d2saGXYKkc2rHoAV11Eu7R04BBrpNoaBEj56MBCQLrVWppyeYRG6tp5/eYLV7GgX6zNtiVGRIYPntUO2MQJBAJBEN4VgKAtVZ8ISmU7qWAk3yDSQ2mPNJFhLLhdVYGU1dNjAEKIsiagGhJxvxW46ojs1IwDUTpMWj0BHljb4T+g='
>>>


>>> import x
>>> x.f(s)
"0\x82..
30 82 02 5f 02 01 00 02 81 81 00 d7 a9 f0 a3 47 4d 02 b4 4d 5c 0b 13 eb b7 29 75 c1 48 06 8f cd
28 07 73 ff 6b 8d 82 a2 e2 d4 b2 65 43 f6 88 f8 bc 0a 29 a0 ab ab 7a 5e 17 80 d6 c2 55 5e d0 7c
49 ee 92 18 aa 07 f4 9f ed 86 89 3d 8f 72 54 a8 ee 08 dd 89 e6 68 31 68 45 77 84 ba eb 53 6c d3
13 58 21 fe d0 3e b0 90 e8 b6 c8 1a a5 a7 3d c1 14 c8 ca a8 46 cc c8 7e f1 d7 82 6b f0 a3 3a 98
ea 43 fa 01 3a 97 a5 53 55 08 bf 02 03 01 00 01 02 81 81 00 d3 33 9c f2 fa 1f a3 f7 59 0f 3b d6
0d 70 79 8c d5 75 28 df e9 25 3b 6f 51 03 4e 39 52 35 5b e1 3d 24 ba aa 57 15 27 ca ae 8b 90 4a
2d 1d 4d 52 84 4c 40 a7 62 20 b1 1f a8 41 d3 ba b0 68 57 e8 00 c2 49 9e f5 73 ea e8 fd 95 e8 0f
39 29 7b 04 ec 34 09 a9 1f 51 72 cb 70 3a 3f 56 5d eb 1d 00 5d b7 8d d3 91 2f 83 38 70 dd 06 fb
68 62 ee 28 86 13 84 c5 de 39 82 10 2f 9f 8d ff ab 47 e7 e1 02 41 00 f3 17 c7 06 af 49 70 9b 55
0a ef fd 3c db 3a 6a 06 d8 ba ce 6f c6 9e d0 2b 31 79 3c a8 cf c4 b0 88 2c 0a c4 3b a4 20 10 b4
59 1c 52 c5 b2 52 55 7b a8 a0 64 10 de 69 da 7c 9b d8 84 c5 3e fc 0f 02 41 00 e3 1d 55 ca 19 8e
a3 af c9 5d 9f 74 cd 4a 56 10 69 60 44 df f9 77 fe 3a ad 10 00 35 48 60 0f 95 2f a0 7d b8 9f 6c
1a 33 9e d3 c8 7e 80 56 f7 bc db cf 9e c3 74 11 bc fd a0 8c d6 b8 34 7c 38 51 02 41 00 af ac 72
3f 29 73 98 36 18 da 23 9e cd 58 dc b8 fc a3 a9 34 40 60 b8 2a 55 dc 95 f1 b9 49 14 aa 42 6e 19
85 c0 58 16 78 1b ec fd e3 ef 4c b3 e5 64 cc f2 c3 fd d0 cd 8c 80 5a 9b b9 2f 56 1a 0f 02 41 00
ad af 36 77 6b 1a 19 76 0a 91 cd ab 1e 80 15 d7 51 2e ed 1d 38 04 1a e9 36 86 81 12 3e 7a 30 10
90 2e b5 56 a6 9c 9e 61 11 ba b6 9e 7f 79 82 d5 ec 68 17 eb 33 6d 89 51 91 21 83 e7 b5 43 b6 31
02 41 00 90 44 37 85 60 28 0b 55 67 c2 12 99 4e ea 58 09 37 c8 34 90 da 63 cd 24 58 4b 2e 17 55
60 65 35 74 d8 c0 10 a2 2c 89 a8 06 84 9c 6f c5 6e 3a a2 3b 35 23 00 d4 4e 93 16 8f 40 47 96 36
f8 4f e8
>>>


In the middle of line 5 I see ``03 01 00 01``, which I recognize as *e*.  (This is a different key than the ones we looked at before).  If you print out the components for reference:

.. sourcecode:: python

    > openssl rsa -text -in kf
    Private-Key: (1024 bit)
    modulus:
        00:d7:a9:f0:a3:47:4d:02:b4:4d:5c:0b:13:eb:b7: ..

and then compare, what you will find is

.. sourcecode:: bash

    30 82 
    02 5f 
    02 01 00
    02 81 81 *n*
    02 03 *e*
    02 81 81 *d*
    02 41 *p*
    02 41 *q*
    02 41 (all the other components)

Also, all the key components except *e* start with a leading ``00``.  I didn't find an example of ``02`` within a key component, but I might have missed it.  So the structure of each part is extremely simple, just ``02`` + id + ``00`` + data.  The last byte of the key data is the last byte of the "coefficient".

