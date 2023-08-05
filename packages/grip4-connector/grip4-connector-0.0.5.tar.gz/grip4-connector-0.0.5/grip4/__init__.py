import os
from tempfile import gettempdir
from typing import Optional, Union
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


class Region(_Internal):
    def __init__(self, region: Union[str, int], country: Optional[str] = None):
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
        file = os.path.join(gettempdir(), "grip4", f"GRIP4_Region{self.region}_vector_country_{country.numeric}.shp")

        if not os.path.exists(file):
            raise FileNotFoundError(f"File {file} not found.")

        return gpd.read_file(file)
