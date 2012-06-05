"""
Widgets that couple cities_reduced_fat and autocomplete_light.
"""

from django.utils.translation import ugettext_lazy as _
from django import forms

import autocomplete_light

from ..models import City


class CityAutocompleteWidget(forms.MultiWidget):
    """
    Double autocomplete for a City selection form field, requires
    autocomplete_light.

    This widget wraps around a Country and a City autocomplete widget. It sets
    the city widget's bootstrap to 'countrycity' so that the special javascript
    that connects the country and city field be used to instanciate the deck.
    """
    def __init__(self, channel_name, attrs=None, **kwargs):
        widgets = (
            autocomplete_light.AutocompleteWidget('CountryChannel',
                max_items=1, placeholder=_(u'country name ...')),
            autocomplete_light.AutocompleteWidget(channel_name,
                bootstrap='countrycity', placeholder=_(u'city name ...'),
                **kwargs),
        )
        super(CityAutocompleteWidget, self).__init__(widgets, attrs)

    def decompress(self, value):
        """
        Given a value from the database, return a value for each sub-widget.
        """
        if value:
            city = City.objects.get(pk=value)
            return [city.country.pk, value]
        return [None, None]

    def value_from_datadict(self, data, files, name):
        """
        Given values from the widget, return the value for the database.
        """
        values = super(CityAutocompleteWidget, self).value_from_datadict(
            data, files, name)
        return values[1]

    def _has_changed(self, initial, data):
        # we want multiwidget for rendering, but simple for data
        return forms.Widget._has_changed(self, initial, data)
