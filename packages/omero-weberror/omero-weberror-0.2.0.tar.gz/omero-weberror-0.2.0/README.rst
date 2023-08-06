.. image:: https://travis-ci.org/openmicroscopy/omero-weberror.svg?branch=master
    :target: https://travis-ci.org/openmicroscopy/omero-weberror

.. image:: https://badge.fury.io/py/omero-weberror.svg
    :target: https://badge.fury.io/py/omero-weberror


OMERO.weberror
============================
Django application that helps testing errors

Requirements
============

* OMERO 5.1.0 or later

Installation
============

Install OMERO.web

This app installs into the OMERO.web framework.

::

    $ pip install omero-weberror

Add weberror custom app to your installed web apps:

::

    $ bin/omero config append omero.web.apps '"omero_weberror"'

Now restart OMERO.web as normal.


License
-------

OMERO.weberror is released under the AGPL.

Copyright
---------

2016, The Open Microscopy Environment
