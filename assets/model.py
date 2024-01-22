# -*- encoding: utf-8 -*-

"""
A Simple and Effective Model for Consuming Historical Weather

A simple model is created that can be used to store historical
weather information into the database, and to retrieve the data
from your own data warehouse. Check table information for usages.

@author:  Debmalya Pramanik
@version: v0.0.1
"""

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Date, DateTime, Integer, Numeric, String, UniqueConstraint

# create an con/enging object using `sqlalchemy` or any db-drivers
engine = None # recommended to use sqlalchemy
declarative_base_ = declarative_base()

class DailyWeatherLog(declarative_base_):
    __tablename__ = "trx.weather.daily_log"

    # need pk in field https://github.com/sqlalchemy/sqlalchemy/discussions/5771
    _id = Column(Integer, primary_key = True, autoincrement = True)
    
    # this is a daily weather log, so indexation will be on date, location
    effective_date = Column(Date(), nullable = False)

    # visual crossing returns nearest place data, if:
    # the provided location (lat, lon) is not available, thus:
    location_pd = Column(String(32), nullable = False) # provided location
    resolved_ad = Column(String(32), nullable = False) # resolved address by vc
    resolved_tz = Column(String(32), nullable = False) # resolved timezone by vc

    # ! all the below are weather parameter, and is nullable, as not available
    temeperate = Column(Numeric(5, 2), nullable = True)
    temeperate_min = Column(Numeric(5, 2), nullable = True)
    temeperate_max = Column(Numeric(5, 2), nullable = True)

    feelslike = Column(Numeric(5, 2), nullable = True)
    feelslike_min = Column(Numeric(5, 2), nullable = True)
    feelslike_max = Column(Numeric(5, 2), nullable = True)

    dew = Column(Numeric(5, 2), nullable = True)
    humidity = Column(Numeric(5, 2), nullable = True)

    precipitation = Column(Numeric(5, 2), nullable = True)
    precipitation_type = Column(String(64), nullable = True)
    precipitation_cover = Column(Numeric(5, 2), nullable = True)
    precipitation_probability = Column(Numeric(5, 2), nullable = True)

    snow = Column(Numeric(5, 2), nullable = True)
    snow_depth = Column(Numeric(5, 2), nullable = True)

    wind_gust = Column(Numeric(5, 2), nullable = True)
    wind_speed = Column(Numeric(5, 2), nullable = True)
    wind_direction = Column(Numeric(5, 2), nullable = True)

    pressure = Column(Numeric(5, 2), nullable = True)

    cloud_cover = Column(Numeric(5, 2), nullable = True)

    visibility = Column(Numeric(5, 2), nullable = True)

    uv_index = Column(Numeric(5, 2), nullable = True)
    severe_risk = Column(Numeric(5, 2), nullable = True)
    solar_energy = Column(Numeric(5, 2), nullable = True)
    solar_radiation = Column(Numeric(5, 2), nullable = True)

    # sunrise and sunset is datetime
    sunrise = Column(DateTime(timezone = False), nullable = True)
    sunset = Column(DateTime(timezone = False), nullable = True)

    moon_phase = Column(Numeric(5, 2), nullable = True)

    weather_icon = Column(String(12), nullable = True)
    weather_condition = Column(String(16), nullable = True)
    weather_description = Column(String(64), nullable = True)

    weather_data_source = Column(String(8), nullable = True)
    collected_weather_stations = Column(String(512), nullable = True)

    # ! added unique key indexing on date, location
    # pass as tuple: https://stackoverflow.com/a/11169106/6623589
    __table_args__ = (UniqueConstraint(effective_date, location_pd),)


class HourlyWeatherLog(declarative_base_):
    __tablename__ = "trx.weather.hourly_log"

    # need pk in field https://github.com/sqlalchemy/sqlalchemy/discussions/5771
    _id = Column(Integer, primary_key = True, autoincrement = True)
    
    # this is a daily weather log, so indexation will be on date, location
    effective_datetime = Column(DateTime(timezone = False), nullable = False)

    # visual crossing returns nearest place data, if:
    # the provided location (lat, lon) is not available, thus:
    location_pd = Column(String(32), nullable = False) # provided location
    resolved_ad = Column(String(32), nullable = False) # resolved address by vc
    resolved_tz = Column(String(32), nullable = False) # resolved timezone by vc

    # ! all the below are weather parameter, and is nullable, as not available
    temeperate = Column(Numeric(5, 2), nullable = True)
    feelslike = Column(Numeric(5, 2), nullable = True)

    dew = Column(Numeric(5, 2), nullable = True)
    humidity = Column(Numeric(5, 2), nullable = True)

    precipitation = Column(Numeric(5, 2), nullable = True)
    precipitation_type = Column(String(64), nullable = True)
    precipitation_cover = Column(Numeric(5, 2), nullable = True)
    precipitation_probability = Column(Numeric(5, 2), nullable = True)

    snow = Column(Numeric(5, 2), nullable = True)
    snow_depth = Column(Numeric(5, 2), nullable = True)

    wind_gust = Column(Numeric(5, 2), nullable = True)
    wind_speed = Column(Numeric(5, 2), nullable = True)
    wind_direction = Column(Numeric(5, 2), nullable = True)

    pressure = Column(Numeric(5, 2), nullable = True)

    cloud_cover = Column(Numeric(5, 2), nullable = True)

    visibility = Column(Numeric(5, 2), nullable = True)

    uv_index = Column(Numeric(5, 2), nullable = True)
    severe_risk = Column(Numeric(5, 2), nullable = True)
    solar_energy = Column(Numeric(5, 2), nullable = True)
    solar_radiation = Column(Numeric(5, 2), nullable = True)

    weather_icon = Column(String(12), nullable = True)
    weather_condition = Column(String(16), nullable = True)
    weather_description = Column(String(64), nullable = True)

    weather_data_source = Column(String(8), nullable = True)
    collected_weather_stations = Column(String(512), nullable = True)

    # ! added unique key indexing on date, location
    # pass as tuple: https://stackoverflow.com/a/11169106/6623589
    __table_args__ = (UniqueConstraint(effective_datetime, location_pd),)


if __name__ == "__main__":
    declarative_base_.metadata.create_all(engine)
    engine.close()
