
==========================
Leonardo leonardo-feature-switcher
==========================

Simple feature toggle tool for Leonardo CMS

.. contents::
    :local:

Installation
------------

.. code-block:: bash

    pip install leonardo-feature-switcher

add *feature_switchers* to LEONARDO_CONF_SPEC in your local_settings.py::

    LEONARDO_CONF_SPEC = {
        'feature_switchers': {},
    }

then in your modules add custom switchers::

    LEONARDO_FEATURE_SWITCHERS = {
        'my_feature': lambda request, *args, **kw: True,
        'my_feature1': 'leonardo_feature_switcher.my_feature1'
    }

and in your templates::

    {% load feature_switcher %}

    {% is_on "my_feature" %}

    {% if my_feature %}

    {% endif %}

    {% is_on_as "my_feature" as my_feature_result %}

    {% if my_feature_result %}
    {% endif %}

Read More
=========

* https://github.com/django-leonardo/django-leonardo
