pyramid_unicodedammit
=====================

.. image:: https://api.travis-ci.org/npilon/pyramid_unicodedammit.png?branch=master
        :target: https://travis-ci.org/npilon/pyramid_unicodedammit

Pyramid plugin for making a best effort to deal with bizarre query strings.
Query strings should only ever contain UTF-8 encoded text.
However, it's possible using some web browsers to submit forms or enter URLs containing other encodings.
This plugin registers a tween that uses UnicodeDammit from beautifulsoup4 to make a best effort to properly recognize these query strings.

Usage
-----

1. Include ``pyramid_unicodedammit`` using either the ``pyramid.includes`` configuration file setting or ``config.include('pyramid_unicodedammit')``
