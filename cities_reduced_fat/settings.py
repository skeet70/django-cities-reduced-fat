"""
Settings for this application.

COUNTRY_SOURCES
    A list of urls to download country info from. Default is countryInfo.txt
    from geonames download server. Overridable in
    settings.CITIES_REDUCED_FAT_COUNTRY_SOURCES.

CITY_SOURCES
    A list of urls to download city info from. Default is cities15000.zip from
    geonames download server. Overridable in settings.CITIES_REDUCED_FAT_CITY_SOURCES

SOURCES
    A list with all sources, including city and coutry.

DATA_DIR
    Absolute path to download and extract data into. Default is
    cities_reduced_fat/data. Overridable in settings.CITIES_REDUCED_FAT_DATA_DIR
"""

import os.path

from django.conf import settings

__all__ = ['COUNTRY_SOURCES', 'REGION_SOURCES', 'CITY_SOURCES', 'SOURCES', 'DATA_DIR']

COUNTRY_SOURCES = getattr(settings, 'CITIES_REDUCED_FAT_COUNTRY_SOURCES',
    ['http://download.geonames.org/export/dump/countryInfo.txt'])
REGION_SOURCES = getattr(settings, 'CITIES_REDUCED_FAT_REGION_SOURCES',
    ['http://download.geonames.org/export/dump/admin1CodesASCII.txt'])
CITY_SOURCES = getattr(settings, 'CITIES_REDUCED_FAT_CITY_SOURCES',
    ['http://download.geonames.org/export/dump/cities15000.zip'])

SOURCES = list(COUNTRY_SOURCES) + list(REGION_SOURCES) + list(CITY_SOURCES)

DATA_DIR = getattr(settings, 'CITIES_REDUCED_FAT_DATA_DIR',
    os.path.normpath(os.path.join(
        os.path.dirname(os.path.realpath(__file__)), 'data')))
