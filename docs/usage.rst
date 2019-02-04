=====
Usage
=====

To use Awesome Django Timezones in a project, add it to your ``INSTALLED_APPS``:

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

    <script src="{% static 'js/awesome_django_timezones.js' %}"></script>

(Optional) If you need Django to be timezone aware on the Admin page, you will have to extend the
Admin ``base.html`` in ``your_project/templates/admin/base.html``

.. code-block:: python

    {% extends 'admin/base.html' %}
    {% load static %}

    {% block footer %}
      {{ block.super }}

      <script src="{% static 'js/awesome_django_timezones.js' %}"></script>

    {% endblock %}
