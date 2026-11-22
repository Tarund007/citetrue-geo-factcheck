# CiteTrue GEO: The Generative Truth Layer & Automated Fact-Checking Platform

> **Candidate Assignment:** Management Trainee — Product Management at **Cog Culture**  
> **Author:** Tarun Dinkar  
> **Submission Date:** November 2026  
> **Live App:** `[Insert Deployed Streamlit URL]`  
> **GitHub Repo:** https://github.com/Tarund007/citetrue-geo-factcheck  

---

## 1. Product Context & Thesis

**Why this project is not generic "AI-slop":**
Traditional SEO and ORM tools track rankings and sentiment across web links and social threads. In the 2026 search landscape, user discovery is driven by synthesized zero-click AI engines: **ChatGPT Search, Google AI Overviews, Perplexity, Copilot, and Gemini**.

Emerging Generative Engine Optimization (GEO) platforms (such as *Profound, Peec AI, AthenaHQ, Scrunch, Semrush AI Visibility*) focus almost exclusively on **mention volume**—measuring *how often* a brand is cited. 

**The Unaddressed Gap:** None of these tools systematically audit whether the answers synthesized by LLMs state **true or hallucinated facts** about a brand. If an AI engine invents an incorrect funding round, an outdated hospital bed count, or a fabricated CEO name, the brand suffers severe reputational, financial, or regulatory damage.

**CiteTrue GEO** is Cog Culture's proprietary **"Truth Layer"**. It audits marketing collaterals, press releases, and LLM answers by:
1. Parsing documents to isolate testable numerical metrics, dates, and quantitative claims.
2. Querying live real-time web search (via Tavily) to establish empirical ground truth.
3. Classifying claims into three strict verdicts: **Verified**, **Inaccurate** (outdated stats), or **False** (unsupported or fabricated), accompanied by real-world corrected facts and source URLs.

---

## 2. Deliverables Summary

1. **Part 1 — Strategy & Presentation Deck (`deliverables/CogCulture_GEO_CiteTrue.pptx`):**
   - 14-slide executive presentation generated directly via `python-pptx`.
   - Built in an editorial black-and-white theme with clean crimson highlights.
   - Covers: 2026 AI Search State, Cog Agency Context (PepsiCo, DLF, Apollo, Cashfree), JTBD, Competitor Pricing Scan, Positioning Matrix, Feature Spec, Wireframes, Guardrails, Success Metrics, 3-Month MVP Roadmap, 12-Month Monetization Strategy, and Risk Matrix.
2. **Part 2 — Automated Fact-Checking Application (`app.py`):**
   - Built on Streamlit for instant zero-friction deployment to Streamlit Community Cloud.
   - Fully interactive UI with PDF uploader, assessment trap document loader, progress pipeline, and custom-styled audit cards.
   - Exportable CSV report.
3. **Assessment Trap Document & Benchmark (`fixtures/trap_document.pdf` & `fixtures/expected_flags.md`):**
   - Custom test document with deliberate truthful, outdated, and fabricated claims to prove accuracy under test.
4. **Demo Video Walkthrough Script (`deliverables/DEMO_SCRIPT.md`):**
   - Precise 30-second recording storyboard for screen recording via Windows Game Bar (`Win + G`).
5. **Submission Pack (`deliverables/SUBMISSION.md`):**
   - Ready-to-send email copy for recruiter submission.

---

## 3. Architecture & Data Flow

```
+--------------------------------------------------------------------+
| 1. Ingestion: PDF Upload or Synthetic LLM Brand Answer Text        |
+--------------------------------------------------------------------+
                                  |
                                  v
+--------------------------------------------------------------------+
| 2. Extraction: pdfplumber text parsing + Gemini 3.5 Flash          |
|    - Isolates percentages, currencies, dates, headcounts, versions |
|    - Heuristic regex fallback for zero-downtime execution          |
+--------------------------------------------------------------------+
                                  |
                                  v
+--------------------------------------------------------------------+
| 3. Live Search: Tavily Search API                                  |
|    - Queries live web; retrieves authoritative snippets & URLs     |
+--------------------------------------------------------------------+
                                  |
                                  v
+--------------------------------------------------------------------+
| 4. Judgment Engine: Temperature 0.0 Gemini Factual Classifier      |
|    - Verified: Matches live web consensus                          |
|    - Inaccurate: Outdated figure -> supplies current real fact     |
|    - False: Contradicted/Fabricated -> supplies debunking evidence |
+--------------------------------------------------------------------+
                                  |
                                  v
+--------------------------------------------------------------------+
| 5. Presentation Layer: Streamlit UI + CSV Audit Report Export      |
+--------------------------------------------------------------------+
```

---

## 4. How Recruiters Can Test

### Option A: Testing on Live Deployed URL
1. Navigate to the deployed Streamlit app URL: `[Deployed Link]`.
2. Ensure API keys are active (or enter your own Gemini & Tavily keys in the left sidebar).
3. Click the **"📄 Load Assessment Trap Document"** button.
4. Click **"Run Truth-Check Audit"**.
5. Observe the system identify outdated figures (e.g., Swiggy IPO status, Zomato Blinkit acquisition cost) and fabrications (e.g., Apollo Hospitals 120,000 beds, Satya Nadella as PepsiCo CEO).
6. Click **"📥 Export Fact-Check Audit Report (CSV)"** to test data export.

### Option B: Running Locally

1. **Clone the repository:**
   ```bash
   git clone <repo-url>
   cd "management trainee"
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure API Keys:**
   Create a `.streamlit/secrets.toml` file (or set environment variables):
   ```toml
   GEMINI_API_KEY = "your-gemini-api-key"
   TAVILY_API_KEY = "your-tavily-api-key"
   ```

4. **Launch the web application:**
   ```bash
   streamlit run app.py
   ```

---

## 5. Trap Document Test Cases & Benchmark

| Claim in Trap Document | Claim Type | Expected Verdict | Verified Ground Truth |
| :--- | :--- | :--- | :--- |
| **OpenAI founded in Dec 2015 in SF** | Date / Org | `Verified` | Founded Dec 2015 in San Francisco by Altman, Musk, Brockman, Sutskever. |
| **Swiggy planning IPO in late 2026** | Date / Milestone | `Inaccurate` | Swiggy completed its IPO in November 2024 and is already listed on NSE/BSE. |
| **Zomato acquired Blinkit for $1.8B** | Financial / Stat | `Inaccurate` | Deal was closed for approximately $568M (~Rs 4,447 crore), not $1.8B. |
| **iPhone 16 launched Sept 2024 with A18** | Tech / Date | `Verified` | Launched September 9, 2024 powered by the 3nm A18 family chips. |
| **Apollo Hospitals operates 120,000 beds in 45 countries** | Headcount / Stat | `False` | Operates ~10,000 to 11,000 beds across ~70 hospitals, predominantly in India. |
| **DLF Cyber City located in Gurugram, Haryana** | Geography / Tech | `Verified` | Confirmed major commercial cyber hub in Gurugram, Haryana. |
| **Cashfree Payments founded in 2021** | Date | `Inaccurate` | Founded in 2015 by Akash Gehani and Reeju Datta, not 2021. |
| **Satya Nadella is CEO of PepsiCo since 2018** | Leadership | `False` | Ramon Laguarta is CEO of PepsiCo. Satya Nadella is CEO of Microsoft. |

---

## 6. Project Layout

```
.
├── .streamlit/
│   └── secrets.toml.example     # Template for API keys
├── deliverables/
│   ├── CogCulture_GEO_CiteTrue.pptx # 14-slide executive presentation deck
│   ├── DEMO_SCRIPT.md          # 30-second recording storyboard
│   └── SUBMISSION.md           # Submission email pack
├── fixtures/
│   ├── expected_flags.md       # Ground-truth documentation of trap claims
│   ├── generate_trap_pdf.py    # ReportLab generator for test PDF
│   └── trap_document.pdf       # Pre-built benchmark test PDF
├── src/
│   ├── extract.py              # pdfplumber parsing + LLM/regex claim extractor
│   ├── prompts.py              # Strict system prompts for extraction & judgment
│   ├── search.py               # Tavily search wrapper
│   └── verify.py               # Multi-source judgment & correction engine
├── app.py                      # Main Streamlit web application
├── build_deck.py               # Automated PPTX presentation generator
├── requirements.txt            # Pinned dependencies
├── .gitignore                  # Git hygiene
└── README.md                   # System documentation
```

---

## 7. Business & Monetization Architecture for Cog Culture

- **Tier 1 (One-off GEO Brand Audit — ₹1.5L / $1,800):** Comprehensive baseline audit across 5 LLM engines and brand PDFs to identify factual inaccuracies.
- **Tier 2 (Continuous GEO Governance Retainer — ₹75K / $900 per month):** Bi-weekly automated prompt audits, PR correction tickets, and citation growth reports.
- **Tier 3 (Enterprise Multi-Brand Portal — ₹2.5L / $3,000 per month):** Self-serve dashboard access for client comms teams with automated Wikipedia, schema markup, and press seeding recommendations.

*Built with precision for Cog Culture Product Management.*

## 8. Screenshots of the webapp


