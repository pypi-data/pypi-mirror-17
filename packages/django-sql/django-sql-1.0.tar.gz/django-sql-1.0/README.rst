|Build Status| |Licence| |Coverage Status|

Django-SQL
==========

A simple app for executing SQL queries in Django admin panel.

*! WARNINIG !*

*Do not install this app if you afraid of consequences of giving access
to database from admin panel.*

Requirements
''''''''''''

-  Python3
-  Django 1.9

Installation
''''''''''''

::

        pip install git+https://github.com/luminousmen/django-sql.git

Add to your ``INSTALLED_APPS`` in ``settings.py``:

::

        INSTALLED_APPS = [
          ...
          'sql',
        ]

Add to your ``urls.py``:

::

        url(r'^admin/sql/(?:sql/)?$', execute_sql, name='sql'),

.. |Build Status| image:: https://travis-ci.org/luminousmen/django-sql.svg?branch=master
   :target: https://travis-ci.org/luminousmen/django-sql
.. |Licence| image:: https://img.shields.io/github/license/mashape/apistatus.svg
   :target: https://github.com/luminousmen/django-sql/blob/master/LICENCE
.. |Coverage Status| image:: https://coveralls.io/repos/github/luminousmen/django-sql/badge.svg?branch=master
   :target: https://coveralls.io/github/luminousmen/django-sql?branch=master
