django-cities-reduced-fat -- *Simple django-cities alternative*
=========================================================

This appplication is a slightly modified version of django-cities-light that includes
regions. Most all the django-cities-light documentation still applies, in most instances
just replace light with reduced fat. File an issue for any bugs you come across!

This add-on provides models and commands to import country/region/city data into your
database.
The data is pulled from `GeoNames
<http://www.geonames.org/>`_ and contains:

  - country names
  - city names
  - admin1 region names

Spatial query support is not required by this application.

This application is very simple and is useful if you want to make a simple
address book for example. If you intend to build a fully featured spatial
database, you should use
`django-cities
<https://github.com/coderholic/django-cities>`_.

Upgrade
-------

See CHANGELOG.

Installation
------------

The development version::

    pip install -e git+git@github.com:skeet70/django-cities-reduced-fat.git#egg=cities_reduced_fat

Add `cities_reduced_fat` to your `INSTALLED_APPS`.

Now, run syncdb, it will only create tables for models that are not disabled::

    ./manage.py syncdb

Note that this project supports django-south.

Data update
-----------

Finally, populate your database with command::

    ./manage.py cities_reduced_fat

This command is well documented, consult the help with::

    ./manage.py help cities_reduced_fat

Resources
---------

You could subscribe to the mailing list ask questions or just be informed of
package updates.

- `Git graciously hosted
  <https://github.com/skeet70/django-cities-reduced-fat/>`_ by `GitHub
  <http://github.com>`_,
- `Documentation graciously hosted
  <http://django-cities-light.rtfd.org>`_ by `RTFD
  <http://rtfd.org>`_,
- `Package graciously hosted
  <http://pypi.python.org/pypi/django-cities-light/>`_ by `PyPi
  <http://pypi.python.org/pypi>`_,
- `Continuous integration graciously hosted
  <http://travis-ci.org/yourlabs/django-cities-light>`_ by `Travis-ci
  <http://travis-ci.org>`_
