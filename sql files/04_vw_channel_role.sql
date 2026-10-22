-- 04_vw_channel_role.sql
-- Channel Role Matrix: what share of each channel's touchpoints falls in each funnel stage.
-- stage_order lets Power BI sort the stages Awareness > Engagement > Intent > Conversion.
USE CobaltMetrics;
GO
CREATE OR ALTER VIEW vw_channel_role AS
SELECT Channel,
       Touchpoint_Type,
       CASE Touchpoint_Type
            WHEN 'Awareness'  THEN 1
            WHEN 'Engagement' THEN 2
            WHEN 'Intent'     THEN 3
            WHEN 'Conversion' THEN 4
       END AS stage_order,
       COUNT(*) AS touchpoints,
       CAST(COUNT(*) * 100.0 / SUM(COUNT(*)) OVER (PARTITION BY Channel) AS DECIMAL(5,1)) AS pct_of_channel
FROM touchpoints
GROUP BY Channel, Touchpoint_Type;
GO
