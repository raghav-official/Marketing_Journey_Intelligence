-- 01_create_table.sql
-- Creates the CobaltMetrics database and the touchpoints table, then loads touchpoints.csv.
-- Easier alternative: SSMS > right-click the database > Tasks > Import Flat File (used to build this project).
-- Use this script if you prefer a repeatable, scripted load.

IF DB_ID('CobaltMetrics') IS NULL CREATE DATABASE CobaltMetrics;
GO
USE CobaltMetrics;
GO

-- Staging table: Conversion arrives as text ('Yes'/'No')
CREATE TABLE touchpoints_staging (
    Customer_ID     NVARCHAR(20),
    Journey_ID      NVARCHAR(30),
    Touchpoint      TINYINT,
    [Date]          DATE,
    Channel         NVARCHAR(50),
    Source_Medium   NVARCHAR(50),
    Campaign        NVARCHAR(150),
    Action          NVARCHAR(50),
    Touchpoint_Type NVARCHAR(20),
    Intent_Score    TINYINT,
    Conversion      NVARCHAR(5),
    Revenue         INT
);
GO

-- Change the path. The file must be readable by the SQL Server service account.
BULK INSERT touchpoints_staging
FROM 'C:\path\to\touchpoints.csv'
WITH (FORMAT = 'CSV', FIRSTROW = 2, FIELDTERMINATOR = ',', TABLOCK);
GO

-- Final table: Conversion stored as bit (1 = purchase row)
SELECT Customer_ID, Journey_ID, Touchpoint, [Date], Channel, Source_Medium, Campaign, Action,
       Touchpoint_Type, Intent_Score,
       CAST(CASE WHEN Conversion = 'Yes' THEN 1 ELSE 0 END AS BIT) AS Conversion,
       Revenue
INTO touchpoints
FROM touchpoints_staging;
GO

DROP TABLE touchpoints_staging;
GO
