-- 02_vw_attribution_base.sql
-- Four attribution models stacked into one result: model, channel, attributed_conversions, attributed_revenue.
-- Only converted journeys are credited, so every model distributes the same 928 conversions differently.
USE CobaltMetrics;
GO
CREATE OR ALTER VIEW vw_attribution_base AS
WITH converting AS (
    SELECT DISTINCT Journey_ID AS journey_id FROM touchpoints WHERE Conversion = 1
),
counts AS (                       -- touchpoints per converted journey (used by Linear)
    SELECT Journey_ID AS journey_id, COUNT(*) AS n_touch
    FROM touchpoints
    WHERE Journey_ID IN (SELECT journey_id FROM converting)
    GROUP BY Journey_ID
),
revenue AS (                      -- deal value sits only on the purchase row
    SELECT Journey_ID AS journey_id, Revenue AS revenue FROM touchpoints WHERE Conversion = 1
),
positioned AS (                   -- position of each touchpoint within its journey
    SELECT t.*,
           ROW_NUMBER() OVER (PARTITION BY t.Journey_ID ORDER BY t.Touchpoint) AS rn,
           COUNT(*) OVER (PARTITION BY t.Journey_ID) AS n_touch2
    FROM touchpoints t
    WHERE t.Journey_ID IN (SELECT journey_id FROM converting)
)
-- 1) First Touch: 100% to touchpoint 1
SELECT 'First Touch' AS model, t.Channel AS channel,
       COUNT(*) AS attributed_conversions, SUM(r.revenue) AS attributed_revenue
FROM touchpoints t
JOIN revenue r ON t.Journey_ID = r.journey_id
WHERE t.Touchpoint = 1
GROUP BY t.Channel

UNION ALL
-- 2) Last Touch: 100% to the purchase touchpoint
SELECT 'Last Touch', Channel, COUNT(*), SUM(Revenue)
FROM touchpoints
WHERE Conversion = 1
GROUP BY Channel

UNION ALL
-- 3) Linear: 1/N to every touchpoint
SELECT 'Linear', t.Channel, SUM(1.0 / c.n_touch), SUM(r.revenue * 1.0 / c.n_touch)
FROM touchpoints t
JOIN counts c  ON t.Journey_ID = c.journey_id
JOIN revenue r ON t.Journey_ID = r.journey_id
GROUP BY t.Channel

UNION ALL
-- 4) Position-Based: 40% first, 40% last, 20% shared by the middle (1 touch: 100%; 2 touches: 50/50)
SELECT 'Position-Based', w.Channel,
    SUM(CASE WHEN w.n_touch2 = 1 THEN 1.0
             WHEN w.n_touch2 = 2 THEN 0.5
             WHEN w.rn = 1 THEN 0.4
             WHEN w.rn = w.n_touch2 THEN 0.4
             ELSE 0.2 / (w.n_touch2 - 2) END),
    SUM(r.revenue * (CASE WHEN w.n_touch2 = 1 THEN 1.0
             WHEN w.n_touch2 = 2 THEN 0.5
             WHEN w.rn = 1 THEN 0.4
             WHEN w.rn = w.n_touch2 THEN 0.4
             ELSE 0.2 / (w.n_touch2 - 2) END))
FROM positioned w
JOIN revenue r ON w.Journey_ID = r.journey_id
GROUP BY w.Channel;
GO
