Lipy\_Notify
============

Send message to your Line.app from Python

Instllation
-----------

``pip install lipy_notify``

Usage
-----

Firstly, get your personal access token from `LINE Notify My
Page <https://notify-bot.line.me/my/>`__

then;

.. code:: python

    from lipy_notify import LipyNotify

    line = LipyNotify
    line.set_token("your_access_token")
    line.send("message")

and you're done.
