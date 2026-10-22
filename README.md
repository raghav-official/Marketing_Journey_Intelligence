<img width="1327" height="746" alt="Marketing journey intelligence" src="https://github.com/user-attachments/assets/acc7ee8f-d941-4cb4-9500-8ddea8179632" />
# Marketing Journey Intelligence

**Which marketing channels actually influence customers across the whole journey, not just the one that gets last-click credit?**

An end-to-end B2B SaaS marketing attribution project: Excel -> SQL Server -> Power BI. It compares four attribution models, classifies each channel by funnel role, and finds the journey sequences that convert best.

> **The data is synthetic.** It simulates a fictional B2B SaaS company ("Cobalt Metrics", marketing attribution software) with 5,000 customer journeys and 18,620 touchpoints. Channels were weighted toward funnel stages so the models disagree, so the findings below show the **method**, not real market results. See [limitations](docs/methodology.md#limitations).

## Dashboard

| Journey Overview | Attribution Comparison |
|---|---|
| ![Journey Overview](images/page1_journey_overview.png) | ![Attribution Comparison](images/page2_attribution_comparison.png) |
| **Journey Intelligence** | **Decision Center** |
| ![Journey Intelligence](images/page3_journey_intelligence.png) | ![Decision Center](images/page4_decision_center.png) |

## Key findings

1. **Attribution model choice changes which channels look valuable.** Email gets 39.7% of conversions under Last Touch but only 4.6% under First Touch. Google Ads is the reverse: 20.5% First Touch, 7.8% Last Touch.
2. **Early-funnel channels are invisible to last-click.** LinkedIn Ads, Meta Ads, Content Marketing and Referral get 0% Last Touch, yet LinkedIn is the first touch for 18.6% of converted journeys and Content for 11.7%.
3. **Channels play distinct roles.** Meta and Referral work mainly at Awareness, Content, Retargeting and Webinar at Intent, and Email and Direct close.
4. **Opening channel + Email converts best.** `Meta Ads > Email` converts at 41.7%, `Referral > Email` 38.5%, `Google Ads > Email` 36.0%, against an 18.6% overall rate. These rest on small counts (5-10 conversions each) and are directional.
5. **Most journeys never convert.** 4,072 of 5,000 (81.4%) are lost; Considered Buyers (3-5 touchpoints) are the largest converting group (512).

Headline numbers: 5,000 journeys, 928 converted (18.6%), 3.72 average touchpoints, 13.68 average journey days, about INR 11.3 crore total revenue.

**Recommendation pattern:** Protect Email (main closer), Invest in LinkedIn and Content (they start journeys), Optimize Google Ads (check cost per acquisition), Investigate Meta Ads (awareness traffic that does not reach intent).

## Tech stack
Excel (data and QA) - SQL Server Express + SSMS (T-SQL views, window functions) - Power BI Desktop (DAX) - Python (synthetic data generator).


## How to reproduce
1. `pip install -r requirements.txt`, then `python data_generation/generate_data.py` (writes `data/touchpoints.csv` and the workbook).
2. In SQL Server, load `touchpoints.csv` into a `touchpoints` table in a database named `CobaltMetrics` (SSMS Import Flat File wizard, or `sql/01_create_table.sql`).
3. Run `sql/02` to `sql/06` in order to create the views.
4. Run `sql/07_validation_checks.sql`. Expect 18,620 rows, 5,000 journeys, 928 conversions, and 928 attributed conversions under every model.
5. In Power BI Desktop: Get Data -> SQL Server -> `localhost\SQLEXPRESS` / `CobaltMetrics` -> load `touchpoints` and the four views. Add the measures from `powerbi/dax_measures.md` and build the four pages.

## Skills demonstrated
Multi-touch attribution modelling - T-SQL (CTEs, window functions, `STRING_AGG`, views) - DAX measures and filter context - funnel and journey analysis - dashboard design - documenting assumptions and limitations.

## Possible extensions
Add channel spend to compute cost per acquisition, run the analysis at account level, and test a data-driven (Markov) attribution model.

