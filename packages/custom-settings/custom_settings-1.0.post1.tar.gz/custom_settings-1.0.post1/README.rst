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

.. code-block::

   $ pip install custom_settings

How to use it
-------------

settings_custom.py

::

   AUTH_CREDENTIAL = 'MY_CREDENTIAL'
   INTEGER_VALUE = '1'


Do the following to use this configuration file.


.. code-block::

   >>> import custom_settings
   >>> custom = custom_settings.load('settings_custom')
   >>> custom.get('AUTH_CREDENTIAL')
   'MY_CREDENTIAL'


If you specified `type_` argument, convert type to.


.. code-block::

   >>> custom.get('INTEGER_VALUE', type_=int, default=10)
   1


If you specify True in `use_environ`, if it does not exist in settings_custom, acquired from the os.environ.


.. code-block::

   >>> custom.get('PS1', use_environ=True)
   '$ '


If you specify `default`, if it does not exist in settings_custom, to used default.


.. code-block::

   >>> custom.get('NO_SET_VALUE', default=10)
   10


If you specify True in `raise_exception`, if it does not exist in settings_custom,  raise exception.


.. code-block::

   >>> custom.get('NO_SET_VALUE', use_environ=True, raise_exception=True)
   Traceback (most recent call last):
     File "<stdin>", line 1, in <module>
     File "/envs/3.5/lib/python3.5/site-packages/custom_settings/adapters.py", line 40, in get
       raise exc.NoCustomSettingError('Not been set: {}'.format(name))
   custom_settings.exc.NoCustomSettingError: Not been set: NO_SET_VALUE



Other
-----

- PyPI: https://pypi.python.org/pypi/custom_settings
- Github: https://github.com/TakesxiSximada/custom_settings
- CircleCI: https://circleci.com/gh/TakesxiSximada/custom_settings
- CodeCov: https://codecov.io/gh/TakesxiSximada/custom_settings
