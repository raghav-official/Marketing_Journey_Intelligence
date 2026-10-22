-- 03_vw_attribution_all.sql
-- Zero-fills the base view so every channel appears under every model (4 models x 10 channels = 40 rows).
-- Power BI reads this view, so channels with no credit (e.g. LinkedIn under Last Touch) show 0, not blank.
USE CobaltMetrics;
GO
CREATE OR ALTER VIEW vw_attribution_all AS
SELECT m.model, c.channel,
       COALESCE(a.attributed_conversions, 0) AS attributed_conversions,
       COALESCE(a.attributed_revenue, 0)     AS attributed_revenue
FROM (SELECT DISTINCT model   FROM vw_attribution_base) m
CROSS JOIN (SELECT DISTINCT channel FROM vw_attribution_base) c
LEFT JOIN vw_attribution_base a ON a.model = m.model AND a.channel = c.channel;
GO
