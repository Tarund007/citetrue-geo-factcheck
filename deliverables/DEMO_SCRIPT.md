# 30-Second Screen Recording Script & Storyboard

**Objective:** A punchy, 30-second screen recording demonstrating CiteTrue GEO validating a document and catching outdated/hallucinated facts.
**Screen Tool:** Windows Game Bar (`Win + G`) or OBS Studio.

---

### Timing & Shot List

| Timestamp | Screen Action | Voiceover / Text Cue |
| :--- | :--- | :--- |
| **0:00 - 0:05** | Browser open on Streamlit web app (`app.py`). Show the header: "CiteTrue GEO — Automated Fact-Checking Layer" and sidebar with API status. | *"This is CiteTrue GEO—the truth layer built for Cog Culture to verify factual claims in AI search and marketing collaterals."* |
| **0:05 - 0:10** | Click on the **"📄 Load Assessment Trap Document"** button (or drag-and-drop `fixtures/trap_document.pdf`). Click **"Run Truth-Check Audit"**. | *"We load a test collateral containing a mix of true statements, outdated statistics, and fabricated figures."* |
| **0:10 - 0:18** | Expand the pipeline progress status showing: `Extracting claims` -> `Searching live web` -> `Verifying accuracy`. Progress bar fills up. | *"In seconds, CiteTrue extracts quantitative claims and cross-references them in real time against the live web."* |
| **0:18 - 0:26** | Audit Executive Summary appears: 8 Total Claims, 3 Verified, 3 Inaccurate, 2 False. Scroll down through the cards: highlight Swiggy IPO (`Inaccurate` -> corrected to Nov 2024) and Apollo Hospitals (`False` -> corrected from 120k to ~10k beds). | *"It flags the Swiggy IPO as outdated, catches the fabricated Apollo Hospital bed count, and provides the real-world facts with live source URLs."* |
| **0:26 - 0:30** | Click the **"📥 Export Fact-Check Audit Report (CSV)"** button. File downloads immediately. | *"Delivering exportable, audit-ready reports that transform standard SEO into an enterprise brand governance retainer."* |

---

### Tips for Recording
1. Set browser window to 1080p (1920x1080) for crisp typography.
2. Ensure dark/light mode contrast looks sharp.
3. Keep mouse movements smooth and intentional.
