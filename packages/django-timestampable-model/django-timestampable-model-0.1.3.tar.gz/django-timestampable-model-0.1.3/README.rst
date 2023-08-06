===========================
Django Timestampable Models
===========================

.. image:: https://travis-ci.org/achedeuzot/django-timestampable.svg?branch=master
    :target: https://travis-ci.org/achedeuzot/django-timestampable.svg?branch=master

.. image:: https://coveralls.io/repos/github/achedeuzot/django-timestampable/badge.svg?branch=master
    :target: https://coveralls.io/github/achedeuzot/django-timestampable?branch=master


Django Timestampable model is a simple enhancement mixin that enables Django models to have a ``created_at``
and ``updated_at`` field that is always updated.

This has been done under many plugins *BUT* the main difference between this plugin and the
many others out there that do the same, is that Django Timestampable Models update
the ``updated_at`` field under any circumstance: fixture loading, bulk updates, etc. whereas traditional
Timestampable mixins only provide shorthand for ``auto_add`` and ``auto_add_now`` shortcuts for ``DateTimeField``  s.

It achieves this by using Django signals.

Quick start
-----------

1. Add "django_timestampable" to your ``INSTALLED_APPS`` settings like this:

.. code-block:: python

    INSTALLED_APPS = [
        ...
        'django_timestampable',
    ]

2. Add ``TimestampableModel`` in your ``Model`` s like so:

.. code-block:: python

    class Stuff(TimestampableModel):

        some_attribute = CharField()

        ...

3. Run `python manage.py makemigrations` then `python manage.py migrate` to add the columns to your models
in your database.

Requirements
------------

No dependencies.

Tested on `Django`_ 1.9.9, 1.10.1 with Python 2.7, 3.4, 3.5

.. _Django: http://www.djangoproject.com/

