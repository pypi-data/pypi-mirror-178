from typing import Dict, List, Optional, Tuple
import requests as r
from bs4 import BeautifulSoup as bs
import geopandas as gpd

class _Internal:
    DATA_BASE_URL = "https://geodata.ucdavis.edu/gadm/"

class Country(_Internal):
    def __init__(self, code: Optional[str]=None, level:int=0, version:Optional[str]=None):
        self.code: Optional[str] = code
        self.level = level
        self.version: Optional[str] = version
        self.options: Dict[str, List[int]] = {}
        self.data: Optional[gpd.GeoDataFrame] = None

        self.__get_posible_country_codes_with_level()
        self.__download()

    def __download(self):
        if self.version is None:
            self.version = self.__get_latest_version()
            print(self.version)
        if self.code is None:
            raise ValueError("Country code must be specified")

        if self.code not in self.options.keys():
            raise ValueError(f"Country code {self.code} not found")
        elif self.level not in self.options[self.code]:
            raise ValueError(f"Level {self.level} not found for country {self.code}")

        version = self.version.replace('.','')
        url = f"{self.DATA_BASE_URL}gadm{self.version}/json/gadm{version}_{self.code}_{self.level}.json"

        response = r.get(url)

        if response.status_code == 404:
            raise ValueError(f"Country code {self.code} with level {self.level} not found")

        data = response.json()
        self.data = gpd.GeoDataFrame.from_features(data['features'])

    def __get_latest_version(self):
        page = r.get(self.DATA_BASE_URL)
        soup = bs(page.content, 'html.parser')
        links = soup.find_all('a')
        versions = [link.text.replace('gadm','').replace('/', '') for link in links if link.text.startswith('gadm') and link.text.endswith('/')]
        versions = {int(version.replace('.','')):version for version in versions}
        return versions[max(versions.keys())]

    def __get_posible_country_codes_with_level(self):
        if self.version is None:
            self.version = self.__get_latest_version()

        url = f"{self.DATA_BASE_URL}gadm{self.version}.txt"
        response = r.get(url)
        if response.status_code == 404:
            raise ValueError(f"Version {self.version} not found")

        data = response.text.split('\n')
        version = self.version.replace('.','')
        data = [line.replace(f'gadm{version}_', '').replace('_pk.rds', '') for line in data if line.startswith(f'gadm{version}_')]
        data = [line.split('_') for line in data]
        for country, level in data:
            if country not in self.options:
                self.options[country] = []
            self.options[country].append(int(level))

    def get_coordinates(self) -> List[Tuple[float, float]]:
        if self.data is None:
            self.__download()

        if self.data is None:
            raise ValueError("Data not found")

        def coords_lister(geom):
            if geom.type == 'Polygon':
                coords = list(geom.exterior.coords)
                return coords
            elif geom.type == 'MultiPolygon':
                coords = []
                for poly in geom.geoms:
                    coords.extend(list(poly.exterior.coords))
                return coords


        return list(self.data.geometry.apply(coords_lister))[0]

    def get_gpd(self) -> gpd.GeoDataFrame:
        if self.data is None:
            self.__download()

        if self.data is None:
            raise ValueError("Data not found")

        return self.data
