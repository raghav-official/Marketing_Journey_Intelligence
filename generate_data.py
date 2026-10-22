"""
Generates the synthetic B2B SaaS marketing touchpoint dataset used in this project.

Company (fictional): Cobalt Metrics - sells marketing attribution software to other companies.
Output: ../data/touchpoints.csv and ../data/marketing_touchpoint_data.xlsx (plain, unformatted)

Run:  python generate_data.py
"""
import os
import random
import datetime as dt
import pandas as pd

random.seed(21)
N_JOURNEYS = 5000

STAGE_NAMES = ["Awareness", "Engagement", "Intent", "Conversion"]

INTENT_SCORE = {
    "Ad Impression": 1, "Social Impression": 1, "Content View": 2,
    "Ad Click": 3, "Website Visit": 3, "Blog Read": 3, "Video View": 3, "Email Open": 2,
    "Pricing Page View": 7, "Product Page View": 5, "Case Study Download": 6, "Webinar Registration": 6,
    "Demo Request": 9, "Trial Start": 9, "Purchase": 10,
}

GOOGLE_THEMES = ["Brand", "Competitor", "Generic - Marketing Attribution", "Generic - Analytics Software"]
GOOGLE_MATCH = ["Exact", "Phrase", "Broad"]
LINKEDIN_AUD = ["ABM - Marketing Leaders", "Lookalike - Customers", "Job Title - VP Marketing",
                "Job Title - Head of Growth", "Retarget - Website Visitors 30D"]
META_OBJ = ["Awareness", "Lead Gen", "Retargeting"]
META_AUD = ["Lookalike 1% - Signups", "Marketers - Interest Stack", "Site Visitors 30D", "Pricing Page Abandon"]
BLOG_SLUGS = ["/blog/multi-touch-attribution-guide", "/blog/marketing-roi-benchmarks-2026",
              "/resources/buyer-journey-playbook", "/case-studies/saas-attribution-win",
              "/blog/first-touch-vs-last-touch", "/resources/marketing-ops-maturity-model"]
REFERRAL_PARTNERS = ["Partner - G2 Crowd", "Partner - Zapier Marketplace", "Partner - Segment Connections",
                     "Customer Referral Program", "Partner - HubSpot App Marketplace"]
EMAIL_FLOWS = ["Nurture | Demo Follow-up | Email 2", "Nurture | Demo Follow-up | Email 3",
               "Lifecycle | Trial Expiry Reminder", "Lifecycle | Onboarding Day 3",
               "Newsletter | Product Update - Sept", "Re-engagement | Cold Lead Win-back",
               "Webinar Follow-up | On-demand Recording"]
WEBINAR_TOPICS = ["Attribution Masterclass", "Customer Story - Series B SaaS",
                  "Building a Marketing Data Stack", "Q3 Product Roadmap AMA"]


def google_campaign(): return f"Google Ads | Search | {random.choice(GOOGLE_THEMES)} | {random.choice(GOOGLE_MATCH)} - IN"
def google_display_retarget(): return "Google Ads | Display | Retargeting - Pricing Page Visitors"
def linkedin_campaign(): return f"LinkedIn | Sponsored Content | {random.choice(LINKEDIN_AUD)}"
def meta_campaign(): return f"Meta | {random.choice(META_OBJ)} | {random.choice(META_AUD)}"
def blog_campaign(): return random.choice(BLOG_SLUGS)
def referral_campaign(): return random.choice(REFERRAL_PARTNERS)
def email_campaign(): return random.choice(EMAIL_FLOWS)
def webinar_campaign(): return f"Webinar | {random.choice(WEBINAR_TOPICS)}"


# Which actions are plausible for each (channel, funnel stage), so a channel never gets an impossible action.
CHANNEL_STAGE_ACTIONS = {
    "Google Ads":        {0: ["Ad Impression"], 1: ["Ad Click", "Website Visit"],
                          2: ["Pricing Page View", "Product Page View"], 3: ["Demo Request", "Trial Start"]},
    "LinkedIn Ads":      {0: ["Social Impression"], 1: ["Ad Click"],
                          2: ["Case Study Download", "Product Page View"], 3: ["Demo Request"]},
    "Meta Ads":          {0: ["Social Impression", "Ad Impression"], 1: ["Ad Click"],
                          2: ["Product Page View"], 3: ["Demo Request"]},
    "Organic Search":    {0: ["Content View"], 1: ["Website Visit"],
                          2: ["Product Page View", "Pricing Page View"], 3: ["Demo Request", "Trial Start"]},
    "Content Marketing": {0: ["Content View"], 1: ["Blog Read", "Video View"],
                          2: ["Case Study Download"], 3: ["Demo Request"]},
    "Referral":          {0: ["Content View"], 1: ["Website Visit"],
                          2: ["Case Study Download"], 3: ["Demo Request"]},
    "Email":             {0: ["Email Open"], 1: ["Email Open"],
                          2: ["Webinar Registration", "Case Study Download"], 3: ["Demo Request", "Trial Start"]},
    "Retargeting":       {0: ["Ad Impression"], 1: ["Ad Click"],
                          2: ["Pricing Page View"], 3: ["Demo Request", "Trial Start"]},
    "Webinar":           {0: ["Social Impression"], 1: ["Video View"],
                          2: ["Webinar Registration"], 3: ["Demo Request", "Trial Start"]},
    "Direct":            {0: ["Website Visit"], 1: ["Website Visit"],
                          2: ["Pricing Page View", "Product Page View"], 3: ["Demo Request", "Trial Start"]},
}

# stage -> (channel, source / medium, campaign generator, weight)
STAGE_CHANNELS = {
    0: [("Google Ads", "google / cpc", google_campaign, 0.26),
        ("LinkedIn Ads", "linkedin / paid-social", linkedin_campaign, 0.20),
        ("Meta Ads", "facebook / paid-social", meta_campaign, 0.16),
        ("Organic Search", "google / organic", lambda: "(not set)", 0.16),
        ("Content Marketing", "google / organic", blog_campaign, 0.12),
        ("Referral", "referral / referral", referral_campaign, 0.10)],
    1: [("Google Ads", "google / cpc", google_campaign, 0.20),
        ("LinkedIn Ads", "linkedin / paid-social", linkedin_campaign, 0.16),
        ("Organic Search", "google / organic", lambda: "(not set)", 0.16),
        ("Content Marketing", "google / organic", blog_campaign, 0.18),
        ("Meta Ads", "facebook / paid-social", meta_campaign, 0.10),
        ("Retargeting", "google / display", google_display_retarget, 0.12),
        ("Referral", "referral / referral", referral_campaign, 0.08)],
    2: [("Content Marketing", "google / organic", blog_campaign, 0.20),
        ("Organic Search", "google / organic", lambda: "(not set)", 0.15),
        ("Google Ads", "google / cpc", google_campaign, 0.13),
        ("Retargeting", "google / display", google_display_retarget, 0.16),
        ("LinkedIn Ads", "linkedin / paid-social", linkedin_campaign, 0.10),
        ("Webinar", "webinar / event", webinar_campaign, 0.14),
        ("Email", "email / email", email_campaign, 0.12)],
    3: [("Email", "email / email", email_campaign, 0.40),
        ("Retargeting", "google / display", google_display_retarget, 0.18),
        ("Direct", "(direct) / (none)", lambda: "(not set)", 0.16),
        ("Webinar", "webinar / event", webinar_campaign, 0.12),
        ("Google Ads", "google / cpc", google_campaign, 0.09),
        ("Organic Search", "google / organic", lambda: "(not set)", 0.05)],
}


def weighted_choice(options):
    total = sum(o[-1] for o in options)
    r = random.uniform(0, total)
    upto = 0
    for o in options:
        upto += o[-1]
        if upto >= r:
            return o
    return options[-1]


# Hidden journey archetypes: (name, weight, touchpoint count, probability of converting)
ARCHETYPES = [
    ("Fast Converter", 0.10, lambda: random.choice([1, 2]), 0.35),
    ("Considered Buyer", 0.20, lambda: random.randint(3, 5), 0.45),
    ("Long Journey", 0.10, lambda: random.randint(6, 8), 0.35),
    ("Lost Journey", 0.60, lambda: random.randint(1, 6), 0.03),
]
ARCH_LOOKUP = {a[0]: a for a in ARCHETYPES}


def pick_archetype():
    r, upto = random.uniform(0, 1), 0
    for name, w, _, _ in ARCHETYPES:
        upto += w
        if upto >= r:
            return name
    return ARCHETYPES[-1][0]


REVENUE_RANGE = (18000, 220000)  # INR per closed deal
TODAY = dt.date(2026, 9, 1)
START = TODAY - dt.timedelta(days=270)
WINDOW = (TODAY - START).days

rows, summary = [], []
for j in range(1, N_JOURNEYS + 1):
    cust_id, journey_id = f"CUST-{100000 + j}", f"JRN-2026-{j:05d}"
    arch = pick_archetype()
    _, _, n_fn, conv_prob = ARCH_LOOKUP[arch]
    n = n_fn()
    converts = random.random() < conv_prob

    start = START + dt.timedelta(days=random.randint(0, WINDOW - 30))
    now = dt.datetime.combine(start, dt.time(random.randint(7, 21), random.choice([0, 15, 30, 45])))

    for i in range(n):
        is_last = i == n - 1
        if is_last and converts:
            stage = 3
        else:
            noisy = (i / max(n - 1, 1)) * 2.6 + random.gauss(0, 0.6)
            stage = max(0, min(3, round(noisy)))
            if stage == 3:
                stage = 2            # only the purchase row may be the Conversion stage

        channel, source_medium, campaign_fn, _w = weighted_choice(STAGE_CHANNELS[stage])
        campaign = campaign_fn()
        is_purchase = is_last and converts
        if is_purchase:
            action, touch_type = "Purchase", "Conversion"
        else:
            action = random.choice(CHANNEL_STAGE_ACTIONS[channel][stage])
            touch_type = STAGE_NAMES[stage]
        revenue = random.randint(*REVENUE_RANGE) if is_purchase else 0

        rows.append({
            "Customer ID": cust_id, "Journey ID": journey_id, "Touchpoint": i + 1,
            "Date": now.strftime("%Y-%m-%d"), "Channel": channel, "Source / Medium": source_medium,
            "Campaign": campaign, "Action": action, "Touchpoint Type": touch_type,
            "Intent Score": INTENT_SCORE[action], "Conversion": "Yes" if is_purchase else "No",
            "Revenue": revenue,
        })
        now += dt.timedelta(days=random.randint(1, 9), hours=random.randint(-3, 5))

    summary.append({"Journey ID": journey_id, "Customer ID": cust_id,
                    "Archetype (ground truth, QA only)": arch, "Touchpoints": n,
                    "Converted": "Yes" if converts else "No"})

df, qa = pd.DataFrame(rows), pd.DataFrame(summary)
out = os.path.join(os.path.dirname(__file__), "..", "data")
os.makedirs(out, exist_ok=True)
df.to_csv(os.path.join(out, "touchpoints.csv"), index=False)
with pd.ExcelWriter(os.path.join(out, "marketing_touchpoint_data.xlsx"), engine="openpyxl") as w:
    df.to_excel(w, sheet_name="Touchpoint_Level_Data", index=False)
    qa.to_excel(w, sheet_name="Journey_Summary_QA", index=False)

print(f"Rows: {len(df):,} | Journeys: {df['Journey ID'].nunique():,} | "
      f"Conversion rate: {(qa['Converted'] == 'Yes').mean():.1%}")
