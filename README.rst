===============================
Welcome to django-item-messages
===============================

.. image:: https://github.com/thomst/django-item-messages/actions/workflows/ci.yml/badge.svg
   :target: https://github.com/thomst/django-item-messages/actions/workflows/ci.yml
   :alt: Run tests for django-item-messages

.. image:: https://coveralls.io/repos/github/thomst/django-item-messages/badge.svg?branch=main
   :target: https://coveralls.io/github/thomst/django-item-messages?branch=main
   :alt: coveralls badge

.. image:: https://img.shields.io/badge/python-3.7%20%7C%203.8%20%7C%203.9%20%7C%203.10%20%7C%203.11-blue
   :target: https://img.shields.io/badge/python-3.7%20%7C%203.8%20%7C%203.9%20%7C%203.10%20%7C%203.11-blue
   :alt: python: 3.7, 3.8, 3.9,3.9,3.10,3.11

.. image:: https://img.shields.io/badge/django-2.2%20%7C%203.0%20%7C%203.1%20%7C%203.2%20%7C%204.0%20%7C%204.1%20%7C%204.2-orange
   :target: https://img.shields.io/badge/django-2.2%20%7C%203.0%20%7C%203.1%20%7C%203.2%20%7C%204.0%20%7C%204.1%20%7C%204.2-orange
   :alt: django: 2.2, 3.0, 3.1, 3.2, 4.0, 4.1, 4.2


Description
===========
Item-messages allows you to add item specific messages which are rendered
beneath the related item in an admin changelist view.

Item messages are permanent within a session and can be added, updated or
removed. This makes them also useful for long running asynchronious background
processes.


Installation
============
Install from pypi.org::

    pip install django-item-messages


Setup
=====
Add item_messages to your installed apps::

    INSTALLED_APPS = [
        ...
        'item_messages',
        ...
    ]

Add the item_messages' middleware class::

    MIDDLEWARE = [
        ...
        'item_messages.middleware.ItemMessageMiddleware',
        ...
    ]

**Note**: The item-messages middelware class have to be listed after the session's
middelware class.

Add item_messages' context processor::

    TEMPLATES = [
        {
            ...
            'OPTIONS': {
                'context_processors': [
                    ...
                    'item_messages.context_processors.item_messages',
                    ...
                ],
            },
        },
    ]


Usage
=====
TODO