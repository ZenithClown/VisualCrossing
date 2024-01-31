CREATE TABLE `tblDailyWeather` (
    _id INTEGER PRIMARY KEY AUTO_INCREMENT,

    /* Primary Identifier Fileds */
    EffectiveDate    DATE NOT NULL,
    CityUUID         VARCHAR(36) NOT NULL,
    ResolvedLocation VARCHAR(128) NOT NULL COMMENT 'Send the Resolved Address as Provided by Visual Crossing API',
    
    /* Daily Temperature Information */
    TempAvg DECIMAL(5, 2) DEFAULT NULL,
    TempMin DECIMAL(5, 2) DEFAULT NULL,
    TempMax DECIMAL(5, 2) DEFAULT NULL,
    
    FeelsLikeAvg DECIMAL(5, 2) DEFAULT NULL,
    FeelsLikeMin DECIMAL(5, 2) DEFAULT NULL,
    FeelsLikeMax DECIMAL(5, 2) DEFAULT NULL,

    DewTemp DECIMAL(5, 2) DEFAULT NULL,
    HumidityPercent DECIMAL(5, 2) DEFAULT NULL,

    PrecipAmt    DECIMAL(5, 2) DEFAULT NULL COMMENT 'Amount of Liquid Precipitation (or equivalent) Predicted to Fall in the Period',
    PrecipProb   DECIMAL(5, 2) DEFAULT NULL COMMENT 'Forecast Only, the likelihood of measurable precipitation ranging from (0 - 100)%',
    PrecipType   VARCHAR(128) DEFAULT NULL COMMENT 'CSV Value indicating the type(s) of expected precipitation expected or occured.',
    PrecipCover  DECIMAL(5, 2) DEFAULT NULL COMMENT 'The proportion fo hours where there was non-zero precipitation.',

    SnowCover DECIMAL(5, 2) DEFAULT NULL,
    SnowDepth DECIMAL(5, 2) DEFAULT NULL,

    WindDir      DECIMAL(5, 2) DEFAULT NULL,
    WindGust     DECIMAL(5, 2) DEFAULT NULL COMMENT 'Instantaneous speed, may be empty representing significantly lower wind speed.',
    WindSpeed    DECIMAL(5, 2) DEFAULT NULL,
    WindSpeedAvg DECIMAL(5, 2) DEFAULT NULL,
    WindSpeedMin DECIMAL(5, 2) DEFAULT NULL,
    WindSpeedMax DECIMAL(5, 2) DEFAULT NULL,

    AtmPressure    DECIMAL(5, 2) DEFAULT NULL COMMENT 'Sea level atmospheric pressure in millibars.',
    CloudCoverage  DECIMAL(5, 2) DEFAULT NULL COMMENT 'Percentage of sky covered in cloud raning from (0 - 100)%',
    VisibilityDist DECIMAL(5, 2) DEFAULT NULL,

    UVIndex DECIMAL(5, 2) DEFAULT NULL COMMENT 'A value between 0 to 10, where 0 = lowest exposure and 10 is the highest exposure for that hour/day.',
    SevereRisk DECIMAL(5, 2) DEFAULT NULL COMMENT 'Forecast Only, A value between 0 to 100 representing convective storms.',

    SolarEnergy DECIMAL(5, 2) DEFAULT NULL COMMENT 'Solar Energy in MJ/m^2',
    SolarRadiation DECIMAL(5, 2) DEFAULT NULL COMMENT 'Solar Radion in W/m^2',

    SunRise   DATETIME DEFAULT NULL,
    SunSet    DATETIME DEFAULT NULL,
    MoonPhase DECIMAL(5, 2) DEFAULT NULL COMMENT 'Value range from 0.0 (new moon) to 0.5 (full moon) to 1.0 (next new moon).',

    WeatherIcon VARCHAR(12) DEFAULT NULL,
    WeatherCond VARCHAR(16) DEFAULT NULL,
    WeatherDesc VARCHAR(64) DEFAULT NULL,

    _source   VARCHAR(12) NOT NULL COMMENT 'Type of weather data used - obs, fcst, histfcst, or stats.',
    _stations VARCHAR(512) DEFAULT NULL COMMENT 'CSV values of weather statiosn names which was used to buold the data.',
    
    UNIQUE KEY `ck_weather_record` (EffectiveDate, CityUUID)
);


CREATE TABLE `dbo.mwVCWeatherStations` (
    VCWeatherStationID VARCHAR(16) PRIMARY KEY COMMENT 'Station ID as represented in Visual Crossing API',

    StationName         VARCHAR(32) UNIQUE NOT NULL,
    StationLatitude     DECIMAL(18, 6) NULL,
    StationLongitude    DECIMAL(18, 6) NULL,
    StationQuality      DECIMAL(5, 2) NULL,
    StationContribution DECIMAL(5, 2) NULL
);
