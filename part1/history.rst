.. _history:

#####################
Encryption in History
#####################

**Enigma**

In the Enigma encryption machine

http://en.wikipedia.org/wiki/Enigma_machine

a rotor is a mechano-electrical device that maps one ordering of the letters of the alphabet to another ordering.  

For each version of Enigma, there was a small number of rotors (3-5) with fixed mappings.

.. image:: /_static/enigma1.jpg
   :scale: 50 %

For example, the Enigma I rotors included

http://en.wikipedia.org/wiki/Enigma_rotor_details

.. sourcecode:: bash

    	ABCDEFGHIJKLMNOPQRSTUVWXYZ
    I	EKMFLGDQVZNTOWYHXUSPAIBRCJ
    II	AJDKSIRUXBLHWTMCQGZNPYFVOE
    III	BDFHJLCPRTXVZNYEIWGAKMUSQO

A letter can map to itself (I count 4 such events in 26 x 3 = 78).

As letters of the plaintext are sequentially encoded, one or more of the rotors is rotated.  We can model this like so:

step 1

.. sourcecode:: bash

    .	ABCDEFGHIJKLMNOPQRSTUVWXYZ
    I	EKMFLGDQVZNTOWYHXUSPAIBRCJ

step 2 (rotor I advanced one position)

.. sourcecode:: bash

    .	ABCDEFGHIJKLMNOPQRSTUVWXYZ
    I	KMFLGDQVZNTOWYHXUSPAIBRCJE
    
To encode a letter, find it in the alphabet on the first line, and then read off the encoding directly below.

The pair of letters ``AA`` would thus be encoded as ``EK``.  The change occurs because rotor I has been advanced for step 2.

More complexity is achieved by using combinations of rotors in series.  The collection of rotors is rotated just like an odometer, each complete turn of the rotor showing tenths of a mile in an odometer rotates the unit miles rotor by 1, and a full turn of the unit miles turns the tens place by 1.  

In the schematic on wikipedia, the right hand rotor is the that takes the plaintext letter input (rotor I), and it is the one that rotates the fastest.

In this scheme, letters from the plaintext preserve the same position in the ciphertext, and each encryption step occurs one-at-a-time (although not independently, as the above text indicates).

All traffic encrypted for a single message would use a particular arrangement of 3-5 available rotors.

Furthermore, a "letter" moving through the arrangement is *reflected* and sent backward through the same set of three rotors in reverse orientation.  Consider the arrangement given above

.. sourcecode:: bash

    	ABCDEFGHIJKLMNOPQRSTUVWXYZ
    I	EKMFLGDQVZNTOWYHXUSPAIBRCJ
    II	AJDKSIRUXBLHWTMCQGZNPYFVOE
    III	BDFHJLCPRTXVZNYEIWGAKMUSQO

An `A` comes in and becomes, sequentially `E` (rotor I), then `E` becomes `S` (rotor II) and finally `S` becomes `G` (rotor III).  

After rotation, the letter is reflected and sent back through in reverse order.  However, in the meantime, the one or more rotors have rotated according to the odometer model.  Thus, for the return trip we have

.. sourcecode:: bash

    	ABCDEFGHIJKLMNOPQRSTUVWXYZ
    III	BDFHJLCPRTXVZNYEIWGAKMUSQO
    II	AJDKSIRUXBLHWTMCQGZNPYFVOE
    I	KMFLGDQVZNTOWYHXUSPAIBRCJE
    
Here, we are going to move through the rotors in the reverse direction.  What this corresponds to is finding the input letter in the line for a given rotor, and reading off the "output" in the alphabet on the first line.

The `G` from the reflector becomes `E`, then `Z` and finally `M`.

A last layer of encryption is provided by the "plugboard"  The plugboard swaps pairs of letters, for example, `A` might become `T` and at the same time `T` becomes `A`.  Not all letters were switched in the plugboard, but most are.  Normally, ten pairs were used.

Suppose that the plugboard we are using swaps `A` for `T` and `M` for `J`.  Then, to encode a message starting with `THE` the first letter `T` would go through the plugboard (in the forward direction) to become `A`, become encoded to `M` as described above, and then go out through the plugboard in reverse to become, finally, `J`.

In the language of linear algebra, we might express the algorithm as:

.. math::

    E = P R M L U L^{-1} M^{-1} R^{-1} P^{-1}

remembering of course, that the rotors RML advance with each letter, as described above.

``enigma.py``:

.. literalinclude:: /_static/enigma.py


