custom_settings - CUSTOM SETTINGS
=================================

.. image:: https://circleci.com/gh/TakesxiSximada/custom_settings.svg?style=svg
           :target: https://circleci.com/gh/TakesxiSximada/custom_settings
           :alt: CircleCI Status

.. image:: https://codecov.io/gh/TakesxiSximada/custom_settings/branch/master/graph/badge.svg
           :target: https://codecov.io/gh/TakesxiSximada/custom_settings
           :alt: CodeCov Status

When describing in python of the configuration file, you need to change it in each environment. For example settings.py of Django.
This package provides the utility to assist it.


Install
-------

::

   $ pip install custom_settings

How to use it
-------------

settings_custom.py::

  AUTH_CREDENTIAL = 'MY_CREDENTIAL'

.. code-block::

   >>> import custom_settings
   >>> custom = custom_settings.load('settings_custom')
   >>> custom.get('AUTH_CREDENTIAL')
   'MY_CREDENTIAL'
   >>> custom.get('NO_SET_VALUE', default=10)
   10



Other
-----

- PyPI: https://pypi.python.org/pypi/custom_settings
- Github: https://github.com/TakesxiSximada/custom_settings
- CircleCI: https://circleci.com/gh/TakesxiSximada/custom_settings
- CodeCov: https://codecov.io/gh/TakesxiSximada/custom_settings
