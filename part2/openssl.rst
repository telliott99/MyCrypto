.. _openssl:

########################
Encryption using openssl
########################

**Key generation and basic usage**

In this  chapter we will go through an example of how to use public-key cryptography. Let’s explore a very simple method of file encryption working with ``ssh`` and ``openssl``. The demo uses OS X Terminal but it would be very similar on Linux.

The first step is to generate an RSA key pair.  We will use ``ssh-key`` for starters, something like:

.. sourcecode:: bash

    > ssh-keygen -C "name@host"

or perhaps

.. sourcecode:: bash

    > ssh-keygen -b 1024 -t rsa -f ./kf -N ""

The ``-C`` flag is for a comment (for convenience of the user only, not transmitted), 

``-t`` is the type of key.  Possible values are rsa and dsa and so on.  rsa means protocol version 2, whatever that is.  The default is rsa (version ???).

``-b`` is number of bits (the default for RSA is 2048).  There are plenty of other options, for example when converting between different key formats.  

.. sourcecode:: bash

    > ssh-keygen -b 1024 -t rsa -f ./kf -N "" -C "te"
    Generating public/private rsa key pair.
    Your identification has been saved in ./kf.
    Your public key has been saved in ./kf.pub.
    The key fingerprint is:
    ec:2e:44:ee:b0:fb:1f:f0:96:4f:9b:f1:99:f3:9c:e5 te
    The key's randomart image is:
    +--[ RSA 1024]----+
    |                 |
    |                 |
    |                 |
    |      ..         |
    |     o. S        |
    |    . o+ .       |
    |     =  * o     .|
    |    . oo + =.+ + |
    |    .o.oo + +o+ E|
    +-----------------+
    >

If the ``-f`` flag is not used, then ``ssh-keygen`` prompts for a file path to save the key.  In responding to the file save prompt, ``~`` is not expanded and will give an error.

If the ``-N`` flag isn't used, ``ssh-keygen`` will prompt for a passphrase which encrypts the private key against prying eyes.  It is possible to change the passphrase later (also with the ``-N`` flag)

``ssh-keygen`` has written two files to disk, a private key file called ``kf`` and a public key file called ``kf.pub``.  Look at the latter:

.. sourcecode:: bash

    > hexdump -C kf.pub
    00000000  73 73 68 2d 72 73 61 20  41 41 41 41 42 33 4e 7a  |ssh-rsa AAAAB3Nz|
    00000010  61 43 31 79 63 32 45 41  41 41 41 44 41 51 41 42  |aC1yc2EAAAADAQAB|
    00000020  41 41 41 41 67 51 43 7a  51 57 36 50 33 51 43 53  |AAAAgQCzQW6P3QCS|
    00000030  6e 50 33 44 39 48 47 55  77 34 45 4e 4d 49 41 68  |nP3D9HGUw4ENMIAh|
    00000040  50 62 38 57 6a 46 4f 67  4a 43 6e 73 5a 32 62 56  |Pb8WjFOgJCnsZ2bV|
    00000050  75 34 55 39 53 4e 42 7a  69 52 6e 55 30 41 6e 2b  |u4U9SNBziRnU0An+|
    00000060  47 41 57 56 51 38 71 49  44 30 38 47 30 30 65 7a  |GAWVQ8qID08G00ez|
    00000070  6c 78 4d 6e 73 59 59 43  59 52 43 74 78 4f 61 50  |lxMnsYYCYRCtxOaP|
    00000080  74 42 6a 6d 38 32 68 37  4a 68 32 6b 52 71 63 66  |tBjm82h7Jh2kRqcf|
    00000090  51 57 74 4a 6f 68 36 42  4b 6e 73 6c 72 78 58 48  |QWtJoh6BKnslrxXH|
    000000a0  58 4d 4a 35 39 56 59 2f  57 48 50 32 79 66 47 43  |XMJ59VY/WHP2yfGC|
    000000b0  49 2b 76 54 4d 45 32 33  6b 59 74 48 61 53 52 67  |I+vTME23kYtHaSRg|
    000000c0  4a 64 50 65 45 56 65 45  7a 77 36 70 49 64 75 39  |JdPeEVeEzw6pIdu9|
    000000d0  49 51 3d 3d 20 74 65 0a                           |IQ== te.|
    000000d8
    >

The comment comes after the key data, separated by a space, and there is a newline at the end (regardless of whether a comment is present).

To generate RSA keys for actual use, I would accept the default output file paths: ``~/.ssh/id rsa`` and ``~/.ssh/id rsa.pub``.  But instead, for this demo I’ve put them on the Desktop.

We can check the fingerprints like this:

.. sourcecode:: bash

    > ssh-keygen -lf kf
    1024 ec:2e:44:ee:b0:fb:1f:f0:96:4f:9b:f1:99:f3:9c:e5  te (RSA)
    > ssh-keygen -lf kf.pub
    1024 ec:2e:44:ee:b0:fb:1f:f0:96:4f:9b:f1:99:f3:9c:e5  te (RSA)
    >

No difference.

Now for an example.  The next step uses ``openssl``. This utility can do a lot of things, for example, it can compute hashes or digests. Here are some possible approaches

.. sourcecode:: bash

    > echo "hello world" | openssl sha1
    22596363b3de40b06f981fb85d82312e8c0ed511
    > echo "hello world" | md5
    6f5902ac237024bdd0c176cb93063dc4
    > openssl md5 <filename>

``openssl`` can also do ``base64`` encoding.

.. sourcecode:: bash

    > echo "hello world" | openssl base64 
    aGVsbG8gd29ybGQK
    >

Write this short message to a file:

.. sourcecode:: bash

    > echo "hello world" >  /Desktop/p.txt

.. sourcecode:: bash

    > openssl base64 -in p.txt -out b.txt
    > openssl base64 -d -in b.txt
    hello world
    > hexdump -C b.txt
    00000000  61 47 56 73 62 47 38 67  64 32 39 79 62 47 51 4b  |aGVsbG8gd29ybGQK|
    00000010  0a                                                |.|
    00000011
    >

http://en.wikipedia.org/wiki/Base64

For the demo, we will first use ``openssl`` to extract the public key from ``kf.pub`` and then convert it into PEM format.  since ``openssl`` prefers ``.pem`` this is the default:

.. sourcecode:: bash

    > openssl rsa -in kf -pubout -out kf.pem
    writing RSA key
    >

Let's compare the two public key files

``kf.pub``

.. sourcecode:: bash

    > hexdump -C kf.pub
    00000000  73 73 68 2d 72 73 61 20  41 41 41 41 42 33 4e 7a  |ssh-rsa AAAAB3Nz|
    00000010  61 43 31 79 63 32 45 41  41 41 41 44 41 51 41 42  |aC1yc2EAAAADAQAB|
    00000020  41 41 41 41 67 51 43 7a  51 57 36 50 33 51 43 53  |AAAAgQCzQW6P3QCS|
    00000030  6e 50 33 44 39 48 47 55  77 34 45 4e 4d 49 41 68  |nP3D9HGUw4ENMIAh|
    00000040  50 62 38 57 6a 46 4f 67  4a 43 6e 73 5a 32 62 56  |Pb8WjFOgJCnsZ2bV|
    00000050  75 34 55 39 53 4e 42 7a  69 52 6e 55 30 41 6e 2b  |u4U9SNBziRnU0An+|
    00000060  47 41 57 56 51 38 71 49  44 30 38 47 30 30 65 7a  |GAWVQ8qID08G00ez|
    00000070  6c 78 4d 6e 73 59 59 43  59 52 43 74 78 4f 61 50  |lxMnsYYCYRCtxOaP|
    00000080  74 42 6a 6d 38 32 68 37  4a 68 32 6b 52 71 63 66  |tBjm82h7Jh2kRqcf|
    00000090  51 57 74 4a 6f 68 36 42  4b 6e 73 6c 72 78 58 48  |QWtJoh6BKnslrxXH|
    000000a0  58 4d 4a 35 39 56 59 2f  57 48 50 32 79 66 47 43  |XMJ59VY/WHP2yfGC|
    000000b0  49 2b 76 54 4d 45 32 33  6b 59 74 48 61 53 52 67  |I+vTME23kYtHaSRg|
    000000c0  4a 64 50 65 45 56 65 45  7a 77 36 70 49 64 75 39  |JdPeEVeEzw6pIdu9|
    000000d0  49 51 3d 3d 20 74 65 0a                           |IQ== te.|
    000000d8
    >

``kf.pem``

.. sourcecode:: bash

    > hexdump -C kf.pem
    00000000  2d 2d 2d 2d 2d 42 45 47  49 4e 20 50 55 42 4c 49  |-----BEGIN PUBLI|
    00000010  43 20 4b 45 59 2d 2d 2d  2d 2d 0a 4d 49 47 66 4d  |C KEY-----.MIGfM|
    00000020  41 30 47 43 53 71 47 53  49 62 33 44 51 45 42 41  |A0GCSqGSIb3DQEBA|
    00000030  51 55 41 41 34 47 4e 41  44 43 42 69 51 4b 42 67  |QUAA4GNADCBiQKBg|
    00000040  51 43 7a 51 57 36 50 33  51 43 53 6e 50 33 44 39  |QCzQW6P3QCSnP3D9|
    00000050  48 47 55 77 34 45 4e 4d  49 41 68 0a 50 62 38 57  |HGUw4ENMIAh.Pb8W|
    00000060  6a 46 4f 67 4a 43 6e 73  5a 32 62 56 75 34 55 39  |jFOgJCnsZ2bVu4U9|
    00000070  53 4e 42 7a 69 52 6e 55  30 41 6e 2b 47 41 57 56  |SNBziRnU0An+GAWV|
    00000080  51 38 71 49 44 30 38 47  30 30 65 7a 6c 78 4d 6e  |Q8qID08G00ezlxMn|
    00000090  73 59 59 43 59 52 43 74  78 4f 61 50 0a 74 42 6a  |sYYCYRCtxOaP.tBj|
    000000a0  6d 38 32 68 37 4a 68 32  6b 52 71 63 66 51 57 74  |m82h7Jh2kRqcfQWt|
    000000b0  4a 6f 68 36 42 4b 6e 73  6c 72 78 58 48 58 4d 4a  |Joh6BKnslrxXHXMJ|
    000000c0  35 39 56 59 2f 57 48 50  32 79 66 47 43 49 2b 76  |59VY/WHP2yfGCI+v|
    000000d0  54 4d 45 32 33 6b 59 74  48 61 53 52 67 0a 4a 64  |TME23kYtHaSRg.Jd|
    000000e0  50 65 45 56 65 45 7a 77  36 70 49 64 75 39 49 51  |PeEVeEzw6pIdu9IQ|
    000000f0  49 44 41 51 41 42 0a 2d  2d 2d 2d 2d 45 4e 44 20  |IDAQAB.-----END |
    00000100  50 55 42 4c 49 43 20 4b  45 59 2d 2d 2d 2d 2d 0a  |PUBLIC KEY-----.|
    00000110
    >

The data is base64.  Because the two formats differ, the data is different in part (but quite similar in other parts).  We'll look more closely at the formats in a future chapter.

I forgot to provide a destination file the first time.  To show you what happened, I saved the original ``kf.pub`` and then redid everything from the start.  Here is what I got

.. sourcecode:: bash

    > openssl rsa -in kf -pubout
    writing RSA key
    -----BEGIN PUBLIC KEY-----
    MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQDVM7H49oOkFpmWQA5Nf8qIJnHT
    HTvvG1STTALd0aViJeo0LVa0NggWAsTAzWJkv8kIBmO4E7Y2vtbGXS1k+xNa4Wix
    M79J1s7/jhcHstJjOWe5YBF4sjDAPBg1qqXuoFAabbtGXj5KERXxEbBB3ad8M6V5
    87WDat81/wE3rbO0QQIDAQAB
    -----END PUBLIC KEY-----
    >

No file was written because I didn't provide ``-out``, but this is clearly just ``kf.pem``.

Note that it is not necessary to use ``hexdump``.  One can print the contents in a nice way.  To view the key elements inside the private key:

.. sourcecode:: bash

    > openssl rsa -text -in kf
    Private-Key: (1024 bit)
    modulus:
        00:b3:41:6e:8f:dd:00:92:9c:fd:c3:f4:71:94:c3:
        81:0d:30:80:21:3d:bf:16:8c:53:a0:24:29:ec:67:
        66:d5:bb:85:3d:48:d0:73:89:19:d4:d0:09:fe:18:
        05:95:43:ca:88:0f:4f:06:d3:47:b3:97:13:27:b1:
        86:02:61:10:ad:c4:e6:8f:b4:18:e6:f3:68:7b:26:
        1d:a4:46:a7:1f:41:6b:49:a2:1e:81:2a:7b:25:af:
        15:c7:5c:c2:79:f5:56:3f:58:73:f6:c9:f1:82:23:
        eb:d3:30:4d:b7:91:8b:47:69:24:60:25:d3:de:11:
        57:84:cf:0e:a9:21:db:bd:21
    publicExponent: 65537 (0x10001)
    privateExponent:
        0e:f5:6d:e1:89:82:cb:b9:58:1f:eb:1d:33:59:e1:
        42:15:83:0b:c3:18:58:2c:5b:aa:28:7a:6b:24:f1:
        da:f2:2c:1b:42:21:4b:12:ec:d9:ea:86:7a:f2:cc:
        3c:79:8c:c4:2f:ea:db:59:f4:48:d3:59:a0:dd:5a:
        9e:86:35:1a:f7:44:dc:bd:ff:44:97:fa:c5:15:bd:
        36:a3:01:a1:f4:9a:e2:9d:08:55:b1:35:54:76:6d:
        e8:ee:b2:d7:c6:84:12:a4:c8:8c:6e:3a:b5:ec:ce:
        6e:80:d5:c6:b9:f2:24:bf:67:02:00:13:91:0c:99:
        aa:db:d3:9b:bd:ea:f7:71
    prime1:
        00:ea:df:cf:4e:a1:65:54:c8:5c:b4:45:6a:99:1e:
        85:de:d4:2e:a6:16:df:47:76:c5:8d:ca:68:a6:c3:
        e4:e9:f2:33:c1:dc:82:b6:0c:0e:75:4b:3f:b7:81:
        18:fc:39:0f:58:51:f9:20:da:06:6a:a0:2d:92:99:
        14:99:62:ee:35
    prime2:
        00:c3:60:f3:d8:a9:fc:63:88:fd:fb:67:35:c8:4b:
        bf:b5:f7:0d:e1:b9:b5:31:8f:e1:f1:88:10:8e:c7:
        5f:32:6f:d5:6f:c7:18:63:83:25:28:a4:72:5d:7f:
        13:b6:8f:d5:99:a8:29:5e:1f:00:c9:ee:16:0d:f4:
        b0:08:46:60:bd
    exponent1:
        72:77:c9:4d:05:13:a1:92:54:bb:f6:e8:d0:df:33:
        57:3a:09:d2:20:6b:89:24:b5:7b:39:1e:6f:c8:21:
        14:73:5a:0e:2d:2d:f7:13:41:28:a1:17:d8:93:2e:
        5e:1e:61:00:26:53:48:53:79:b5:15:83:a0:62:c2:
        cb:4e:8f:d1
    exponent2:
        00:b0:e2:e8:22:32:d4:04:31:94:f0:b5:a2:a5:b2:
        9e:e0:d9:c9:c1:a1:66:80:76:a9:b3:08:e3:24:c1:
        30:58:f3:93:23:5d:f7:a0:b0:ad:45:bc:8c:a6:45:
        54:cd:a6:2f:56:ac:3e:b7:ae:0e:02:c4:01:47:a5:
        4e:72:4f:75:69
    coefficient:
        00:b9:1f:9c:65:81:00:bc:61:34:96:a4:fb:04:1c:
        6c:7d:2b:f4:57:72:88:ca:7b:75:02:5f:bc:83:71:
        e3:af:2e:f7:6d:5e:ef:79:3d:94:6c:d1:86:10:f2:
        47:0a:49:c4:3e:bd:9f:50:ec:bc:da:9b:8b:c2:0c:
        fc:68:5c:79:2f
    writing RSA key
    -----BEGIN RSA PRIVATE KEY-----
    MIICXQIBAAKBgQCzQW6P3QCSnP3D9HGUw4ENMIAhPb8WjFOgJCnsZ2bVu4U9SNBz
    iRnU0An+GAWVQ8qID08G00ezlxMnsYYCYRCtxOaPtBjm82h7Jh2kRqcfQWtJoh6B
    KnslrxXHXMJ59VY/WHP2yfGCI+vTME23kYtHaSRgJdPeEVeEzw6pIdu9IQIDAQAB
    AoGADvVt4YmCy7lYH+sdM1nhQhWDC8MYWCxbqih6ayTx2vIsG0IhSxLs2eqGevLM
    PHmMxC/q21n0SNNZoN1anoY1GvdE3L3/RJf6xRW9NqMBofSa4p0IVbE1VHZt6O6y
    18aEEqTIjG46tezOboDVxrnyJL9nAgATkQyZqtvTm73q93ECQQDq389OoWVUyFy0
    RWqZHoXe1C6mFt9HdsWNymimw+Tp8jPB3IK2DA51Sz+3gRj8OQ9YUfkg2gZqoC2S
    mRSZYu41AkEAw2Dz2Kn8Y4j9+2c1yEu/tfcN4bm1MY/h8YgQjsdfMm/Vb8cYY4Ml
    KKRyXX8Tto/VmagpXh8Aye4WDfSwCEZgvQJAcnfJTQUToZJUu/bo0N8zVzoJ0iBr
    iSS1ezkeb8ghFHNaDi0t9xNBKKEX2JMuXh5hACZTSFN5tRWDoGLCy06P0QJBALDi
    6CIy1AQxlPC1oqWynuDZycGhZoB2qbMI4yTBMFjzkyNd96CwrUW8jKZFVM2mL1as
    PreuDgLEAUelTnJPdWkCQQC5H5xlgQC8YTSWpPsEHGx9K/RXcojKe3UCX7yDceOv
    LvdtXu95PZRs0YYQ8kcKScQ+vZ9Q7Lzam4vCDPxoXHkv
    -----END RSA PRIVATE KEY-----
    >

**Encryption**

Now to finally encrypt our text using ``openssl rsautl``:

.. sourcecode:: bash

    echo "hello world" | openssl rsautl -encrypt -pubin -inkey kf.pem > c.txt
    
The ``-pubin`` option means to encrypt with the public key.  

We can also specify the input and output files like this:

.. sourcecode:: bash

    openssl rsautl -encrypt -in p.txt -out c.txt -pubin -inkey kf.pem
    
Take a look

.. sourcecode:: bash

    > echo "hello world" | openssl rsautl -encrypt -pubin -inkey kf.pem > c.txt
    > hexdump -C c.txt
    00000000  79 36 69 6d 7c 9d 95 0f  61 6a 6d 1a d1 3a 99 d3  |y6im|...ajm..:..|
    00000010  af ca 24 a2 b3 2b d4 48  28 23 44 56 4a c0 79 36  |..$..+.H(#DVJ.y6|
    00000020  3f 8b cd cd 90 d7 3f 23  34 eb f4 b6 95 b2 2b 98  |?.....?#4.....+.|
    00000030  e1 e9 9b fd 1e 5b 91 23  fc 3c 2b 15 fa 8e 04 62  |.....[.#.<+....b|
    00000040  04 0f 8f 17 d9 d3 3d f2  53 98 74 7b 80 49 66 9f  |......=.S.t{.If.|
    00000050  a1 01 a6 df 2b 33 92 53  ee aa 28 96 6e a5 0f 04  |....+3.S..(.n...|
    00000060  74 3a 7b 71 55 c7 11 12  9c c9 c2 98 22 16 38 2c  |t:{qU.......".8,|
    00000070  79 b8 a1 05 dd 33 fa ca  e2 d0 18 2f 33 1b 48 bf  |y....3...../3.H.|
    00000080
    >

Decrypt with the private key

.. sourcecode:: bash

    > openssl rsautl -decrypt -in c.txt -inkey kf
    hello world
    >
    
If a passphrase is used to protect ``kf``, you will be prompted for it.
    
Of course, we can also use the keys the other way around, first encrypting with the private key and then decrypting with the public one:

These options are called ``-sign`` and ``-verify``

.. sourcecode:: bash

    > echo "hello world" > p.txt
    > openssl rsautl -sign -in p.txt -out c.txt -inkey kf
    > hexdump -C c.txt
    00000000  7a aa b7 d3 88 28 b8 a6  40 f5 0a d8 0b fc 2f bd  |z....(..@...../.|
    00000010  e7 7f 35 9f 36 19 85 eb  65 5b 25 34 ee 69 60 e8  |..5.6...e[%4.i`.|
    00000020  fc 23 40 cc 53 54 48 fe  56 1c 22 7a 9f 33 de 5d  |.#@.STH.V."z.3.]|
    00000030  d3 4b 4f 94 26 df d4 5c  4f 7d 11 e5 3e 6f 0d 09  |.KO.&..\O}..>o..|
    00000040  31 12 1f 32 b7 e2 39 c1  05 10 88 8c 2b 62 4d 85  |1..2..9.....+bM.|
    00000050  d2 65 1a 0d 50 c7 48 c0  14 6f bd 26 41 f9 73 72  |.e..P.H..o.&A.sr|
    00000060  d8 f1 2d 1d 6c c6 34 09  34 dd 6e 3f 77 68 ed a4  |..-.l.4.4.n?wh..|
    00000070  ed d0 e5 ee 78 90 44 6a  fd 1d dc 6f e8 62 cc 01  |....x.Dj...o.b..|
    00000080
    > openssl rsautl -verify -in c.txt -pubin -inkey kf.pem
    hello world
    >

**Encrypting more data**

With a larger message to encrypt, we have to be more sophisticated

http://www.czeskis.com/random/openssl-encrypt-file.html

We generate 256 random bytes (the article I'm following does it in two steps, so that’s what we’ll do:

.. sourcecode:: bash

    cat k1.bin k2.bin > key.bin

To encrypt using AES with 256 bits and CBC mode:

.. sourcecode:: bash

    openssl enc -aes-256-cbc -salt -in p.txt -out c.txt -pass file:./key.bin
    
To decrypt:

.. sourcecode:: bash

    > openssl enc -d -aes-256-cbc -in c.txt -out m.txt -pass file:./key.bin
    > cat m.txt
    hello world
    >
    
In practice, use the RSA key to encrypt this key before sending it to your cohort, and find a way to bundle the cipher text and the encrypted key together.

You should also verify the digest (hash) of the data you send, or sign it with your private key (see above).  I have written quite a bit about the structure of RSA key files. See:

http://telliott99.blogspot.com/2011/08/dissecting-rsa-keys-in-python.html

There are four posts, and I explore the use of Python modules to do encryption.