=====
django-api-base
=====

django-api-base is simple django package that can be used to build RESTFUL web api's with django

Detailed documentation is in the "docs" directory.

Quick start
-----------

1. Add "Common" to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = [
        ...
        'django-api-base',
    ]

2. Run `python manage.py migrate` to create the Common BaseProfile model which can be used as a user profile model in your django project.

