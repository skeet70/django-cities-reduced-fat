"""
Signals for this application.

city_items_pre_import
    Emited by city_import() in the cities_reduced_fat command for each row parsed in
    the data file. If a signal reciever raises InvalidItems then it will be
    skipped.

    An example is worth 1000 words: if you want to import only cities from
    France, USA and Belgium you could do as such::

        import cities_reduced_fat

        def filter_city_import(sender, items, **kwargs):
            if items[8] not in ('FR', 'US', 'BE'):
                raise cities_reduced_fat.InvalidItems()

        cities_reduced_fat.signals.city_items_pre_import.connect(filter_city_import)

Note: this signal gets a list rather than a City instance for performance
reasons.

filter_non_cities()
    By default, this reciever is connected to city_items_pre_import, it raises
    InvalidItems if the row doesn't have PPL in its features (it's not a
    populated place).
"""

import django.dispatch

from exceptions import *

__all__ = ['city_items_pre_import']

city_items_pre_import = django.dispatch.Signal(providing_args=['items'])


def filter_non_cities(sender, items, **kwargs):
    if 'PPL' not in items[7]:
        raise InvalidItems()
city_items_pre_import.connect(filter_non_cities)
