-- 05_vw_journey_patterns.sql
-- Conversion rate by channel sequence (path). Keeps paths seen at least 10 times.
-- Requires SQL Server 2017+ (STRING_AGG).
USE CobaltMetrics;
GO
CREATE OR ALTER VIEW vw_journey_patterns AS
WITH j AS (
    SELECT Journey_ID,
           STRING_AGG(Channel, ' > ') WITHIN GROUP (ORDER BY Touchpoint) AS path,
           COUNT(*) AS n_touch,
           MAX(CASE WHEN Conversion = 1 THEN 1 ELSE 0 END) AS converted,
           SUM(Revenue) AS revenue
    FROM touchpoints
    GROUP BY Journey_ID
)
SELECT path,
       COUNT(*) AS journeys,
       SUM(converted) AS conversions,
       CAST(SUM(converted) * 100.0 / COUNT(*) AS DECIMAL(5,1)) AS conv_rate_pct,
       AVG(CASE WHEN converted = 1 THEN revenue END) AS avg_revenue,
       AVG(n_touch * 1.0) AS avg_touchpoints
FROM j
GROUP BY path
HAVING COUNT(*) >= 10;
GO
