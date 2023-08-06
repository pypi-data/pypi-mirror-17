lipy\_notify
============

Send message to your Line.app from Python

Installation
============

``pip install lipy_notify``

Usage
=====

Firstly, get your personal access token from `LINE Notiy My
Page <https://notify-bot.line.me/my/>`__.

Then:

.. code:: python

    from lipy_notify import LipyNotify

    line = LipyNotify
    line.set_token("your_personal_access_token")
    line.send("message")

...and you are good to go!
