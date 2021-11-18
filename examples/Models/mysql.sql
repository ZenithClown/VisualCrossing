-- DROP TABLE IF EXISTS visualcrossing.DataSource, visualcrossing.RegionMaster,visualcrossing.StateMaster,visualcrossing.WeatherGroupMaster,
-- visualcrossing.WeatherTypeMaster,visualcrossing.LocationData,visualcrossing.Weather;

CREATE TABLE visualcrossing.DataSource
(
 DataSourceId  int NOT NULL ,
 DataSourceName varchar(50) NOT NULL ,
 DataSourceType varchar(20) NOT NULL ,
 
  PRIMARY KEY (DataSourceId)
);

CREATE TABLE visualcrossing.RegionMaster
(
 RegionId   int NOT NULL ,
 RegionName varchar(10) NOT NULL ,
 
 PRIMARY KEY (RegionId)
);

CREATE TABLE visualcrossing.StateMaster
(
 StateId  int NOT NULL ,
 StateName varchar(50) NOT NULL ,

 PRIMARY KEY (StateId)
);

CREATE TABLE visualcrossing.WeatherGroupMaster
(
 GroupId   int NOT NULL ,
 GroupName varchar(100) NOT NULL ,
 Keyword  varchar(50) NOT NULL ,

 PRIMARY KEY (GroupId)
);

CREATE TABLE visualcrossing.WeatherTypeMaster
(
 WeatherTypeName varchar(50) NOT NULL ,
 GroupId         int NOT NULL ,
 WTypeId        int NOT NULL ,

PRIMARY KEY (WTypeId),
 FOREIGN KEY (GroupId)  REFERENCES WeatherGroupMaster(GroupId)
);


CREATE TABLE visualcrossing.LocationData
(
 LocationId     int NOT NULL ,
 Name           varchar(50) NOT NULL ,
 StateId        int NOT NULL ,
 Address        varchar(200) NOT NULL ,
 Latitude       nchar(10) NOT NULL ,
 Longitude      nchar(10) NOT NULL ,
 InsertedOn     datetime NOT NULL ,
 UpdatedOn      datetime NOT NULL ,
 RegionId       int NOT NULL ,
 ResovedAddress varchar(100) NOT NULL ,

 PRIMARY KEY (LocationId),
 FOREIGN KEY (StateId)  REFERENCES StateMaster(StateId),
 FOREIGN KEY (RegionId)  REFERENCES RegionMaster(RegionId)
);


CREATE TABLE visualcrossing.Weather
(
 LocationId        int NULL ,
 EffectiveDate    date NOT NULL ,
 Revision           int NOT NULL ,
 MaxTemp            float NOT NULL ,
 MinTemp            float NOT NULL ,
 AvgTemp            float NOT NULL ,
 Rainfall           float NOT NULL ,
 DewPoint           float NOT NULL ,
 Relativehumidity   float NOT NULL ,
 HeatIndex         float NOT NULL ,
 WindSpeed        float NOT NULL ,
 WindDirection     float NOT NULL ,
 Precipitation      float NOT NULL ,
 PrecipitationCover float NOT NULL ,
 Visibility         float NOT NULL ,
 CloudCover         float NOT NULL ,
 SeaLevelPressure  float NOT NULL ,
 ResolvedAddress    varchar(200) NOT NULL ,
 InDataId         varchar(10) NOT NULL ,
 DataSourceId       int NOT NULL ,
 GroupId            int NOT NULL ,
 WeatherDataId      int NOT NULL ,


PRIMARY KEY (WeatherDataId),
FOREIGN KEY (LocationId)  REFERENCES LocationData(LocationId),
FOREIGN KEY (DataSourceId)  REFERENCES DataSource(DataSourceId),
FOREIGN KEY (GroupId)  REFERENCES WeatherGroupMaster(GroupId)
);
