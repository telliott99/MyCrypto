.. _summary:

#######
Summary
#######

**Using openssh**

.. sourcecode:: bash

    > ssh-keygen -t rsa -C "" -N "" -b 1024 -f kf
    
which gives us ``kf`` and ``kf.pub``.

For ``ssh`` -ing into a server see chapter ___.

**Using openssl**

We've already done key migration from ``openssh``

.. sourcecode:: bash

    > openssl rsa -in kf -pubout > kf.pem

which gives us ``kf.pem``.

And we can also generate key pairs directly using ``openssl``:

.. sourcecode:: bash

    > openssl genrsa -out privkey.pem
    Generating RSA private key, 512 bit long modulus
    ...++++++++++++
    .......++++++++++++
    e is 65537 (0x10001)
    >

We've looked directly at these private keys:

.. sourcecode:: bash

    > openssl rsa -text -in kf

We've done encryption and decryption both symmetric 

.. sourcecode:: bash

    > echo "hello world" > p.txt
    > openssl rand 250 > key
    > openssl enc -aes-256-cbc -salt -in p.txt -out c.txt -pass file:./key
    > openssl enc -d -aes-256-cbc -in c.txt -out m.txt -pass file:./key
    > cat m.txt
    hello world
    >
    
and asymmetric

.. sourcecode:: bash

    > openssl rsautl -encrypt -in p.txt -out c.txt -pubin -inkey kf.pem
    > openssl rsautl -decrypt -in c.txt -inkey kf
    hello world
    >
    
    > openssl rsautl -sign -in p.txt -out c.txt -inkey kf
    > openssl rsautl -verify -in c.txt -pubin -inkey kf.pem
    hello world
    >
    
Each of these will work with a pipe ``|`` or a redirect ``>``

.. sourcecode:: bash

    > echo "abc" | openssl rsautl -encrypt -pubin -inkey kf.pem > c.txt

And, or course, we did some ``base64`` stuff

.. sourcecode:: bash

    > openssl base64 -in p.txt -out b.txt