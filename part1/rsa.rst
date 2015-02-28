.. _rsa:

#################
Python rsa module
#################

The Python ``rsa`` module can be installed using ``pip``

.. sourcecode:: bash

    pip install rsa

It is a pure-Python RSA implementation.

http://stuvel.eu/rsa

>>> import rsa
>>> rsa.__version__
'3.1.4'
>>> 

Given *e*,*n*,*p*,*q* and *d*, create new key objects.

Recall:

``x.py``:

.. sourcecode:: python

    def egcd(a, b):
        if a == 0:
            return (b, 0, 1)
        else:
            g, y, x = egcd(b \% a, a)
            return (g, x - (b // a) * y, y)
            
    def modinv(a, m):
        g, x, y = egcd(a, m)
        if g != 1:
            raise Exception("modular inverse does not exist")
        else:
            return x % m

Use it like so:

>>> import rsa
>>> rsa.__version__
'3.1.4'
>>> e = 65537
>>> p = 4169414332984308880603L
>>> q = 7602535963858869797L
>>> n = p*q
>>> n
31698122414741849421263704398157795847591L

>>> import x
>>> phi = (p-1)*(q-1)
>>> phi
31698122414741849417086687529209628097192L
>>> d = x.modinv(e,phi)
>>> d
7506520894712811128876594754922157377793L
>>> d*e % phi
1L
>>> 

>>> pub_key = rsa.PublicKey(n,e)
>>> k = pub_key.save_pkcs1()
>>> print k
-----BEGIN RSA PUBLIC KEY-----
MBgCEV0nBFBeZSvDWvZZHnKFuG2nAgMBAAE=
-----END RSA PUBLIC KEY-----

>>>

Add this to ``x.py`` (and repeat the import), or just paste it into the interpreter

.. sourcecode:: bash

    import base64

    def f(input):
        data = base64.b64decode(input)
        print `data`
        L = [ord(b) for b in data]
        print L
        for i in range(0,len(L),32):
            print ' '.join([hex(h)[2:].zfill(2) for h in L[i:i+32]])


>>> f('MBgCEV0nBFBeZSvDWvZZHnKFuG2nAgMBAAE=')
..
30 18 02 11 5d 27 04 50 5e 65 2b c3 5a f6 59 1e 72 85 b8 6d a7 02 03 01 00 01
>>>

As we saw when looking at the private key, there is a two byte header (``48 24``), then, using ``02`` as a spacer, we have the byte ``11`` (decimal 17) at position 4 as a size marker for the following 17 bytes before we recognize the spacer and then *e* as ``03 01 00 01``.  To see *n*, copy the relevant data:

>>> s = '5d 27 04 50 5e 65 2b c3 5a f6 59 1e 72 85 b8 6d a7'
>>> s = ''.join(s.split())
>>> int('0x' + s, 16)
31698122414741849421263704398157795847591L
>>>

>>> n
31698122414741849421263704398157795847591L

Matches.

Similarly we can construct a private key

>>> pri_key = rsa.PrivateKey(n=n,e=e,p=p,q=q,d=d)
>>> pri_key
PrivateKey(31698122414741849421263704398157795847591, 65537, 7506520894712811128876594754922157377793, 4169414332984308880603, 7602535963858869797)
>>> s = pri_key.save_pkcs1()
>>> print s
-----BEGIN RSA PRIVATE KEY-----
MGQCAQACEV0nBFBeZSvDWvZZHnKFuG2nAgMBAAECERYPR1ZBBHR4eVJmddE8ywkB
AgoA4gY/VVhn+VTbAghpgaIt3fCeJQIJDBWpbTa82GfhAgg5UqRh1T7BPQIJQffe
wQcxQ9E5
-----END RSA PRIVATE KEY-----

>>>

matching

>>> e = 65537
>>> p = 4169414332984308880603L
>>> q = 7602535963858869797L
>>> n = p*q
>>> n
31698122414741849421263704398157795847591L
>>> d
7506520894712811128876594754922157377793L

The order is *n* *e* *d* *p* *q*.

The keys in the above example are too short and will throw an error.  

>>> msg = 'hello Bob'
>>> crypto = rsa.encrypt(msg, pub_key)
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
  File "/usr/local/lib/python2.7/site-packages/rsa/pkcs1.py", line 166, in encrypt
    padded = _pad_for_encryption(message, keylength)
  File "/usr/local/lib/python2.7/site-packages/rsa/pkcs1.py", line 83, in _pad_for_encryption
    ' space for %i' % (msglength, max_msglength))
OverflowError: 9 bytes needed for message, but there is only space for 6


So let's make a new pair:

>>> (pub,pri) = rsa.newkeys(512)
>>> crypto = rsa.encrypt(msg, pub)
>>> print rsa.decrypt(crypto,pri)
hello Bob
>>>

Pretty easy!

We can write them to disk just like any data:

>>> FH = open('kf.pub','w')
>>> FH.write(pub.save_pkcs1())
>>> FH.close()
>>> FH = open('kf','w')
>>> FH.write(pri.save_pkcs1())
>>> FH.close()
>>>

And from the command line:

.. sourcecode:: bash

    > openssl rsa -text -in kf
    Private-Key: (512 bit)
    modulus:
        00:82:18:3e:87:2f:d4:d7:c9:8c:25:f3:f1:43:f2:
        bb:91:a2:d5:be:7e:39:17:8e:07:43:b9:55:e7:0a:
        4b:f9:90:f4:e6:d9:a9:3f:d8:66:71:42:ca:ec:64:
        e7:8f:49:22:1a:d1:77:44:c3:d4:4c:fa:0e:2f:a1:
        fd:0f:d5:40:0d
    publicExponent: 65537 (0x10001)
    privateExponent:
        74:fb:3e:06:ab:e1:15:64:fb:ac:09:0e:53:0e:4a:
        d1:eb:7d:8e:3c:cc:33:bd:18:15:32:eb:e6:c4:5f:
        c8:3e:f2:a6:4f:ed:84:3c:68:79:ad:53:f3:73:a9:
        e5:0f:ac:03:fd:1e:2e:ee:4c:05:81:ee:04:22:a8:
        72:16:dc:01
    prime1:
        00:d8:8f:ab:d6:fe:b7:f1:27:53:2e:ac:dc:5a:b7:
        f8:de:08:36:23:9a:68:db:d1:9a:2d:db:08:4a:24:
        3d:61:95:bd:0d
    prime2:
        00:99:c9:68:0d:7b:c0:78:02:f9:5c:7d:ea:d8:40:
        4e:a1:4c:5d:61:55:d9:bf:27:ed:74:8d:df:6a:cf:
        01
    exponent1:
        08:9a:cc:cd:22:19:d4:ef:27:12:f7:b3:59:b7:6d:
        a0:04:db:81:d6:a4:cb:f7:2c:15:1e:5a:d9:f7:4e:
        a9:0d:f6:11
    exponent2:
        17:bf:4a:1a:0a:ea:05:9e:2f:f3:60:5e:4b:56:62:
        cd:f5:84:d5:ea:f3:dc:d8:c5:8a:21:fe:45:f8:01
    coefficient:
        60:d1:d9:f7:a2:a0:55:11:2f:7f:54:47:67:2e:67:
        44:fa:21:cd:00:60:d0:ab:bb:7b:1a:8e:7c:d7:77:
        11:fb:7c:a5
    writing RSA key
    -----BEGIN RSA PRIVATE KEY-----
    MIIBOwIBAAJBAIIYPocv1NfJjCXz8UPyu5Gi1b5+OReOB0O5VecKS/mQ9ObZqT/Y
    ZnFCyuxk549JIhrRd0TD1Ez6Di+h/Q/VQA0CAwEAAQJAdPs+BqvhFWT7rAkOUw5K
    0et9jjzMM70YFTLr5sRfyD7ypk/thDxoea1T83Op5Q+sA/0eLu5MBYHuBCKochbc
    AQIjANiPq9b+t/EnUy6s3Fq3+N4INiOaaNvRmi3bCEokPWGVvQ0CHwCZyWgNe8B4
    AvlcferYQE6hTF1hVdm/J+10jd9qzwECIgiazM0iGdTvJxL3s1m3baAE24HWpMv3
    LBUeWtn3TqkN9hECHhe/ShoK6gWeL/NgXktWYs31hNXq89zYxYoh/kX4AQIiYNHZ
    96KgVREvf1RHZy5nRPohzQBg0Ku7exqOfNd3Eft8pQ==
    -----END RSA PRIVATE KEY-----
    >

Convert the public key to ``SSL`` format

.. sourcecode:: bash

    > openssl rsa -in kf -pubout > kf.pem
    writing RSA key

Encrypt and decrypt

.. sourcecode:: bash

    > echo "hello world" | openssl rsautl -encrypt -pubin -inkey kf.pem > c.txt
    > openssl rsautl -decrypt -in c.txt -inkey kf
    hello world
    >

**Reading key files with the rsa module**

.. sourcecode:: bash

    > ssh-keygen -b 1024 -t rsa -f ./kf -N "" -C "te"
    > openssl rsa -in kf -pubout > kf.pem
    writing RSA key
    >

>>> rsa
>>> pub = rsa.PublicKey.load_pkcs1('kf.pub')
>>> pub = rsa.PublicKey.load_pkcs1('kf.pem')

Both of these calls fail, as is.  The manual:

    load_pkcs1(keyfile, format='PEM')
    Loads a key in PKCS#1 DER or PEM format.

    Parameters:	
    keyfile – contents of a DER- or PEM-encoded file that contains the public key.
    format – the format of the file to load; ‘PEM’ or ‘DER’
    Returns:	
    a PublicKey object

According to the interoperability page of the manual, what we need to do is:

    The standard PKCS#8 is widely used, and more complex than the PKCS#1 v1.5 supported by Python-RSA. In order to extract a key from the PKCS#8 format you need an external tool such as OpenSSL

.. sourcecode:: bash

    > openssl rsa -in kf -out kf.pkcs1.pem
    writing RSA key
    > pyrsa-priv2pub -i kf.pkcs1.pem -o kf.pub.pkcs1.pem
    Reading private key from kf.pkcs1.pem in PEM format
    Writing public key to kf.pub.pkcs1.pem in PEM format
    >

More to do here, still not working