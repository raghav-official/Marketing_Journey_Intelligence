-- 07_validation_checks.sql
-- Run after the views exist. Expected values are for the dataset in this repo.
USE CobaltMetrics;
GO
SELECT COUNT(*) AS touchpoint_rows FROM touchpoints;                          -- 18,620
SELECT COUNT(DISTINCT Journey_ID) AS journeys FROM touchpoints;               -- 5,000
SELECT COUNT(DISTINCT Journey_ID) AS converted_journeys
FROM touchpoints WHERE Conversion = 1;                                        -- 928

-- Every model must distribute the same 928 conversions and the same revenue
SELECT model, ROUND(SUM(attributed_conversions), 1) AS total_conversions,
       ROUND(SUM(attributed_revenue), 0) AS total_revenue
FROM vw_attribution_all GROUP BY model;

SELECT model, COUNT(*) AS rows_per_model FROM vw_attribution_all GROUP BY model;   -- 10 each

SELECT segment, COUNT(*) AS journeys FROM vw_journey_segments GROUP BY segment;
-- Lost 4,072 | Considered 512 | Fast 216 | Long 200

SELECT DISTINCT Touchpoint_Type, stage_order FROM vw_channel_role ORDER BY stage_order;  -- 1 to 4
