djangocms-classic-admin-style
==============================
I'm a big fan of `django-cms`_ but I've always thought that their `djangocms-admin-style`_ wasn't an improvement on the original Django admin styling. In the past I just wouldn't use `djangocms-admin-style`_, but then there are a few styling issues that you can then run into. This app is to fix those styling bugs.


Installation
------------
To install::

    pip install djangocms-classic-admin-style

Then add djangocms_classic_admin_style to your installed apps before Django's admin::

    INSTALLED_APPS = [
        ...
        'djangocms_classic_admin_style',
        'django.contrib.admin',
        ...
    ]

Then collect the static files and that's it::

    python manage.py collectstatic


.. _django-cms: https://github.com/divio/django-cms
.. _djangocms-admin-style: https://github.com/divio/djangocms-admin-style
