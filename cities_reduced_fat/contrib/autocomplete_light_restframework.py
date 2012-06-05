"""
Couples djangorestframework and cities_reduced_fat.
"""

import autocomplete_light

from ..models import City, Country

from autocomplete_light_channels import CityChannelMixin


class ApiChannelMixin(object):
    """
    Defines model_for_source_url for cities_reduced_fat.contrib.restframework.
    """
    def model_for_source_url(self, url):
        """
        Return the appropriate model for the urls defined by
        cities_reduced_fat.contrib.restframework.urlpatterns.
        """
        if 'cities_reduced_fat/city/' in url:
            return City
        elif 'cities_reduced_fat/country/' in url:
            return Country


class RemoteCityChannel(CityChannelMixin, ApiChannelMixin,
    autocomplete_light.RemoteChannelBase):
    """
    Remote channel for City that is compatible with
    cities_reduced_fat.contrib.restframework.
    """

    def get_source_url_data(self, limit):
        """
        Converts country__pk data to country__name, to avoid PK conflict hell.

        The author insists that he learnt this the hard way.
        """
        data = super(RemoteCityChannel, self).get_source_url_data(limit)
        country_pk = data.pop('country__pk')
        data['country_name'] = Country.objects.get(pk=country_pk).name
        return data


class RemoteCountryChannel(ApiChannelMixin,
    autocomplete_light.RemoteChannelBase):
    """
    Remote channel for Country that is compatible with
    cities_reduced_fat.contrib.restframework.
    """
    pass
