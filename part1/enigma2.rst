.. _enigma2:

####################
Enigma with rotation
####################

This section contains a modified version of the simulator that incorporates rotation (of the rightmost-rotor only).  Here is a run:

.. sourcecode:: bash

    > python enigma.py ATTACKATDAWN
    input:  ATTACKATDAWN
    ctext:  RFALTWCQFHYT
    ptext:  ATTACKATDAWN
    > python enigma.py ATTACKYOUIDIOTSORIWILLBESOMADATTACK
    input:  ATTACKYOUIDIOTSORIWILLBESOMADATTACK
    ctext:  RFALTWXVZNCDZUADHHQTCGHPPYDZRLCVCXR
    ptext:  ATTACKYOUIDIOTSORIWILLBESOMADATTACK
    >
    
And here is the code.  The modified ``enigma_util.py``:

.. literalinclude:: /_static/enigma_util.py

``enigma.py``:

.. literalinclude:: /_static/enigma.py