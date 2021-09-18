# Dependencies and Setup
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from pandas.core.frame import DataFrame
import requests
import time, json, os, csv

from scipy.stats import linregress
from citipy import citipy
from pprint import pprint

# Hi Markers, please use your onw API keys to run the script, thank you!
from api_keys import weather_api_key
from api_keys import g_key

# Define function to set data type
def set_integer(data_type, pddf):
    for row in data_type:
        pddf[row] = pddf[row].astype(int)

def clean_house_data(house_data: DataFrame, column_to_int_list: list[str]) -> DataFrame:
    house_data_cleaned = house_data.dropna(subset = ["Price"])
    house_data_cleaned = house_data_cleaned.drop(["Bedroom2"], axis = "columns")
    house_data_cleaned = house_data_cleaned.fillna(0)
    set_integer(column_to_int_list, house_data_cleaned)
    house_data_cleaned["Price"] = house_data_cleaned.apply(lambda x: "{:,.0f}".format(x["Price"]), axis = 1)
    return house_data_cleaned

def clean_school_data(school_data: DataFrame) -> DataFrame:
    school_data_cleaned = school_data.drop(["SCHOOL_NO",
                                            "Address_Line_2",
                                            "Postal_Address_Line_1",
                                            "Postal_Address_Line_2",
                                            "Postal_Town",
                                            "Postal_State",
                                            "Postal_Postcode"], axis = "columns")

    school_data_cleaned = school_data_cleaned.rename({"X": "Lng",
                                                      "Y": "Lat",
                                                      "Address_Line_1": "Address",
                                                      "Address_Town": "Suburb",
                                                      "Address_State": "State",
                                                      "Address_Postcode": "Postcode"}, axis = "columns")
    return school_data_cleaned

def clean_crime_data(crime_data: DataFrame) -> DataFrame:
    crime_data_cleaned = crime_data.loc[(crime_data["Year"] >= 2016) &
                                        (crime_data["Year"] <= 2018)].dropna()
    crime_data_cleaned = crime_data_cleaned.reset_index(drop = True)
    return crime_data_cleaned