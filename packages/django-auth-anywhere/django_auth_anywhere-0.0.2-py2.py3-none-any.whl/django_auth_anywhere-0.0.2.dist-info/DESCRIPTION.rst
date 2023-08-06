django-auth-anywhere
=======================

django-auth-anywhere is a Django application which enables using `Django Rest Framework`_ authentication backends throughout your Django application. This can be useful to secure non-API endpoints behind token authentication using `JSON web tokens`_.

.. _Django Rest Framework: http://www.django-rest-framework.org/

.. _JSON web tokens: http://getblimp.github.io/django-rest-framework-jwt/

Requirements
------------

This has only been tested with:

* Python: 3.5
* Django: 1.8, 1.9, 1.10

Setup
-----

Install from **pip**:

.. code-block:: sh

    pip install django-auth-anywhere

and then add it to your installed apps:

.. code-block:: python

    INSTALLED_APPS = (
        ...
        'auth_anywhere',
        ...
    )

You will also need to add a middleware class to listen in on responses:

.. code-block:: python

    MIDDLEWARE_CLASSES = [
        ...
        'auth_anywhere.middleware.AuthenticationMiddleware',
        'django.middleware.common.CommonMiddleware',
        ...
    ]

Credits
-------

``django-auth-anywhere`` was created by Morgante Pell (`@morgante
<https://github.com/morgante>`_), with inspiration from Anthony Lobko (`@amelius15
<https://github.com/amelius15>`_).


History
=======

Pending
-------

* New release notes go here.

0.0.2 (2016-09-30)
-----------------

* Remove references to internal project code.


0.0.1 (2016-09-30)
-----------------

* Initial release


