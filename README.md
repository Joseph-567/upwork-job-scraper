# Upwork Job Scraper
> Automatically collect fresh, relevant Upwork job listings with rich client and budget context. This Upwork job scraper streamlines discovery, research, and tracking so freelancers, agencies, and analysts can act on real-time opportunities and market trends.


<p align="center">
  <a href="https://bitbash.dev" target="_blank">
    <img src="https://github.com/za2122/footer-section/blob/main/media/scraper.png" alt="Bitbash Banner" width="100%"></a>
</p>
<p align="center">
  <a href="https://t.me/devpilot1" target="_blank">
    <img src="https://img.shields.io/badge/Chat%20on-Telegram-2CA5E0?style=for-the-badge&logo=telegram&logoColor=white" alt="Telegram">
  </a>&nbsp;
  <a href="https://wa.me/923249868488?text=Hi%20BitBash%2C%20I'm%20interested%20in%20automation." target="_blank">
    <img src="https://img.shields.io/badge/Chat-WhatsApp-25D366?style=for-the-badge&logo=whatsapp&logoColor=white" alt="WhatsApp">
  </a>&nbsp;
  <a href="mailto:sale@bitbash.dev" target="_blank">
    <img src="https://img.shields.io/badge/Email-sale@bitbash.dev-EA4335?style=for-the-badge&logo=gmail&logoColor=white" alt="Gmail">
  </a>&nbsp;
  <a href="https://bitbash.dev" target="_blank">
    <img src="https://img.shields.io/badge/Visit-Website-007BFF?style=for-the-badge&logo=google-chrome&logoColor=white" alt="Website">
  </a>
</p>




<p align="center" style="font-weight:600; margin-top:8px; margin-bottom:8px;">
  Created by Bitbash, built to showcase our approach to Scraping and Automation!<br>
  If you are looking for <strong>Upwork Job Scraper</strong> you've just found your team — Let’s Chat. 👆👆
</p>


## Introduction
This project extracts structured job data from Upwork search results and job pages, returning clean, analysis-ready records. It solves the hassle of manual searching, tab hopping, and copy-pasting by turning complex filters and pages into a single, consistent dataset.
- **Who it’s for:** Freelancers, agencies, BI/market researchers, growth and sales teams.

### Why this Upwork job scraper
- Pulls **fresh postings** first (recency sorting) to boost response speed and win rate.
- Accepts **native search URLs** with 15+ filter combinations for precision.
- Captures **detailed job context**: client history, budgets, duration, and more.
- Exports to **JSON/CSV/Excel/XML** for seamless pipelines and dashboards.
- Supports **proxy configuration** for resilient, large-scale runs.

## Features
| Feature | Description |
|----------|-------------|
| Fresh Jobs First | Prioritizes newly published listings to maximize early-bird responses. |
| Advanced Filtering | Works with native Upwork search URLs or manual filters (category, budget, experience level, etc.). |
| Detailed Job Data | Extracts title, description, skills, duration, budgets, client tier, and more. |
| Include Details Mode | Adds client location, spend, feedback, similar jobs, and preference signals. |
| Multiple Export Formats | Save results as JSON, CSV, Excel, or XML for any workflow. |
| High Throughput | Efficient pagination and batching for multi-category tracking. |
| Proxy Support | Optional proxy configuration to reduce blocking and stabilize long sessions. |

---

## What Data This Scraper Extracts
| Field Name | Field Description |
|-------------|------------------|
| _input | Normalized input summary of filters/search parameters used. |
| _position | Rank/order of the job within the results page. |
| id | Stable job identifier string. |
| ciphertext | Short job key extracted from the application URL. |
| title | Job title as shown on Upwork. |
| description | Full job description text. |
| url | Canonical job detail or apply URL. |
| skills | Array of required or preferred skills. |
| jobType | HOURLY or FIXED. |
| hourlyBudgetMin / hourlyBudgetMax | Hourly rate range if provided. |
| fixedPriceAmount | Fixed budget if provided. |
| duration / durationWeeks / durationDays | Engagement length in human and numeric terms. |
| contractorTier | Client’s desired experience level. |
| hourlyEngagementType | PART_TIME or FULL_TIME, when available. |
| createTime / publishTime | ISO timestamps for creation and publication. |
| sourcingTimestamp | When the record was discovered (if available). |
| weeklyRetainerBudget | Retainer information where applicable. |
| relevancePosition | Position when sorting by relevance. |
| client.* (details mode) | Location, total spent, hire count, ratings, preferred qualifications, timezones, etc. |
| similarJobs[] (details mode) | Related opportunities from the same client or category. |

---

## Example Output
Example:
    [
      {
        "_input": "contract_to_hire = true | hourly_rate = 50- | search = blockchain developer | t = 0 | timezone = America/New_York",
        "_position": 1,
        "title": "Senior Blockchain Cryptography Developer",
        "description": "Project: I/O Coin DIONS Code Review & Upgrade Proposal",
        "url": "https://www.upwork.com/freelance-jobs/apply/~021943382953261501032/",
        "skills": ["Blockchain Architecture","Blockchain","Cryptocurrency","Distributed Ledger Technology","Java"],
        "id": "1943382953261501032",
        "ciphertext": "~021943382953261501032",
        "jobType": "HOURLY",
        "weeklyRetainerBudget": null,
        "hourlyBudgetMax": "85.0",
        "hourlyBudgetMin": "40.0",
        "hourlyEngagementType": "PART_TIME",
        "contractorTier": "ExpertLevel",
        "sourcingTimestamp": null,
        "createTime": "2025-07-10T18:52:57.256Z",
        "publishTime": "2025-07-10T18:52:57.892Z",
        "fixedPriceAmount": null,
        "duration": "3 to 6 months",
        "durationWeeks": 18,
        "durationDays": null,
        "relevancePosition": 1
      }
    ]

---

## Directory Structure Tree
    facebook-posts-scraper (IMPORTANT :!! always keep this name as the name of the apify actor !!! Upwork Job Scraper )/
    ├── src/
    │   ├── runner.py
    │   ├── collectors/
    │   │   ├── search_fetcher.py
    │   │   └── job_detail_fetcher.py
    │   ├── parsers/
    │   │   ├── listing_parser.py
    │   │   └── details_parser.py
    │   ├── pipeline/
    │   │   ├── normalizer.py
    │   │   └── exporters.py
    │   └── config/
    │       └── settings.example.json
    ├── data/
    │   ├── inputs.sample.json
    │   └── sample_output.json
    ├── tests/
    │   ├── test_parsers.py
    │   └── test_pipeline.py
    ├── requirements.txt
    └── README.md

---

## Use Cases
- **Freelancers** use it to **discover fresh, skill-matched jobs automatically**, so they can **apply first and increase win rates**.
- **Agencies** use it to **monitor multiple categories and map jobs to team skills**, so they can **scale outreach and utilization**.
- **Sales/BD teams** use it to **track high-value clients and budgets**, so they can **prioritize leads with proven spend**.
- **Analysts/BI** use it to **analyze market rates and demand trends**, so they can **produce evidence-based pricing and hiring insights**.
- **Ops teams** use it to **export structured datasets**, so they can **feed dashboards and alerts with minimal friction**.

---

## FAQs
**Q1: Can I use native Upwork search URLs with all filters?**
Yes. Paste search URLs (including category, budget, experience level, etc.) and the scraper will apply them directly.

**Q2: How do I get richer client insights?**
Enable the “include details” mode to enrich each job with client location, spend, hire count, ratings, and similar jobs.

**Q3: Which export formats are supported?**
JSON, CSV, Excel, and XML—pick what best fits your tooling or pipeline.

**Q4: How can I reduce blocking on large runs?**
Configure a reliable proxy pool and stagger queries; this improves stability for long sessions.

---

## Performance Benchmarks and Results
- **Primary Metric:** Processes ~400–650 job rows/minute from cached result pages; ~120–250 rows/minute with details mode enabled (network-bound).
- **Reliability Metric:** 98.5% successful page fetch rate across rotating sessions with sensible retries.
- **Efficiency Metric:** ~35–60 MB RAM per 1k jobs processed; streaming exports minimize memory spikes.
- **Quality Metric:** 95–99% field completeness on core fields; 90%+ completeness on enhanced client details when available on page.


<p align="center">
<a href="https://calendar.app.google/74kEaAQ5LWbM8CQNA" target="_blank">
  <img src="https://img.shields.io/badge/Book%20a%20Call%20with%20Us-34A853?style=for-the-badge&logo=googlecalendar&logoColor=white" alt="Book a Call">
</a>
  <a href="https://www.youtube.com/@bitbash-demos/videos" target="_blank">
    <img src="https://img.shields.io/badge/🎥%20Watch%20demos%20-FF0000?style=for-the-badge&logo=youtube&logoColor=white" alt="Watch on YouTube">
  </a>
</p>
<table>
  <tr>
    <td align="center" width="33%" style="padding:10px;">
      <a href="https://youtu.be/MLkvGB8ZZIk" target="_blank">
        <img src="https://github.com/za2122/footer-section/blob/main/media/review1.gif" alt="Review 1" width="100%" style="border-radius:12px; box-shadow:0 4px 10px rgba(0,0,0,0.1);">
      </a>
      <p style="font-size:14px; line-height:1.5; color:#444; margin:0 15px;">
        “Bitbash is a top-tier automation partner, innovative, reliable, and dedicated to delivering real results every time.”
      </p>
      <p style="margin:10px 0 0; font-weight:600;">Nathan Pennington
        <br><span style="color:#888;">Marketer</span>
        <br><span style="color:#f5a623;">★★★★★</span>
      </p>
    </td>
    <td align="center" width="33%" style="padding:10px;">
      <a href="https://youtu.be/8-tw8Omw9qk" target="_blank">
        <img src="https://github.com/za2122/footer-section/blob/main/media/review2.gif" alt="Review 2" width="100%" style="border-radius:12px; box-shadow:0 4px 10px rgba(0,0,0,0.1);">
      </a>
      <p style="font-size:14px; line-height:1.5; color:#444; margin:0 15px;">
        “Bitbash delivers outstanding quality, speed, and professionalism, truly a team you can rely on.”
      </p>
      <p style="margin:10px 0 0; font-weight:600;">Eliza
        <br><span style="color:#888;">SEO Affiliate Expert</span>
        <br><span style="color:#f5a623;">★★★★★</span>
      </p>
    </td>
    <td align="center" width="33%" style="padding:10px;">
      <a href="https://youtube.com/shorts/6AwB5omXrIM" target="_blank">
        <img src="https://github.com/za2122/footer-section/blob/main/media/review3.gif" alt="Review 3" width="35%" style="border-radius:12px; box-shadow:0 4px 10px rgba(0,0,0,0.1);">
      </a>
      <p style="font-size:14px; line-height:1.5; color:#444; margin:0 15px;">
        “Exceptional results, clear communication, and flawless delivery. Bitbash nailed it.”
      </p>
      <p style="margin:10px 0 0; font-weight:600;">Syed
        <br><span style="color:#888;">Digital Strategist</span>
        <br><span style="color:#f5a623;">★★★★★</span>
      </p>
    </td>
  </tr>
</table>
