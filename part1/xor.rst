.. _xor:

####################
Encryption using XOR
####################

**XOR is symmetric**

The XOR (exclusive or, xor) operation takes two bits and generates a third bit using the rules:

    * 0 ^ 0 = 1 ^ 1 = 0
    * 0 ^ 1 = 1 ^ 0 = 1

It can also be applied to streams of bytes like so:

    * p = 0101
    * k = 0011
    * c = 0110
    
A fundamental result is that XOR is symmetric:

    p ^ k = c ^ k

If we take our message to be a string of ASCII characters like 'hello world', we can encrypt the string by computing the XOR of the bytes with a string of random bytes as the **key**.

The resulting ciphertext will consist of random bytes that can be de-ciphered if the key is known, by simply repeating the XOR operation.

In principle, if Alice and Bob both know the key but no one else does, and if the key is long enough (and never re-used), then their encrypted messages to each cannot be read by an eavesdropper, Eve.

Modern cryptography is about providing tools to make sure these two provisions are satisfied.  Making a long enough key typically involves a stream cipher, whereas transmitting the key over an open network involves asymmetric (public/private key) cryptography.

Let's just do an example

.. sourcecode:: bash

    > echo -n "hello world" > p.txt
    
We echo the text to ``p.txt``, with the ``-n`` flag so as not to have a newline added at the end.

Find out how long a key we need and generate the necessary random bytes with ``openssl``:

.. sourcecode:: bash

    > wc -c p.txt
          11 p.txt
    > openssl rand 11 > kf

One would have expected a command line utility to do the XOR operation, but I couldn't find one.  So, to Python:

``xor_script.py``

.. literalinclude:: /_static/xor_script.py

In Python, the XOR operator is ``^``, and it operates on decimals, which we obtain here using ``ord``.  We convert the result back to bytes using ``bytearray`` and write it to disk.

I did ``hexdump`` sequentially on ``p.txt``, ``kf`` and ``c`` and re-formatted the results.

.. sourcecode:: bash

    68 65 6c 6c 6f 20 77 6f 72 6c 64               
    de 62 db 79 9c 86 b5 bc c3 a0 09               
    b6 07 b7 15 f3 a6 c2 d3 b1 cc 6d               

Now, unless you are made of metal, you won't obviously see that, for example, ``6 ^ b = d``, but it does.

Recall that hexadecimal ``b`` is decimal ``11 = 8 + 2 + 1`` and ``d`` is decimal ``13 = 8 + 4 + 1``, while ``6 = 4 + 2`` so:    

.. sourcecode:: bash

    6 = 0110
    b = 1011
    3 = 1101

Similar ``a ^ c = 1010 ^ 1100 = 0110 = 6``, as seen in the leading position for the second byte from the end.

Anyway, it works.  It is helpful to remember (or be able to count on your fingers to find) that

.. sourcecode:: bash

    a = 10
    b = 11
    c = 12
    d = 13
    e = 14
    f = 15

And then to factor for powers of 2 quickly.

.. sourcecode:: bash

    13 = 8 + 4 + 1

And so on.

The result of this introductory material is devoted to solving the other problems, starting with key exchange.


