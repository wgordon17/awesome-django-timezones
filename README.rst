=============================
Awesome Django Timezones
=============================

.. image:: https://badge.fury.io/py/awesome-django-timezones.svg
    :target: https://badge.fury.io/py/awesome-django-timezones

.. image:: https://travis-ci.org/wgordon17/awesome-django-timezones.svg?branch=master
    :target: https://travis-ci.org/wgordon17/awesome-django-timezones

.. image:: https://codecov.io/gh/wgordon17/awesome-django-timezones/branch/master/graph/badge.svg
    :target: https://codecov.io/gh/wgordon17/awesome-django-timezones

Easily set a localized timezone for users

Documentation
-------------

The full documentation is at https://awesome-django-timezones.readthedocs.io.

Quickstart
----------

Install Awesome Django Timezones::

    pip install awesome-django-timezones

Add it to your ``INSTALLED_APPS``:

.. code-block:: python

    INSTALLED_APPS = (
        ...
        'awesome_django_timezones.apps.DjangoTimezonesConfig',
        ...
    )

Add DjangoTimezonesMiddleware to your ``MIDDLEWARE_CLASSES``:

.. code-block:: python

    MIDDLEWARE_CLASSES = (
        ...
        'awesome_django_timezones.middleware.TimezonesMiddleware',
        ...
    )

Add ``js/awesome_django_timezones.js`` to your base template

.. code-block:: html

    <script src="{% static 'awesome_django_timezones/js/awesome_django_timezones.js' %}"></script>

(Optional) If you need Django to be timezone aware on the Admin page, you will have to extend the
Admin ``base.html`` in ``your_project/templates/admin/base.html``

.. code-block:: python

    {% extends 'admin/base.html' %}
    {% load static %}

    {% block footer %}
      {{ block.super }}

      <script src="{% static 'js/awesome_django_timezones.js' %}"></script>

    {% endblock %}

Features
--------

* Provides an accurate method of determining the an end user's timezone and activating that timezone in Django.

* Uses client side, JavaScript detection for the most accurate method of determining a timezone.

  * Uses the widely supported, native `Intl JavaScript
    library <https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/DateTimeFormat/resolvedOptions>`_
    to detect the client's timezone. This library is not currently implemented for IE11.

* Falls back to server side timezone detection via an IP API.

  * Fall back is provided for IE11 clients or clients with JavaScript disabled.

  * Relies on third-party IP API lookups by https://ipapi.co. Consider purchasing a plan if you need more than 30k IP lookups/month or
    if you need support (no affiliation).

Running Tests
-------------

Does the code actually work?

::

    source <YOURVIRTUALENV>/bin/activate
    (myenv) $ pip install -r requirements_test.txt
    (myenv) $ tox

Credits
-------

Tools used in rendering this package:

*  Cookiecutter_
*  `cookiecutter-djangopackage`_
*  `ipapi`_

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`cookiecutter-djangopackage`: https://github.com/pydanny/cookiecutter-djangopackage
.. _`ipapi`: https://github.com/ipapi-co/ipapi-python
