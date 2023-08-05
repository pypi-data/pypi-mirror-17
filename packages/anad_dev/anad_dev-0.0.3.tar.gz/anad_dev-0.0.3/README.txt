anad\_dev
=========

tools for development..... in anad labo

Installation
------------

::

    pip install anad_dev

Usage
-----

ecrypt
^^^^^^

e.g.:

.. code:: python

    >>> from anad_dev import ecrypt
    >>> pw = 'test_pass_phrase'
    >>> ec_pw = ecrypt.ecrypt.compr(pw)
    >>> ec_pw
    '/Td6WFoAAATm1rRGAgAhARYAAAB0L+WjAQAPdGVzdF9wYXNzX3BocmFzZQA3khspehQ3iwABKBDl\nC2xgH7bzfQEAAAAABFla\n'
    >>> 
    >>> ecrypt.ecrypt.decompr(ec_pw)
    'test_pass_phrase'

| this is just a easy encryption everybody CAN decrypt.
| I just use it when I don't want to show my password at glimpse.

send\_gmail
^^^^^^^^^^^

e.g.:

.. code:: python

    from anad_dev import ecrypt, send_gmail
    account = 'dais.cns@gmail.com'
    passwd = ecrypt.ecrypt.decompr('/Td6WFoAAATm1rRGAgAhARYAAAB0L+WjAQAPdGVzdF9wYXNzX3BocmFzZQA3khspehQ3iwABKBDl\nC2xgH7bzfQEAAAAABFla\n')
    body = 'test\nhehehe'
    subject = 'gmail test send'
    msg_to = 'dais.cns@gmail.com'
    send_gmail.send_gmail.doIt(account, passwd, body, subject, msg_to)

\*\*\* you need to turn on as your gmail account can used low level
access on your gmail setting page.

--------------

| any questions to:
| dais.cns@gmail.com
