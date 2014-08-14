.. _openssl:

#####################
Example using openssl
#####################

**Key generation and basic usage**

In this  chapter we will go through an example of using public-key cryptography. Let’s explore a very simple method of file encryption using ``ssh`` and ``openssl``. The demo uses OS X Terminal but it would be very similar on Linux.

The first step is to generate an RSA key pair. Normally one would do something like:

.. sourcecode:: bash

    ssh-keygen -t rsa -C "name@host"

Here ``-C`` is a comment (for convenience of the user only, not transmitted), ``-t`` is the type of key, ``-b`` is number of bits (the default for RSA is 2048), and ``-m`` is the format (the default is RFC4716 but PEM is also an option).

If I were generating RSA keys for actual use, I would write them to the default filepaths: ``~/.ssh/id rsa`` and ``~/.ssh/id rsa.pub``.  But instead, for this demo I’m going to put them on the Desktop.  This first step generates only the private key:

.. sourcecode:: bash

    ssh-keygen -t rsa -C "te" -f ./kf
    
At the prompt, I can enter a passphrase: ``abcde``.  This is not strictly necessary.  The purpose is to protect the private (secret) keyfile on your machine, by encrypting it.

This produces two files: ``kf`` and ``kf.pub``.  We can check the fingerprint like this:

.. sourcecode:: bash

    ssh-keygen -lf kf
    
The output is:

.. sourcecode:: bash

    2048 05:f4:3a:1d:b6:48:7e:2f:1f:e5:a0:c7:bd:c6:bc:d8 te (RSA)

Now for an example.  The next step uses ``openssl``. This utility can do a lot of things, for example, digests. Here are some possible approaches

.. sourcecode:: bash

    echo "hello world" | openssl sha1
    echo "hello world" | openssl md5
    openssl md5 ./p.txt
    
.. sourcecode:: bash

    $ openssl md5 ~/Desktop/p.txt
    MD5(/Users/telliott_admin/Desktop/p.txt)= 6f5902ac237024bdd0c176cb93063dc4

``openssl`` can also do ``base64`` encoding: 

.. sourcecode:: bash

    openssl base64 -in p.txt -out b.txt
    openssl base64 -d -in b.txt
    
http://en.wikipedia.org/wiki/Base64

We first use it to output the public key in PEM format:

.. sourcecode:: bash

    openssl rsa -in kf -pubout > ./kf.pem

Now we write this short message to a file:

.. sourcecode:: bash

    echo "hello world" >  /Desktop/p.txt

and encrypt it

.. sourcecode:: bash

    cat p.txt | openssl rsautl -encrypt -pubin -inkey kf.pem > c.txt
    
The ``-pubin`` option means to encrypt with the public key.  We can also specify the input and output files like this:

.. sourcecode:: bash

    openssl rsautl -encrypt -in p.txt -out c.txt -pubin -inkey kf.pem
    
Take a look

.. sourcecode:: bash

    hexdump -C c.txt

Decrypt with the private key

.. sourcecode:: bash

    $ openssl rsautl -decrypt -in c.txt -inkey kf
    
Enter pass phrase for ``kf``:

.. sourcecode:: bash

    hello world
    
We can also use the keys the other way around, encrypting with the private key and decrypting with the public one:

These options are called ``-sign`` and ``-verify``

.. sourcecode:: bash

    openssl rsautl -sign -in p.txt -out c.txt -inkey kf
    openssl rsautl -verify -in c.txt -pubin -inkey kf.pem

**Encrypting more data**

With a larger message to encrypt, we have to be more sophisticated

http://www.czeskis.com/random/openssl-encrypt-file.html

We generate 256 random bytes (the source does it in two steps, so that’s what we’ll do:

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