.. _enigma1:

##############
Enigma machine
##############

The Enigma encryption machine was used extensively by the German military during World War II

http://en.wikipedia.org/wiki/Enigma_machine

employs a series of *rotors*.  A rotor is an electro-mechanical device that maps one ordering of the letters of the alphabet to another ordering.

As a simple example, we could imagine reversing the alphabet:

.. sourcecode:: bash

    fwd  ABCDEFGHIJKLMNOPQRSTUVWXYZ
    rev  ZYXWVUTSRQPONMLKJIHGFEDCBA  

To encode a letter, find it in the alphabet on the first line, and then read off the encoding directly below.

Each version of Enigma was provided with a small number of rotors (usually 3) with fixed wiring, but the mapping could be changed by a process of *rotation* of an outside ring.

.. image:: /_static/enigma1.jpg
   :scale: 50 %

For example, the Enigma I rotors included

http://en.wikipedia.org/wiki/Enigma_rotor_details

three rotors with these mappings in the base state:

.. sourcecode:: bash

    	ABCDEFGHIJKLMNOPQRSTUVWXYZ
    I	EKMFLGDQVZNTOWYHXUSPAIBRCJ
    II	AJDKSIRUXBLHWTMCQGZNPYFVOE
    III	BDFHJLCPRTXVZNYEIWGAKMUSQO

As each letter from the plaintext is sequentially encoded, one or more of the rotors is rotated.  We can model this like so:

step 1

.. sourcecode:: bash

    .	ABCDEFGHIJKLMNOPQRSTUVWXYZ
    I	EKMFLGDQVZNTOWYHXUSPAIBRCJ

step 2 (rotor I advanced one position)

.. sourcecode:: bash

    .	ABCDEFGHIJKLMNOPQRSTUVWXYZ
    I	KMFLGDQVZNTOWYHXUSPAIBRCJE
    
The pair of letters ``AA`` would thus be encoded as ``EK``.  The second is coding is different because rotor I has been advanced for step 2.

More complexity is achieved by using a series of rotors.  The collection of rotors is works just like an odometer which records mileage in an automobile (or decimal addition).  One complete turn of the rotor in the tenths place then advances the unit miles rotor by 1 step, and then a full turn of the unit miles rotor advances the tens place by 1.  

In the schematic shown in wikipedia, the right hand rotor is the one that takes the plaintext letter input, and it is the one that rotates the fastest.

In this scheme, after encryption, letters from the plaintext are encoded one-at-a-time, so they retain the same relative positions in the ciphertext (although they are not encoded independently, as indicated above).

All traffic encrypted for a single message would use a particular starting arrangement of the available rotors.

Furthermore, a "letter" moving through the arrangement is *reflected* and sent backward through the same set of three rotors in reverse orientation.  Consider the arrangement given above

.. sourcecode:: bash

    .    ABCDEFGHIJKLMNOPQRSTUVWXYZ
    I    EKMFLGDQVZNTOWYHXUSPAIBRCJ
    
	.    ABCDEFGHIJKLMNOPQRSTUVWXYZ
    II   AJDKSIRUXBLHWTMCQGZNPYFVOE
    
	.    ABCDEFGHIJKLMNOPQRSTUVWXYZ
    III  BDFHJLCPRTXVZNYEIWGAKMUSQO

An `A` becomes sequentially `E` (rotor I), then `E` becomes `S` (rotor II) and finally `S` becomes `G` (rotor III).  

After rotation, the letter is reflected and sent back through in reverse order.  

There is more to the process, as explained below, but even at this point I had some misconceptions about the process that were cleared up by this authoritative reference

http://www.codesandciphers.org.uk/enigma/example1.htm

main page:

http://www.codesandciphers.org.uk/enigma/enigma1.htm

The example given has the rotors in the sequence I-II-III, with the current entering from the right.  So the order of use is actually III-II-I-reflector-I-II-III.

This is just a matter of orientation.  More important are these two facts:  first, there is *no rotation* during any individual cycle.  

Secondly, the rotors have the property that decryption is exactly *the same process* as encryption, running an ``encrypt`` function on the ciphertext yields the plaintext.  This works because the cipher is symmetric, so that the pair of letters (AU) is enciphered as `A -> U` and `U -> A`.

Here are the three rotors in series:

.. sourcecode:: bash

    III
    ABCDEF G HIJKLMNO P QRSTUVWXYZ
    BDFHJL C PRTXVZNY E IWGAKMUSQO

    II
    AB C D E FGHIJKLMNOPQRSTUVWXYZ
    AJ D K S IRUXBLHWTMCQGZNPYFVOE

    I
    ABC D EFGHIJKLMNOPQR S TUVWXYZ
    EKM F LGDQVZNTOWYHXU S PAIBRCJ

the standard reflector is

.. sourcecode:: bash

    ABCDE F GHIJKLMNOPQR S TUVWXYZ
    YRUHQ S LDPXNGOKMIEB F ZCWVJAT

The example given is

.. sourcecode:: bash

    G -> C -> D -> F -> S

After that we must *invert the substitutions*.  Here we have done that for each of the 3 rotors.

.. sourcecode:: bash

    I
    ABCDE F GHIJKLMNOPQR S TUVWXYZ
    UWYGA D FPVZBECKMTHX S LRINQOJ

    II
    ABC D EFGHIJKLMNOPQR S TUVWXYZ
    AJP C ZWRLFBDKOTYUQG E NHXMIVS

    III
    AB C D E FGHIJKLMNOPQRSTUVWXYZ
    TA G B P CSDQEUFVNZHYIXJWLRKOM

Now, starting with `S` from the reflector we end up with `P`;  overall, we have `G -> P`.  Using the simulator below, we will show that `P -> G`.  As mentioned, the operation of the rotors (in this combination and without "rotation") gives 13 pairs of letters which are simply exchanged:

.. sourcecode:: bash

    (AU)(BE)(CJ)(DO)(FT)(GP)(HZ)(IW)(KN)(LS)(MR)(QV)(XY)

In actual operation, for the second letter one or more rotors have rotated according to the odometer model.

A last layer of encryption is provided by the "plugboard"  The plugboard swaps pairs of letters, for example, `A` might become `T` and at the same time `T` becomes `A`.  Not all letters were switched in the plugboard, but most are.  Normally, ten pairs were used.  The plugboard settings would be changed each day.

In the language of linear algebra, we might express the algorithm as:

.. math::

    E = P R M L U L^{-1} M^{-1} R^{-1} P^{-1}

remembering of course, that the rotors ``I.II.III`` advance with each letter, as described above.

I have written a simulator in Python.  Normally, I don't do much object-oriented programming, but this is a case where rotor objects are an obvious fit.  Also, the plugboard and reflector can be modeled with the same object, we just never rotate them.

At the end below is the listing for the simulator and its utilities (first version, no rotation).  But before that, here is the output of a run with the rotors described above but no plugboard:

.. sourcecode:: bash

    > python enigma.py 
    A -> B -> J -> Z -> T -> L -> K -> U
    B -> D -> K -> N -> K -> B -> J -> E
    C -> F -> I -> V -> W -> N -> T -> J
    D -> H -> U -> A -> Y -> O -> Y -> O
    E -> J -> B -> K -> N -> K -> D -> B
    F -> L -> H -> Q -> E -> A -> A -> T
    G -> C -> D -> F -> S -> S -> E -> P
    H -> P -> C -> M -> O -> M -> O -> Z
    I -> R -> G -> D -> H -> P -> U -> W
    J -> T -> N -> W -> V -> I -> F -> C
    K -> X -> V -> I -> P -> T -> N -> N
    L -> V -> Y -> C -> U -> R -> G -> S
    M -> Z -> E -> L -> G -> F -> W -> R
    N -> N -> T -> P -> I -> V -> X -> K
    O -> Y -> O -> Y -> A -> U -> H -> D
    P -> E -> S -> S -> F -> D -> C -> G
    Q -> I -> X -> R -> B -> W -> M -> V
    R -> W -> F -> G -> L -> E -> Z -> M
    S -> G -> R -> U -> C -> Y -> V -> L
    T -> A -> A -> E -> Q -> H -> L -> F
    U -> K -> L -> T -> Z -> J -> B -> A
    V -> M -> W -> B -> R -> X -> I -> Q
    W -> U -> P -> H -> D -> G -> R -> I
    X -> S -> Z -> J -> X -> Q -> Q -> Y
    Y -> Q -> Q -> X -> J -> Z -> S -> X
    Z -> O -> M -> O -> M -> C -> P -> H
    >

Notice that we have generated all the pairs described above:

.. sourcecode:: bash

    (AU)(BE)(CJ)(DO)(FT)(GP)(HZ)(IW)(KN)(LS)(MR)(QV)(XY)

and here a second run utilizing this plugboard

.. sourcecode:: bash

    ABCDEFGHIJKLMNOPQRSTUVWXYZ
    OWUREZGPYLKJMQAHNDVTCSBXIF

.. sourcecode:: bash

    > python enigma.py 
    A -> O -> Y -> O -> Y -> A -> U -> H -> D -> R
    B -> W -> U -> P -> H -> D -> G -> R -> I -> Y
    C -> U -> K -> L -> T -> Z -> J -> B -> A -> O
    D -> R -> W -> F -> G -> L -> E -> Z -> M -> M
    E -> E -> J -> B -> K -> N -> K -> D -> B -> W
    F -> Z -> O -> M -> O -> M -> C -> P -> H -> P
    G -> G -> C -> D -> F -> S -> S -> E -> P -> H
    H -> P -> E -> S -> S -> F -> D -> C -> G -> G
    I -> Y -> Q -> Q -> X -> J -> Z -> S -> X -> X
    J -> L -> V -> Y -> C -> U -> R -> G -> S -> V
    K -> K -> X -> V -> I -> P -> T -> N -> N -> Q
    L -> J -> T -> N -> W -> V -> I -> F -> C -> U
    M -> M -> Z -> E -> L -> G -> F -> W -> R -> D
    N -> Q -> I -> X -> R -> B -> W -> M -> V -> S
    O -> A -> B -> J -> Z -> T -> L -> K -> U -> C
    P -> H -> P -> C -> M -> O -> M -> O -> Z -> F
    Q -> N -> N -> T -> P -> I -> V -> X -> K -> K
    R -> D -> H -> U -> A -> Y -> O -> Y -> O -> A
    S -> V -> M -> W -> B -> R -> X -> I -> Q -> N
    T -> T -> A -> A -> E -> Q -> H -> L -> F -> Z
    U -> C -> F -> I -> V -> W -> N -> T -> J -> L
    V -> S -> G -> R -> U -> C -> Y -> V -> L -> J
    W -> B -> D -> K -> N -> K -> B -> J -> E -> E
    X -> X -> S -> Z -> J -> X -> Q -> Q -> Y -> I
    Y -> I -> R -> G -> D -> H -> P -> U -> W -> B
    Z -> F -> L -> H -> Q -> E -> A -> A -> T -> T
    >

Here, notice that with inclusion of the plugboard, the output has changed but it still has the symmetry property:  encoding is reversible:  A -> R and R -> A.

``enigma_util1.py``:

.. literalinclude:: /_static/enigma_util1.py

``enigma1.py``:

.. literalinclude:: /_static/enigma1.py