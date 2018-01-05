.. _history:

#######
History
#######

**Caesar Cipher**

Julius Caesar is said to have used a simple substitution cipher as an encryption system.  

http://en.wikipedia.org/wiki/Caesar_cipher

    If he had anything confidential to say, he wrote it in cipher, that is, by so changing the order of the letters of the alphabet, that not a word could be made out. If anyone wishes to decipher these, and get at their meaning, he must substitute the fourth letter of the alphabet, namely D, for A, and so with the others. --Suetonius

.. image:: /_static/Caesar3.png
   :scale: 50 %


Here is a quick and dirty Python script to do this:

``caesar.py``:

.. literalinclude:: /_static/caesar.py

and here it is in action:

.. sourcecode:: bash

    > python caesar.py 3 ABC
    DEF
    > python caesar.py 3 HI BRUTUS
    KL EUXWXV
    > python caesar.py -3 KL EUXWXV
    HI BRUTUS
    >

Simon Singh, in *The Code Book*

http://www.amazon.com/Code-Book-Science-Secrecy-Cryptography/dp/0385495323

writes about the Vigenere cipher.  Here is a screenshot

.. image:: /_static/vigenere.png
   :scale: 100 %

For each letter of a key, one makes a dictionary to encode the alphabet.  For messages longer than the key, it repeats.

I wrote a Python script to do this.  Here is the output

.. sourcecode:: bash

    > python vigenere.py ATTACK
    WABTGG
    ATTACK
    > python vigenere.py 
    A : ABCDEFGHIJKLMNOPQRSTUVWXYZ
    B : BCDEFGHIJKLMNOPQRSTUVWXYZA
    C : CDEFGHIJKLMNOPQRSTUVWXYZAB
    D : DEFGHIJKLMNOPQRSTUVWXYZABC
    E : EFGHIJKLMNOPQRSTUVWXYZABCD
    F : FGHIJKLMNOPQRSTUVWXYZABCDE
    G : GHIJKLMNOPQRSTUVWXYZABCDEF
    H : HIJKLMNOPQRSTUVWXYZABCDEFG
    I : IJKLMNOPQRSTUVWXYZABCDEFGH
    J : JKLMNOPQRSTUVWXYZABCDEFGHI
    K : KLMNOPQRSTUVWXYZABCDEFGHIJ
    L : LMNOPQRSTUVWXYZABCDEFGHIJK
    M : MNOPQRSTUVWXYZABCDEFGHIJKL
    N : NOPQRSTUVWXYZABCDEFGHIJKLM
    O : OPQRSTUVWXYZABCDEFGHIJKLMN
    P : PQRSTUVWXYZABCDEFGHIJKLMNO
    Q : QRSTUVWXYZABCDEFGHIJKLMNOP
    R : RSTUVWXYZABCDEFGHIJKLMNOPQ
    S : STUVWXYZABCDEFGHIJKLMNOPQR
    T : TUVWXYZABCDEFGHIJKLMNOPQRS
    U : UVWXYZABCDEFGHIJKLMNOPQRST
    V : VWXYZABCDEFGHIJKLMNOPQRSTU
    W : WXYZABCDEFGHIJKLMNOPQRSTUV
    X : XYZABCDEFGHIJKLMNOPQRSTUVW
    Y : YZABCDEFGHIJKLMNOPQRSTUVWX
    Z : ZABCDEFGHIJKLMNOPQRSTUVWXY
    > 

Invocation without a message shows the individual dictionaries.  Of course, one could substitute any dictionary for these, for example, a different randomly scrambled one for each letter of the key.  Nevertheless, even a scrambled system is easily broken by frequency analysis, given a long enough ciphertext.  We will look at how this is done in a later section.  

The fundamental point is that key repetition makes for "broken" cryptography.

``vigenere.py``:

.. literalinclude:: /_static/vigenere.py



