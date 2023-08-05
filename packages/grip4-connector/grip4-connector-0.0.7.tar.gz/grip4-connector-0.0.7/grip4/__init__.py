import os
from tempfile import gettempdir
from typing import Any, Optional, Union
from pycountry import countries
import geopandas as gpd
import requests


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
    ROAD_TYPES = {
        "HIGHWAY": 1,
        "PRIMARY": 2,
        "SECONDARY": 3,
        "TERTIARY": 4,
        "LOCAL": 5,
        "OTHER": 0,
    }


class Region(_Internal):
    def __init__(self, region: Union[str, int]):
        if isinstance(region, str):
            if region not in self.REGIONS:
                raise ValueError(f"Region {region} not found.")
            self.region = self.REGIONS[region]
        else:
            self.region = region

        self.filename = f"GRIP4_Region{self.region}_vector_shp.zip"

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

            url = self.DATA_BASE_URL + self.filename
            response = requests.get(url, stream=True)

            open(temp_file, "wb").write(response.content)
            print("Download complete.")

            data: gpd.GeoDataFrame = gpd.read_file("zip://" + temp_file)

            for elem in data["GP_RCY"].unique():
                country = countries.get(numeric=elem)
                print(f"Saving {country.name}...")
                temp = data[data["GP_RCY"] == elem]
                temp.to_file(os.path.join(temp_dir, f"GRIP4_Region{self.region}_vector_country_{elem}.shp"))

    def get_gpd(self):
        files = os.listdir(gettempdir() + "/grip4")
        files = [file for file in files if file.startswith(f"GRIP4_Region{self.region}_vector_country_")]

        data = None

        for file in files:
            temp = gpd.read_file(gettempdir() + "/grip4/" + file)
            if data is None:
                data = temp
            else:
                data = data.append(temp)

        return data

    def get_country(self, alpha3: str):
        country = countries.get(alpha_3=alpha3)
        return _Country(self.region, country.numeric)


class _Country(_Internal):
    def __init__(self, region: int, country: int):
        self.region = region
        self.country = countries.get(numeric=country)
        self.filename = f"GRIP4_Region{self.region}_vector_country_{self.country.numeric}.shp"
        self.filters = {}

        self.data: Optional[gpd.GeoDataFrame] = None

        self.__get_data()

    def __get_data(self):
        temp_file = os.path.join(gettempdir(), "grip4", self.filename)

        if not os.path.exists(temp_file):
            raise FileNotFoundError(f"File {temp_file} not found.")

        self.data = gpd.read_file(temp_file)

    def get_gpd(self):
        if self.data is None:
            self.__get_data()

        return self.data

    def get_coordinates(self):
        if self.data is None:
            self.__get_data()

        if self.data is None:
            raise ValueError("No data found.")

        data = self.data

        for column, value in self.filters.items():
            data = data[data[column] == value]

        def coords_lister(geom):
            return list(geom.coords)

        coords = list(data.geometry.apply(coords_lister))

        coords = [item for sublist in coords for item in sublist]

        return coords

    def set_highways_filter(self):
        self.__filter("GP_RTP", self.ROAD_TYPES["HIGHWAY"])

    def set_primaries_filter(self):
        self.__filter("GP_RTP", self.ROAD_TYPES["PRIMARY"])

    def set_secondaries_filter(self):
        self.__filter("GP_RTP", self.ROAD_TYPES["SECONDARY"])

    def set_tertiaries_filter(self):
        self.__filter("GP_RTP", self.ROAD_TYPES["TERTIARY"])

    def set_locals_filter(self):
        self.__filter("GP_RTP", self.ROAD_TYPES["LOCAL"])

    def reset_filters(self):
        self.filters = {}

    def __filter(self, column: str, value: Any):
        if self.data is None:
            self.__get_data()

        if self.data is None:
            raise ValueError("No data found.")

        self.filters[column] = value
