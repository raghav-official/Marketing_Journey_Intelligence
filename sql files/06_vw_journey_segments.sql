-- 06_vw_journey_segments.sql
-- Tags every journey: Fast Converter (1-2 touches), Considered Buyer (3-5), Long Journey (6+), Lost Journey (no purchase).
USE CobaltMetrics;
GO
CREATE OR ALTER VIEW vw_journey_segments AS
SELECT Journey_ID,
       COUNT(*) AS n_touch,
       MAX(CASE WHEN Conversion = 1 THEN 1 ELSE 0 END) AS converted,
       CASE WHEN MAX(CASE WHEN Conversion = 1 THEN 1 ELSE 0 END) = 0 THEN 'Lost Journey'
            WHEN COUNT(*) <= 2 THEN 'Fast Converter'
            WHEN COUNT(*) <= 5 THEN 'Considered Buyer'
            ELSE 'Long Journey' END AS segment
FROM touchpoints
GROUP BY Journey_ID;
GO
