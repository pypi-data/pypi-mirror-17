Django settings dict
====================

This is small helper that makes it easier to store distributable django app settings in project :code:`settings.py` as a dict.
Purpose is to keep settings file simple and clean.
With this it's also easier to set defaults for the settings and warn about settings that have been removed.

Helper also supports marking settings that should be imported before returning.
Import is done using :code:`django.utils.module_loading.import_string`.

Helper resolves variables when requested for the first time and caches the value for faster lookup next time.
Variables that are not in :code:`required` or :code:`defaults` raise :code:`AttributeError`.
If you like to clear the cache, you can use :code:`_clear_cached()`,
though there shouldn't be need for that as the helper automatically does it if the setting changes.

Design is based on class done in `Django REST framework <https://github.com/tomchristie/django-rest-framework>`_.


Example
-------

Setting defitions in your applications :code:`app_settings.py` (for example):

.. code-block:: python

  from django_settingsdict import SettingsDict
  REQUIRED = (
      'IMPORTANT_SETTING',
  )
  DEFAULTS = {
      'URL_NAME': 'test_app',
      'REVERSE_FUNC': 'django.core.urlresolvers.reverse',
  }
  IMPORT_STRINGS = (
      'REVERSE_FUNC',
  )
  REMOVED = (
      'OLD_SETTING',
  )
  app_settings = SettingsDict('MY_APP',
                              required=REQUIRED,
                              defaults=DEFAULTS,
                              removed=REMOVED,
                              import_strings=IMPORT_STRINGS)

Configuration in your projects :code:`settings.py`:

.. code-block:: python

  MY_APP = {
      'IMPORTANT_SETTING': 'some value',
      'URL_NAME': 'test_app_2',
  }

And in your application code:

.. code-block:: python

  from .app_settings import app_settings

  print(app_settings.IMPORTANT_SETTING)
  print(app_settings.URL_NAME)
  print(app_settings.REVERSE_FUNC)

would make following result:

.. code-block::

  some value
  test_app_2
  <function reverse at 0x7fd5119e0578>
