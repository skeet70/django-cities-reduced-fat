import urllib
import time
import os
import os.path
import logging
import zipfile
import optparse
import unicodedata

from django.core.management.base import BaseCommand
from django.utils.encoding import force_unicode

from ...exceptions import InvalidItems
from ...signals import city_items_pre_import
from ...models import Country, Region, City
from ...settings import DATA_DIR, SOURCES, COUNTRY_SOURCES, REGION_SOURCES, CITY_SOURCES


class Command(BaseCommand):
    args = '''
[--force-all] [--force-import-all \\]
                              [--force-import countries.txt cities.txt ...] \\
                              [--force countries.txt cities.txt ...]
    '''.strip()
    help = '''
Download all files in CITIES_REDUCED_FAT_COUNTRY_SOURCES if they were updated or if
--force-all option was used.
Import country data if they were downloaded or if --force-import-all was used.

Same goes for CITIES_REDUCED_FAT_CITY_SOURCES.

It is possible to force the download of some files which have not been updated
on the server:

    manage.py --force cities15000.txt countryInfo.txt

It is possible to force the import of files which weren't downloaded using the
--force-import option:

    manage.py --force-import cities15000.txt countryInfo.txt
    '''.strip()

    logger = logging.getLogger('cities_reduced_fat')

    option_list = BaseCommand.option_list + (
        optparse.make_option('--force-import-all', action='store_true',
            default=False, help='Import even if files are up-to-date.'
        ),
        optparse.make_option('--force-all', action='store_true', default=False,
            help='Download and import if files are up-to-date.'
        ),
        optparse.make_option('--force-import', action='append', default=[],
            help='Import even if files matching files are up-to-date'
        ),
        optparse.make_option('--force', action='append', default=[],
            help='Download and import even if matching files are up-to-date'
        ),
    )

    def handle(self, *args, **options):
        if not os.path.exists(DATA_DIR):
            self.logger.info('Creating %s' % DATA_DIR)
            os.mkdir(DATA_DIR)

        for url in SOURCES:
            destination_file_name = url.split('/')[-1]
            destination_file_path = os.path.join(DATA_DIR,
                destination_file_name)

            force = options['force_all'] or \
                destination_file_name in options['force']
            downloaded = self.download(url, destination_file_path, force)

            if destination_file_name.split('.')[-1] == 'zip':
                # extract the destination file, use the extracted file as new
                # destination
                destination_file_name = destination_file_name.replace(
                    'zip', 'txt')

                self.extract(destination_file_path, destination_file_name)

                destination_file_path = os.path.join(
                    DATA_DIR, destination_file_name)

            force_import = options['force_import_all'] or \
                destination_file_name in options['force_import']

            if downloaded or force_import:
                self.logger.info('Importing %s' % destination_file_name)

                if url in CITY_SOURCES:
                    self.city_import(destination_file_path)
                elif url in COUNTRY_SOURCES:
                    self.country_import(destination_file_path)
                if url in REGION_SOURCES:
                    self.region_import(destination_file_path)

    def download(self, url, path, force=False):
        remote_file = urllib.urlopen(url)
        remote_time = time.strptime(remote_file.headers['last-modified'],
            '%a, %d %b %Y %H:%M:%S %Z')
        remote_size = int(remote_file.headers['content-length'])

        if os.path.exists(path) and not force:
            local_time = time.gmtime(os.path.getmtime(path))
            local_size = os.path.getsize(path)

            if local_time >= remote_time and local_size == remote_size:
                self.logger.warning(
                    'Assuming local download is up to date for %s' % url)

                return False

        self.logger.info('Downloading %s into %s' % (url, path))
        with open(path, 'wb') as local_file:
            chunk = remote_file.read()
            while chunk:
                local_file.write(chunk)
                chunk = remote_file.read()

        return True

    def extract(self, zip_path, file_name):
        destination = os.path.join(DATA_DIR, file_name)

        self.logger.info('Extracting %s from %s into %s' % (
            file_name, zip_path, destination))

        zip_file = zipfile.ZipFile(zip_path)
        if zip_file:
            with open(destination, 'wb') as destination_file:
                destination_file.write(zip_file.read(file_name))

    def parse(self, file_path):
        file = open(file_path, 'r')
        line = True

        while line:
            line = file.readline().strip()

            if len(line) < 1 or line[0] == '#':
                continue

            yield [e.strip() for e in line.split('\t')]

    def _get_country(self, code2):
        '''
        Simple lazy identity map for code2->country
        '''
        if not hasattr(self, '_country_codes'):
            self._country_codes = {}

        if code2 not in self._country_codes.keys():
            self._country_codes[code2] = Country.objects.get(code2=code2)

        return self._country_codes[code2]

    def country_import(self, file_path):
        for items in self.parse(file_path):
            try:
                country = Country.objects.get(code2=items[0])
            except Country.DoesNotExist:
                country = Country(code2=items[0])

            country.name = items[4]
            country.code3 = items[1]
            country.continent = items[8]
            country.tld = items[9][1:]  # strip the leading dot
            country.save()

    def region_import(self, file_path):
        for items in self.parse(file_path):
            code2, id = items[0].split('.')
            kwargs = dict(code=id, country=self._get_country(code2))
            try:
                region = Region.objects.get(**kwargs)
            except Region.DoesNotExist:
                region = Region(**kwargs)
            region.name = items[2]
            region.save()

    def _normalize_search_names(self, search_names):
        if isinstance(search_names, str):
            search_names = force_unicode(search_names)

        return unicodedata.normalize('NFKD', search_names).encode(
             'ascii', 'ignore')

    def city_import(self, file_path):
        for items in self.parse(file_path):
            try:
                city_items_pre_import.send(sender=self, items=items)
            except InvalidItems:
                continue

            country = self._get_country(items[8])
            kwargs = dict(name=items[1], country=country)

            try:
                city = City.objects.get(**kwargs)
            except City.DoesNotExist:
                city = City(**kwargs)

            save = False
            if not city.latitude:
                city.latitude = items[4]
                save = True
            if not city.longitude:
                city.longitude = items[5]
                save = True

            if not city.search_names:
                # remove commas for names that are empty after normalization
                search_names = []
                for name in self._normalize_search_names(items[3]).split(','):
                    name = name.strip()
                    if name:
                        search_names.append(name)
                search_names = ','.join(search_names)
                if search_names:
                    city.search_names = search_names
                    save = True

            if not city.geoname_id:
                # city may have been added manually
                city.geoname_id = items[0]
                try:
                    city.region = Region.objects.get(country=country, code=items[10])
                except Region.DoesNotExist:
                    pass
                save = True

            if save:
                city.save()
