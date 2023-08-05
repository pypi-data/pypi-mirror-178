import os
from tempfile import gettempdir
from typing import Optional, Union
import gadm
import geopandas as gpd


class _Internal:
    DATA_BASE_URL = "https://dataportaal.pbl.nl/downloads/GRIP4/"
    REGIONS = {
        "North America": 1,
        "Central and South America": 2,
        "Africa": 3,
        "Europe": 4,
        "Middle East and Central Asia": 5,
        "South and East Asia": 6,
        "Oceania": 7,
    }


class Region(_Internal):
    def __init__(self, region: Union[str, int]):
        if isinstance(region, str):
            if region not in self.REGIONS:
                raise ValueError(f"Region {region} not found.")
            self.region = self.REGIONS[region]
        else:
            self.region = region

        self.filename = f"GRIP4_Region{self.region}_vector.shp"

        self.data: Optional[gpd.GeoDataFrame] = None

        self.__download()

    def __download(self):
        temp_dir = gettempdir()
        temp_dir = os.path.join(temp_dir, "grip4")

        if not os.path.exists(temp_dir):
            os.mkdir(temp_dir)

        temp_file = os.path.join(temp_dir, self.filename)

        if not os.path.exists(temp_file):
            print("Downloading data... This may take a while.")
            url = self.DATA_BASE_URL + f"GRIP4_Region{self.region}_vector_shp.zip"
            data: gpd.GeoDataFrame = gpd.read_file(url)
            data.to_file(temp_file)
            self.data = data
        else:
            self.data = gpd.read_file(temp_file)

    def get_gpd(self):
        if self.data is None:
            self.__download()

        if self.data is None:
            raise ValueError("Data not found.")

        return self.data

    def get_country(self, gadm_country_code: str):
        if self.data is None:
            self.__download()

        if self.data is None:
            raise ValueError("Data not found.")

        country = gadm.Country(gadm_country_code)
        country_gpd = country.get_gdp()

        grip4_country = gpd.clip(self.data, country_gpd)

        return grip4_country
