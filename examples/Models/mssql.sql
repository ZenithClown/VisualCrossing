-- ****************************** [Weather]**************************
CREATE TABLE [Weather]
(
 [LocationId]         int NULL ,
 [EffectiveDate]      date NOT NULL ,
 [Revision]           int NOT NULL ,
 [MaxTemp]            float NOT NULL ,
 [MinTemp]            float NOT NULL ,
 [AvgTemp]            float NOT NULL ,
 [Rainfall]           float NOT NULL ,
 [DewPoint]           float NOT NULL ,
 [Relativehumidity]   float NOT NULL ,
 [HeatIndex]          float NOT NULL ,
 [WindSpeed]          float NOT NULL ,
 [WindDirection]      float NOT NULL ,
 [Precipitation]      float NOT NULL ,
 [PrecipitationCover] float NOT NULL ,
 [Visibility]         float NOT NULL ,
 [CloudCover]         float NOT NULL ,
 [SeaLevelPressure]   float NOT NULL ,
 [ResolvedAddress]    varchar(200) NOT NULL ,
 [InDataId]           varchar(10) NOT NULL ,
 [DataSourceId]       int NOT NULL ,
 [GroupId]            int NOT NULL ,
 [WeatherDataId]      int NOT NULL ,


 CONSTRAINT [PK_5] PRIMARY KEY CLUSTERED ([WeatherDataId] ASC),
 CONSTRAINT [FK_25] FOREIGN KEY ([LocationId])  REFERENCES [Location Data]([LocationId]),
 CONSTRAINT [FK_79] FOREIGN KEY ([DataSourceId])  REFERENCES [DataSource]([DataSourceId]),
 CONSTRAINT [FK_95] FOREIGN KEY ([GroupId])  REFERENCES [WeatherGroupMaster]([GroupId])
);
GO


CREATE NONCLUSTERED INDEX [fkIdx_27] ON [Weather] 
 (
  [LocationId] ASC
 )

GO

CREATE NONCLUSTERED INDEX [fkIdx_81] ON [Weather] 
 (
  [DataSourceId] ASC
 )

GO

CREATE NONCLUSTERED INDEX [fkIdx_97] ON [Weather] 
 (
  [GroupId] ASC
 )

GO


-- **************** [WeatherTypeMaster]
CREATE TABLE [WeatherTypeMaster]
(
 [WeatherTypeName] varchar(50) NOT NULL ,
 [GroupId]         int NOT NULL ,
 [WTypeId]         int NOT NULL ,


 CONSTRAINT [PK_84] PRIMARY KEY CLUSTERED ([WTypeId] ASC),
 CONSTRAINT [FK_92] FOREIGN KEY ([GroupId])  REFERENCES [WeatherGroupMaster]([GroupId])
);
GO


CREATE NONCLUSTERED INDEX [fkIdx_94] ON [WeatherTypeMaster] 
 (
  [GroupId] ASC
 )

GO

-- *************************** [WeatherGroupMaster]
CREATE TABLE [WeatherGroupMaster]
(
 [GroupId]   int NOT NULL ,
 [GroupName] varchar(100) NOT NULL ,
 [Keyword]   varchar(50) NOT NULL ,


 CONSTRAINT [PK_89] PRIMARY KEY CLUSTERED ([GroupId] ASC)
);
GO


-- *************************** [StateMaster]
CREATE TABLE [StateMaster]
(
 [StateId]   int NOT NULL ,
 [StateName] varchar(50) NOT NULL ,


 CONSTRAINT [PK_48] PRIMARY KEY CLUSTERED ([StateId] ASC)
);
GO


-- ******************** [RegionMaster]
CREATE TABLE [RegionMaster]
(
 [RegionId]   int NOT NULL ,
 [RegionName] varchar(10) NOT NULL ,


 CONSTRAINT [PK_68] PRIMARY KEY CLUSTERED ([RegionId] ASC)
);
GO


-- *************************** [Location Data]
CREATE TABLE [Location Data]
(
 [LocationId]     int NOT NULL ,
 [Name]           varchar(50) NOT NULL ,
 [StateId]        int NOT NULL ,
 [Address]        varchar(200) NOT NULL ,
 [Latitude]       nchar(10) NOT NULL ,
 [Longitude]      nchar(10) NOT NULL ,
 [InsertedOn]     datetime NOT NULL ,
 [UpdatedOn]      datetime NOT NULL ,
 [RegionId]       int NOT NULL ,
 [ResovedAddress] varchar(100) NOT NULL ,


 CONSTRAINT [PK_16] PRIMARY KEY CLUSTERED ([LocationId] ASC),
 CONSTRAINT [FK_57] FOREIGN KEY ([StateId])  REFERENCES [StateMaster]([StateId]),
 CONSTRAINT [FK_70] FOREIGN KEY ([RegionId])  REFERENCES [RegionMaster]([RegionId])
);
GO


CREATE NONCLUSTERED INDEX [fkIdx_59] ON [Location Data] 
 (
  [StateId] ASC
 )

GO

CREATE NONCLUSTERED INDEX [fkIdx_72] ON [Location Data] 
 (
  [RegionId] ASC
 )

GO

-- *************************** [DataSource]
CREATE TABLE [DataSource]
(
 [DataSourceId]   int NOT NULL ,
 [DataSourceName] varchar(50) NOT NULL ,
 [DataSourceType] varchar(20) NOT NULL ,


 CONSTRAINT [PK_76] PRIMARY KEY CLUSTERED ([DataSourceId] ASC)
);
GO
