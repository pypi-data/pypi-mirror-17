
Flask-Sendwithus
================

About
-----

Forwards-compatible Flask extension to interact with the `sendwithus <https://www.sendwithus.com/>`_ API.

Installation
------------

    pip install Flask-Sendwithus

Documentation
-------------

Uses the standard extension pattern. Example::

    >>> from flask import Flask
    >>> from flask_sendwithus import Sendwithus

    >>> app = Flask(__name__)
    >>> app.config['SENDWITHUS_API_KEY'] = 'YOUR-API-KEY'
    >>> sendwithus = Sendwithus()
    >>> sendwithus.init_app(app)
    >>> r = sendwithus.send(
        email_id='YOUR-EMAIL-ID',
        recipient={'address': 'us@sendwithus.com'})
    >>> print(r.status_code)
    200
    )

See `the official python client's documentation <https://github.com/sendwithus/sendwithus_python)>`_ for further info on what methods are available. All methods found on the `sendwithus.api` instance is proxied on the Flask-Sendwithus's instance.



