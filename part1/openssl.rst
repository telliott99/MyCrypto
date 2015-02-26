.. _openssl:

#####################
Example using openssl
#####################

**Key generation and basic usage**

In this  chapter we will go through an example of using public-key cryptography. Let’s explore a very simple method of file encryption using ``ssh`` and ``openssl``. The demo uses OS X Terminal but it would be very similar on Linux.

The first step is to generate an RSA key pair. Normally one would do something like:

.. sourcecode:: bash

    > ssh-keygen -C "name@host"

or perhaps

.. sourcecode:: bash

    > ssh-keygen -t rsa -f ./kf

The ``-C`` flag marks a comment (for convenience of the user only, not transmitted), ``-t`` is the type of key, ``-b`` is number of bits (the default for RSA is 2048), and ``-m`` is the format (the default is RFC4716 but PEM is also an option).  

``ssh-keygen`` prompts for a file path to save the key, and a passphrase which encrypts the private key against prying eyes.

.. sourcecode:: bash

    > ssh-keygen -t rsa -C "te" -f ./kf
    Generating public/private rsa key pair.
    ./kf already exists.
    Overwrite (y/n)? y
    Enter passphrase (empty for no passphrase): 
    Enter same passphrase again: 
    Your identification has been saved in ./kf.
    Your public key has been saved in ./kf.pub.
    The key fingerprint is:
    be:40:2a:4f:a6:f3:87:09:4d:b3:7b:09:d1:e7:7c:f6 te
    The key's randomart image is:
    +--[ RSA 2048]----+
    |                 |
    |                 |
    |     .           |
    |    + . .        |
    |   o +.+S        |
    |  . +o .o o      |
    |  ..+=...o .     |
    |  .*+ +. .  E    |
    |  .ooo  .        |
    +-----------------+
    >

.. sourcecode:: bash

    > hexdump -C kf.pub
    00000000  73 73 68 2d 72 73 61 20  41 41 41 41 42 33 4e 7a  |ssh-rsa AAAAB3Nz|
    00000010  61 43 31 79 63 32 45 41  41 41 41 44 41 51 41 42  |aC1yc2EAAAADAQAB|
    ..
    00000160  71 39 4f 44 78 48 51 50  30 61 49 79 2b 69 36 55  |q9ODxHQP0aIy+i6U|
    00000170  74 4c 45 57 75 50 5a 55  44 72 57 78 20 74 65 0a  |tLEWuPZUDrWx te.|
    00000180
    >

The comment is set off from the key data by a space, and there is a newline at the end (regardless of whether a comment is present).

If I were generating RSA keys for actual use, I would write them to the default file paths: ``~/.ssh/id rsa`` and ``~/.ssh/id rsa.pub``.  But instead, for this demo I’ve put them on the Desktop.

This produces two files: ``kf`` and ``kf.pub``.  We can check the fingerprint like this:

.. sourcecode:: bash

    ssh-keygen -lf kf
    
The output is:

.. sourcecode:: bash

    > ssh-keygen -lf kf
    2048 be:40:2a:4f:a6:f3:87:09:4d:b3:7b:09:d1:e7:7c:f6  te (RSA)
    >

Now for an example.  The next step uses ``openssl``. This utility can do a lot of things, for example, digests. Here are some possible approaches

.. sourcecode:: bash

    > echo "hello world" | openssl sha1
    22596363b3de40b06f981fb85d82312e8c0ed511
    > echo "hello world" | md5
    6f5902ac237024bdd0c176cb93063dc4
    >

Or

.. sourcecode:: bash

    openssl md5 <filename>

``openssl`` can also do ``base64`` encoding.  We write this short message to a file:

.. sourcecode:: bash

    echo "hello world" >  /Desktop/p.txt

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

For the demo, we first use ``openssl`` to output the public key in PEM format:

.. sourcecode:: bash

    > openssl rsa -in kf -pubout 
    writing RSA key
    -----BEGIN PUBLIC KEY-----
    MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAsBP9orAaH3wzd6Znrqxt
    ddlwr4f4sDGEexXhC/aZryZXm/J0euQrewgBLukzP8AlQgsYuLT6oBRclHnbWfKX
    NYH+jliPCgvtmuTeHOJH36njuwHHhXQtklIrtlEkvmZI+ZpxRiuALFT4eDUSXvIs
    d3RwdqdATfIbvRN5upUzMJIJMnEdFZ6VzEUNCuN/l7oznimZJyvetS9nEX44zfPE
    /nea3LcR0RQMrRlWpE7g1HVaGzcTAulnVlb+wF1T+/vkdx7zmgZhFe2ivzI9OxcY
    mE+5K0poPNev1xoVJDsyXsKHF+p5Yq3aYsb5f5amZ1sSLxV8hIv4JsgNJebtQQQa
    BQIDAQAB
    -----END PUBLIC KEY-----
    > openssl rsa -in kf -pubout > kf.pem
    writing RSA key
    >

Now encrypt encrypt our text using ``openssl rsautl``:

.. sourcecode:: bash

    cat p.txt | openssl rsautl -encrypt -pubin -inkey kf.pem > c.txt
    
The ``-pubin`` option means to encrypt with the public key.  

We can also specify the input and output files like this:

.. sourcecode:: bash

    openssl rsautl -encrypt -in p.txt -out c.txt -pubin -inkey kf.pem
    
Take a look

.. sourcecode:: bash

    > cat p.txt | openssl rsautl -encrypt -pubin -inkey kf.pem > c.txt
    > hexdump -C c.txt
    00000000  9e fc a6 9a ad ed dc a1  59 55 5f c5 ef 60 cc a3  |........YU_..`..|
    00000010  48 b9 81 12 ed 56 8b b4  8f c0 cd dc e9 97 67 ab  |H....V........g.|
    00000020  92 cf 83 79 74 a4 e3 38  66 6c 30 8f db 08 4c 08  |...yt..8fl0...L.|
    00000030  db 6f 3f 70 c9 b6 b4 b1  13 29 5b e1 9c 5c c7 ab  |.o?p.....)[..\..|
    00000040  a2 24 97 5a 0b ab c2 78  5e 88 1a 52 a3 9f 14 e3  |.$.Z...x^..R....|
    00000050  89 1f 9d 46 f6 cb 84 e2  dc 49 4a 2f 77 a3 2b 54  |...F.....IJ/w.+T|
    00000060  fd a6 88 2b a3 ea 76 cc  b9 d1 66 61 38 ac 1a d7  |...+..v...fa8...|
    00000070  23 d7 d5 94 0c 46 98 6a  b4 45 fd 7c 5c 01 92 de  |#....F.j.E.|\...|
    00000080  c5 a5 fa f4 c9 c2 4d fd  d3 7f d6 64 72 a8 87 3e  |......M....dr..>|
    00000090  30 ec 9a 6b 87 a5 e8 35  bc f5 fe 28 8a 13 94 c5  |0..k...5...(....|
    000000a0  97 1d 62 1b 6c fa b7 90  97 47 ae f5 4f 20 b9 54  |..b.l....G..O .T|
    000000b0  86 89 a7 b2 55 55 ef d5  4f ed cc 84 21 1b b6 62  |....UU..O...!..b|
    000000c0  be f2 ff b6 78 d8 84 1f  fc 51 49 cf 31 14 ee cd  |....x....QI.1...|
    000000d0  cf 7d 5f 40 07 1d b4 42  00 51 07 0b ea 81 81 44  |.}_@...B.Q.....D|
    000000e0  16 e1 44 2c 2d 41 3e f0  ac c1 44 83 7a 50 08 21  |..D,-A>...D.zP.!|
    000000f0  39 9c f8 c2 06 5a 47 75  7b 0f 00 7b 04 f7 df 12  |9....ZGu{..{....|
    00000100
    >

Decrypt with the private key

.. sourcecode:: bash

    > openssl rsautl -decrypt -in c.txt -inkey kf
    hello world
    >
    
If a passphrase is used to protect ``kf``, you will be prompted for it.
    
We can also use the keys the other way around, encrypting with the private key and decrypting with the public one:

These options are called ``-sign`` and ``-verify``

.. sourcecode:: bash

    > openssl rsautl -sign -in p.txt -out c.txt -inkey kf
    > openssl rsautl -verify -in c.txt -pubin -inkey kf.pem
    hello world
    >

**Encrypting more data**

With a larger message to encrypt, we have to be more sophisticated

http://www.czeskis.com/random/openssl-encrypt-file.html

We generate 256 random bytes (the article I'm following does it in two steps, so that’s what we’ll do:

.. sourcecode:: bash

    openssl rand 128 > k1.bin
    openssl rand 128 > k2.bin
    cat k1.bin k2.bin > k.bin

To encrypt using AES with 256 bits and CBC mode:

.. sourcecode:: bash

    openssl enc -aes-256-cbc -salt -in p.txt -out c.txt -pass file:./k.bin
    
To decrypt:

.. sourcecode:: bash

    openssl enc -d -aes-256-cbc -in c.txt -out m.txt -pass file:./key.bin

In practice, use the RSA key to send this key to your cohort.

You should also verify the digest (hash) of the data you send, or sign it with your private key (see above).  I have written quite a bit about the structure of RSA key files. See:

http://telliott99.blogspot.com/2011/08/dissecting-rsa-keys-in-python.html

There are four posts, and I explore the use of Python modules to do encryption.