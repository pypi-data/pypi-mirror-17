===============================================
 django-crossbar - Crossbar.io Integration for Django
===============================================

.. image:: diagram.png

:Version: 0.1
:Web: https://git.atm4coin.com/root/django-crossbar/
:Download: http://pypi.python.org/pypi/django-crossbar/
:Source: https://git.atm4coin.com/root/django-crossbar/
:Keywords: crossbar, django, celery, python

--

WARNING
=======

This software is experimental and incomplete!

Overview
========

All RPC + Pubsub activites are handled by celery tasks, of which there are several types.

The first is a classic celery task where you can write your own code (CROSSBAR_CELERY_TASKS).
The rest are generic celery tasks to acieve object_list, object_detail, object_update & object create (for database objects).   

These are all sepecified in django settings.py file


Installation
=============

You can install ``django-crossbar`` either via the Python Package Index (PyPI)
or from source.

To install using ``pip``,::

    $ pip install django-crossbar

OR from source

    $ pip install git+https://git.atm4coin.com/root/django-crossbar.git

Add "djcb" and "djcelery" to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = [
        ...
        'djcelery',
        'djcb',
    ]

Do crossbar / django-crossbar setup

    ./manage.py djcb_init

Run your project with:

    $ crossbar start


Note: You need to make sure prerequisites for celery etc are setup (message broker etc)
