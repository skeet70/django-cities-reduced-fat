from django.contrib import admin

from .models import *
from .settings import *


class CountryAdmin(admin.ModelAdmin):
    """
    ModelAdmin for Country.
    """

    list_display = (
        'name',
        'code2',
        'code3',
        'continent',
        'tld',
    )
    search_fields = (
        'name',
        'name_ascii',
        'code2',
        'code3',
        'tld'
    )
    list_filter = (
        'continent',
    )
admin.site.register(Country, CountryAdmin)


class RegionAdmin(admin.ModelAdmin):
    list_display = (
        'country', 'code', 'name'
    )
    list_filter = (
        'country__continent',
        'country',
    )
admin.site.register(Region, RegionAdmin)


class CityAdmin(admin.ModelAdmin):
    """
    ModelAdmin for City.
    """
    list_display = (
        'name',
        'country',
        'region',
    )
    search_fields = (
        'name',
        'search_names',
    )
    list_filter = (
        'country__continent',
        'country',
    )

admin.site.register(City, CityAdmin)
