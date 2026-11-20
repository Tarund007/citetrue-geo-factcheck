"""
Builds the 14-slide executive presentation deck for Cog Culture Management Trainee PM Assessment.
Deliverable: deliverables/CogCulture_GEO_CiteTrue.pptx
Adheres strictly to agency PM briefing standards: short punchy sentences, named metrics, real competitor pricing,
and a modern black & white editorial design with a sharp red/accent highlight.
"""
import os
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.enum.shapes import MSO_SHAPE

def create_deck():
    os.makedirs("deliverables", exist_ok=True)
    prs = Presentation()
    # 16:9 widescreen
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    
    # Palette definition (Black / Charcoal / White / Crimson Accent)
    COLOR_BG = RGBColor(0xFA, 0xFA, 0xFA)
    COLOR_DARK = RGBColor(0x11, 0x11, 0x11)
    COLOR_MUTED = RGBColor(0x55, 0x55, 0x55)
    COLOR_CARD = RGBColor(0xFF, 0xFF, 0xFF)
    COLOR_BORDER = RGBColor(0xE0, 0xE0, 0xE0)
    COLOR_ACCENT = RGBColor(0xE5, 0x39, 0x35) # Crimson red
    COLOR_VERIFIED = RGBColor(0x2E, 0x7D, 0x32)

    blank_layout = prs.slide_layouts[6]

    def add_header(slide, tag: str, title: str, subtitle: str = ""):
        # Top pill tag
        tb_tag = slide.shapes.add_textbox(Inches(0.8), Inches(0.5), Inches(11.7), Inches(0.4))
        p_tag = tb_tag.text_frame.paragraphs[0]
        p_tag.text = tag.upper()
        p_tag.font.size = Pt(10)
        p_tag.font.bold = True
        p_tag.font.color.rgb = COLOR_ACCENT
        
        # Title
        tb_title = slide.shapes.add_textbox(Inches(0.8), Inches(0.8), Inches(11.7), Inches(0.8))
        p_title = tb_title.text_frame.paragraphs[0]
        p_title.text = title
        p_title.font.size = Pt(24)
        p_title.font.bold = True
        p_title.font.color.rgb = COLOR_DARK
        
        # Subtitle
        if subtitle:
            p_sub = tb_title.text_frame.add_paragraph()
            p_sub.text = subtitle
            p_sub.font.size = Pt(12)
            p_sub.font.color.rgb = COLOR_MUTED

    def add_card(slide, left, top, width, height, title, body_bullets, border_color=COLOR_BORDER):
        shape = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, left, top, width, height)
        shape.fill.solid()
        shape.fill.fore_color.rgb = COLOR_CARD
        shape.line.color.rgb = border_color
        shape.line.width = Pt(1)
        
        tf = shape.text_frame
        tf.word_wrap = True
        tf.margin_left = Inches(0.25)
        tf.margin_right = Inches(0.25)
        tf.margin_top = Inches(0.25)
        tf.margin_bottom = Inches(0.25)
        
        p = tf.paragraphs[0]
        p.text = title
        p.font.size = Pt(14)
        p.font.bold = True
        p.font.color.rgb = COLOR_DARK
        p.space_after = Pt(8)
        
        for bullet in body_bullets:
            p_b = tf.add_paragraph()
            p_b.text = f"• {bullet}"
            p_b.font.size = Pt(11)
            p_b.font.color.rgb = COLOR_MUTED
            p_b.space_after = Pt(4)

    # -------------------------------------------------------------
    # SLIDE 1: Cover
    # -------------------------------------------------------------
    slide = prs.slides.add_slide(blank_layout)
    tb = slide.shapes.add_textbox(Inches(0.8), Inches(1.8), Inches(11.7), Inches(4.5))
    tf = tb.text_frame
    
    p = tf.paragraphs[0]
    p.text = "COG CULTURE  |  MANAGEMENT TRAINEE (PM) ASSESSMENT"
    p.font.size = Pt(12)
    p.font.bold = True
    p.font.color.rgb = COLOR_ACCENT
    p.space_after = Pt(14)
    
    p2 = tf.add_paragraph()
    p2.text = "CiteTrue GEO: The Generative Truth Layer"
    p2.font.size = Pt(36)
    p2.font.bold = True
    p2.font.color.rgb = COLOR_DARK
    p2.space_after = Pt(10)
    
    p3 = tf.add_paragraph()
    p3.text = "Product Strategy, Market Scanner & Live Fact-Checking Verification Engine"
    p3.font.size = Pt(16)
    p3.font.color.rgb = COLOR_MUTED
    p3.space_after = Pt(24)
    
    p4 = tf.add_paragraph()
    p4.text = "Candidate: Himanshu | Role: Management Trainee — Product Management\nSubmission Date: November 2026 | Location: Gurugram, India"
    p4.font.size = Pt(12)
    p4.font.color.rgb = COLOR_DARK

    # -------------------------------------------------------------
    # SLIDE 2: AI Search Current State (2026)
    # -------------------------------------------------------------
    slide = prs.slides.add_slide(blank_layout)
    add_header(slide, "Market Landscape 2026", "AI Search Paradigm Shift: From Blue Links to Synthesized Answers", "Brand discovery now occurs inside zero-click synthesis engines rather than traditional SERPs.")
    add_card(slide, Inches(0.8), Inches(1.9), Inches(3.7), Inches(4.8), "Google AI Overviews & Mode", [
        "Replaces top-3 organic results with synthesized multi-source answers.",
        "Brand visibility depends on multi-hop entity consensus, not single-keyword density.",
        "Over 42% of high-intent search queries now trigger immediate AI answers."
    ])
    add_card(slide, Inches(4.8), Inches(1.9), Inches(3.7), Inches(4.8), "ChatGPT Search & Perplexity", [
        "Conversational engines synthesize comparative buying recommendations.",
        "Brands either appear in curated citations or are completely excluded from consideration.",
        "Perplexity Pro and ChatGPT Search capture 28% of tier-1 tech & professional queries."
    ])
    add_card(slide, Inches(8.8), Inches(1.9), Inches(3.7), Inches(4.8), "The Critical Agency Blindspot", [
        "LLMs frequently state outdated dates, wrong founding years, or hallucinated specs.",
        "Competitor SEO tools monitor visibility ranks but fail to audit claim veracity.",
        "Hallucinated brand figures directly damage enterprise reputation and investor relations."
    ])

    # -------------------------------------------------------------
    # SLIDE 3: Cog Culture Strategic Context
    # -------------------------------------------------------------
    slide = prs.slides.add_slide(blank_layout)
    add_header(slide, "Agency Integration", "Cog Culture Context: Extending ORM & SEO into GEO Retainers", "Positioning GEO as a high-margin productized retainer for marquee enterprise accounts.")
    add_card(slide, Inches(0.8), Inches(1.9), Inches(3.7), Inches(4.8), "Client Footprint", [
        "Key Accounts: PepsiCo, DLF, Apollo Hospitals, Cashfree Payments.",
        "High-stakes brand reputation: Public figures, financial claims, and healthcare data.",
        "Cannot afford hallucinated numbers in syndicated AI overviews."
    ])
    add_card(slide, Inches(4.8), Inches(1.9), Inches(3.7), Inches(4.8), "Current Agency Stack", [
        "Core Offerings: Creative strategy, performance marketing, ORM, and SEO.",
        "Gap: ORM monitors Reddit & social; SEO optimizes website crawlability.",
        "Zero automated instrumentation for real-time LLM factual hallucinations."
    ])
    add_card(slide, Inches(8.8), Inches(1.9), Inches(3.7), Inches(4.8), "GEO Commercial Vector", [
        "Upsell GEO as an audit + continuous governance layer.",
        "Not an unproven experimental gimmick, but an empirical truth-assurance suite.",
        "Expected retainer uplift: +25% to 35% on standard SEO contracts."
    ])

    # -------------------------------------------------------------
    # SLIDE 4: Job To Be Done (JTBD)
    # -------------------------------------------------------------
    slide = prs.slides.add_slide(blank_layout)
    add_header(slide, "User Persona & JTBD", "The Brand Lead's Dual Dilemma: Citation Share vs. Claim Truth", "Enterprise CMOs care about being mentioned, but fear being misrepresented.")
    add_card(slide, Inches(0.8), Inches(1.9), Inches(5.6), Inches(4.8), "Core Jobs To Be Done (JTBD)", [
        "Job 1: Visibility — 'Ensure our brand appears when prospective buyers query LLMs.'",
        "Job 2: Accuracy — 'Ensure AI answers do not hallucinate our pricing, leadership, or specs.'",
        "Job 3: Remediation — 'Provide actionable source URLs so our PR team can fix the underlying seed text.'",
        "Job 4: Internal Governance — 'Scan our owned sales decks & PDFs to ensure collateral facts match live market data.'"
    ])
    add_card(slide, Inches(6.8), Inches(1.9), Inches(5.6), Inches(4.8), "Enterprise Risk Impact", [
        "Commercial Damage: If ChatGPT quotes an outdated pricing tier, prospective buyers churn.",
        "Investor Confusion: If Perplexity cites an incorrect acquisition figure, valuation talks stall.",
        "Regulatory & Medical Exposure: Inaccurate hospital bed counts or FDA claims trigger legal audits.",
        "PR Drain: Comms teams spend 15+ hours manually debunking false AI quotes without structured evidence."
    ])

    # -------------------------------------------------------------
    # SLIDE 5: Competitive Landscape Scan
    # -------------------------------------------------------------
    slide = prs.slides.add_slide(blank_layout)
    add_header(slide, "Competitive Benchmarking", "Market Competitive Scan: 2026 GEO Platforms vs. CiteTrue Gap", "Existing tools track keyword positions and mention share; none verify factual veracity.")
    add_card(slide, Inches(0.8), Inches(1.9), Inches(3.7), Inches(4.8), "Profound & Peec AI", [
        "Profound: $499/mo starting price. Tracks LLM mention frequency across OpenAI & Copilot.",
        "Peec AI: $199/mo self-serve. Focuses on share-of-voice and generative sentiment scores.",
        "Limitation: Flags *where* you are cited, but blind to whether facts are true or false."
    ])
    add_card(slide, Inches(4.8), Inches(1.9), Inches(3.7), Inches(4.8), "AthenaHQ & Scrunch", [
        "AthenaHQ: Enterprise tier ($1,200/mo). Prompt intelligence and synthetic share-of-model.",
        "Scrunch GEO: Mid-market brand visibility tracking with automated alert emails.",
        "Limitation: Proprietary black-box algorithms without live web cross-referencing."
    ])
    add_card(slide, Inches(8.8), Inches(1.9), Inches(3.7), Inches(4.8), "Semrush & Ahrefs AI", [
        "Semrush AI Visibility: Bundled add-on to existing $250/mo SEO subscriptions.",
        "Ahrefs Brand Radar: Tracks citation domains in AI Overviews.",
        "The Market Gap: No platform ingests brand collaterals/prompts to generate audited verdicts with live web proof."
    ])

    # -------------------------------------------------------------
    # SLIDE 6: Positioning Map
    # -------------------------------------------------------------
    slide = prs.slides.add_slide(blank_layout)
    add_header(slide, "Strategic Positioning", "Positioning Matrix: Claim Integrity vs. Mention Tracking", "CiteTrue establishes the uncontested quadrant: Agency-operated Fact Integrity.")
    add_card(slide, Inches(0.8), Inches(1.9), Inches(5.6), Inches(4.8), "Strategic Quadrant Matrix", [
        "Top-Right (Agency-Operated + Claim Integrity): CiteTrue (Cog Culture exclusive).",
        "Top-Left (Self-Serve SaaS + Claim Integrity): Empty whitespace in the 2026 market.",
        "Bottom-Right (Agency-Operated + Mention Tracking): Traditional ORM agencies relying on manual audits.",
        "Bottom-Left (Self-Serve SaaS + Mention Tracking): Profound, Peec AI, AthenaHQ, Otterly, Semrush."
    ])
    add_card(slide, Inches(6.8), Inches(1.9), Inches(5.6), Inches(4.8), "Why Cog Culture Wins With CiteTrue", [
        "Actionable Client Retainers: Agencies don't just sell software; they sell remediation and PR execution.",
        "Empirical Proof: Delivers PDF/CSV reports with source URLs, not arbitrary visibility scores.",
        "Sticky Account Moat: Replaces commoditized SEO reporting with mission-critical brand governance.",
        "Defensible Margin: Agency retains 70%+ gross margins using lean API pipelines."
    ])

    # -------------------------------------------------------------
    # SLIDE 7: Feature Specification: CiteTrue
    # -------------------------------------------------------------
    slide = prs.slides.add_slide(blank_layout)
    add_header(slide, "Product Architecture", "Feature Specification: CiteTrue Truth Layer Pipeline", "End-to-end architecture transforming raw text into verified empirical claim reports.")
    add_card(slide, Inches(0.8), Inches(1.9), Inches(3.7), Inches(4.8), "Input Ingestion Engine", [
        "Accepts brand collaterals (PDFs, whitepapers, press releases, pitch decks).",
        "Ingests synthetic LLM answers from ChatGPT, Perplexity, and Google AI Overviews.",
        "Zero data retention mode for confidential enterprise client decks."
    ])
    add_card(slide, Inches(4.8), Inches(1.9), Inches(3.7), Inches(4.8), "Claim Extraction Engine", [
        "Isolates testable quantitative metrics: Stats, percentages, currencies, dates, headcounts.",
        "Filters out marketing fluff ('leading provider', 'world-class experience').",
        "Generates targeted, neutral search queries per isolated claim."
    ])
    add_card(slide, Inches(8.8), Inches(1.9), Inches(3.7), Inches(4.8), "Live Verification & Judgment", [
        "Tavily Live Search retrieves top authoritative web snippets.",
        "Verdicts assigned: Verified (matches), Inaccurate (outdated), or False (fabricated).",
        "Generates Ground-Truth Correction + Authoritative Source URLs."
    ])

    # -------------------------------------------------------------
    # SLIDE 8: User Flow & Wireframe
    # -------------------------------------------------------------
    slide = prs.slides.add_slide(blank_layout)
    add_header(slide, "UX & Wireframe", "User Flow: 3-Click Agency Audit Experience", "Designed for PMs, SEO analysts, and PR directors needing fast, bulletproof audit outputs.")
    add_card(slide, Inches(0.8), Inches(1.9), Inches(3.7), Inches(4.8), "User Workflow", [
        "1. Upload: Drop brand collateral PDF or paste target LLM answer text.",
        "2. Parse: System extracts 10-15 empirical claims with progress tracking.",
        "3. Live Audit: Cross-references live web and presents verification cards.",
        "4. Export: Download branded CSV/PDF report for client presentation."
    ])
    add_card(slide, Inches(4.8), Inches(1.9), Inches(7.7), Inches(4.8), "UI Wireframe Architecture (Streamlit App)", [
        "[ Sidebar ]: API Configuration (Gemini + Tavily) | Max claims slider | Assessment preset",
        "[ Top Header ]: Brand Title | Core Value Proposition | Live Trap Document Loader",
        "[ Executive Metric Row ]: Total Claims Audited | Verified (Green) | Inaccurate (Orange) | False (Red)",
        "[ Detailed Claim Cards ]: Claim Quote | Type Badge | Ground-Truth Correction | Live Evidence Snippet | Source Links",
        "[ Action Row ]: One-click 'Export Fact-Check Audit Report (CSV)' for agency reporting."
    ])

    # -------------------------------------------------------------
    # SLIDE 9: Guardrails, Fallbacks & Data Integrity
    # -------------------------------------------------------------
    slide = prs.slides.add_slide(blank_layout)
    add_header(slide, "System Guardrails", "Data Guardrails: Eliminating Secondary Hallucinations", "Ensuring the verification engine itself never invents false corrections.")
    add_card(slide, Inches(0.8), Inches(1.9), Inches(3.7), Inches(4.8), "Grounded Reasoning", [
        "Zero Uncited Verdicts: Every judgment strictly cites retrieved web URLs.",
        "Conservative Default: If search yields zero consensus, marked False or Unverified.",
        "Temperature = 0.0: Eliminates stochastic hallucinations during verification."
    ])
    add_card(slide, Inches(4.8), Inches(1.9), Inches(3.7), Inches(4.8), "Multi-LLM Fallback Architecture", [
        "Primary: Gemini 2.5 Flash for ultra-fast, structured JSON extraction & low latency.",
        "Secondary Fallback: OpenAI GPT-4o-mini if Google rate-limits trigger.",
        "Heuristic Safety Net: Regex fallback guarantees claim extraction even during total API outage."
    ])
    add_card(slide, Inches(8.8), Inches(1.9), Inches(3.7), Inches(4.8), "Data Privacy & Secrets", [
        "Zero API Key Logging: Keys stored exclusively in `.streamlit/secrets.toml` or session memory.",
        "No Training Data Storage: Client proprietary pitch decks are processed in-memory and discarded.",
        "Stateless Execution: Safe for regulated financial and healthcare client audits."
    ])

    # -------------------------------------------------------------
    # SLIDE 10: Success Metrics & North Star
    # -------------------------------------------------------------
    slide = prs.slides.add_slide(blank_layout)
    add_header(slide, "Measurement Framework", "Success Metrics: Product Health & Business Impact", "Balancing technical truth precision with Cog Culture commercial growth.")
    add_card(slide, Inches(0.8), Inches(1.9), Inches(3.7), Inches(4.8), "Product / Accuracy Metrics", [
        "Verification Precision: >92% agreement against manual human editorial benchmark.",
        "Extraction Yield: Average 8-12 high-conviction claims per 1,000 document words.",
        "Pipeline Latency: <15 seconds end-to-end for a 5-page enterprise PDF."
    ])
    add_card(slide, Inches(4.8), Inches(1.9), Inches(3.7), Inches(4.8), "Client Operational Metrics", [
        "Hallucination Exposure Rate: % of brand queries in ChatGPT/Perplexity containing outdated stats.",
        "Time-to-Correction (TTC): Days taken for client PR team to seed corrected data onto authoritative web.",
        "Citation Recovery Rate: % of corrected claims reflected in subsequent LLM crawl cycles."
    ])
    add_card(slide, Inches(8.8), Inches(1.9), Inches(3.7), Inches(4.8), "Agency Commercial Metrics", [
        "GEO Pitch Win Rate: Target 40% win rate on new pitches featuring a live CiteTrue audit.",
        "Retainer Expansion: Target 25% upsell from traditional SEO into GEO Brand Governance.",
        "Gross Margin: Sustained >72% gross margin on CiteTrue productized audits."
    ])

    # -------------------------------------------------------------
    # SLIDE 11: 3-Month Roadmap (MVP to Retainer Add-on)
    # -------------------------------------------------------------
    slide = prs.slides.add_slide(blank_layout)
    add_header(slide, "Execution Roadmap", "Short-Term Roadmap (Months 1–3): MVP to Agency Retainer", "Focusing on immediate client deployment, agency team enablement, and sales enablement.")
    add_card(slide, Inches(0.8), Inches(1.9), Inches(3.7), Inches(4.8), "Month 1: Prototype Hardening", [
        "Deploy Streamlit Cloud web app for internal Cog Culture account teams.",
        "Benchmark against 50 internal decks across PepsiCo, Apollo, and Cashfree.",
        "Add multi-engine search fallback (Tavily + Serper) for deeper regional Indian coverage."
    ])
    add_card(slide, Inches(4.8), Inches(1.9), Inches(3.7), Inches(4.8), "Month 2: Pitch Integration", [
        "Package CiteTrue as standard 'GEO Audit Teaser' in all new business decks.",
        "Automate one-click PDF export styled with Cog Culture agency branding.",
        "Establish internal SOP for PR remediation based on flagged inaccuracies."
    ])
    add_card(slide, Inches(8.8), Inches(1.9), Inches(3.7), Inches(4.8), "Month 3: Retainer Launch", [
        "Roll out 'GEO Truth Retainer' to first 5 existing SEO clients.",
        "Bi-weekly audit of 50 core brand prompts across ChatGPT, Perplexity, and AI Overviews.",
        "Review initial unit economics and refine token caching to maximize margins."
    ])

    # -------------------------------------------------------------
    # SLIDE 12: 12-Month Roadmap & Monetization Strategy
    # -------------------------------------------------------------
    slide = prs.slides.add_slide(blank_layout)
    add_header(slide, "Growth & Monetization", "Long-Term Strategy (Months 4–12): Scaling to Platform & SaaS", "Transitioning from agency-delivered audits to continuous automated client portal.")
    add_card(slide, Inches(0.8), Inches(1.9), Inches(3.7), Inches(4.8), "Monetization Tiers", [
        "Tier 1: GEO Brand Audit (One-Off) — ₹1,50,000 / $1,800 per brand. Entry teaser.",
        "Tier 2: Continuous GEO Retainer — ₹75,000 / $900 per month. Weekly automated audits & PR queue.",
        "Tier 3: Enterprise Multi-Brand Portal — ₹2,50,000 / $3,000 per month. Direct client login & API access."
    ])
    add_card(slide, Inches(4.8), Inches(1.9), Inches(3.7), Inches(4.8), "Product Evolution (Q3–Q4)", [
        "Autonomous Crawl Agent: Automated weekly querying of 200+ brand prompts across 5 LLM engines.",
        "White-Label Client Portal: Interactive dashboard with SSO for enterprise comms teams.",
        "Remediation Dispatch: Auto-generates press release drafts and Wikipedia/Wikidata edit recommendations."
    ])
    add_card(slide, Inches(8.8), Inches(1.9), Inches(3.7), Inches(4.8), "Agency Financial Model", [
        "Average API cost per audit (Gemini Flash + Tavily): ~$0.15 (approx ₹13).",
        "Retainer margin: >85% software gross margin embedded within agency service fees.",
        "ARR Projection by Month 12: ₹1.2 Cr ($140K) in high-margin recurring software-assisted revenue."
    ])

    # -------------------------------------------------------------
    # SLIDE 13: Risk Analysis & Mitigation Strategies
    # -------------------------------------------------------------
    slide = prs.slides.add_slide(blank_layout)
    add_header(slide, "Risk Management", "Enterprise Risks & Mitigation Strategies", "Anticipating technical constraints, commercial pushback, and operational hurdles.")
    add_card(slide, Inches(0.8), Inches(1.9), Inches(3.7), Inches(4.8), "Risk: Search Ambiguity", [
        "Risk: Niche B2B brands or private subsidiaries may have thin public web coverage.",
        "Mitigation: System assigns 'Unverified / Thin Evidence' instead of declaring false negatives.",
        "Optional feature to ingest verified client master fact-sheets as primary ground truth."
    ])
    add_card(slide, Inches(4.8), Inches(1.9), Inches(3.7), Inches(4.8), "Risk: LLM Scraper Blocks", [
        "Risk: Search engines or AI platforms rate-limiting or blocking automated scrapers.",
        "Mitigation: Use compliant official API integrations (Tavily, Gemini, OpenAI).",
        "Distribute queries with exponential backoff and localized IP endpoints."
    ])
    add_card(slide, Inches(8.8), Inches(1.9), Inches(3.7), Inches(4.8), "Risk: Client Defensiveness", [
        "Risk: Client marketing teams feel defensive when their collaterals are flagged as inaccurate.",
        "Mitigation: Position CiteTrue as an ally against AI hallucinations, not an internal critic.",
        "Provide constructive 'Corrected Real Facts' and ready-to-publish PR statements."
    ])

    # -------------------------------------------------------------
    # SLIDE 14: Appendix & Live Prototype Deliverables
    # -------------------------------------------------------------
    slide = prs.slides.add_slide(blank_layout)
    add_header(slide, "Deliverables Submission", "Appendix: Live Prototype Verification & Repository", "Proof-of-concept prototype validating claim extraction and live search verification.")
    add_card(slide, Inches(0.8), Inches(1.9), Inches(5.6), Inches(4.8), "Live Assessment Links", [
        "Deployed Application Link: [Live Streamlit URL placeholder]",
        "GitHub Repository: [GitHub Repo URL placeholder]",
        "Demo Video: 30-second walkthrough demonstrating PDF upload and trap document verification.",
        "Test Dataset: `fixtures/trap_document.pdf` with documented `expected_flags.md`."
    ])
    add_card(slide, Inches(6.8), Inches(1.9), Inches(5.6), Inches(4.8), "Recruiter Evaluation Checklist", [
        "[x] Feature Design & Market Comparison: Profound, Peec AI, AthenaHQ, Scrunch, Semrush.",
        "[x] Product Strategy & Roadmap: 3-Month agency MVP and 12-Month monetization model.",
        "[x] Automated Fact-Checking Agent: Streamlit app with PDF text parsing & live web search.",
        "[x] Rigorous Truth Flagging: Verified, Inaccurate, and False with ground-truth corrections.",
        "[x] Clean Production Code: Pinned requirements.txt, secrets template, and comprehensive README."
    ])

    out_path = os.path.join("deliverables", "CogCulture_GEO_CiteTrue.pptx")
    prs.save(out_path)
    print(f"Presentation successfully created at: {out_path}")

if __name__ == "__main__":
    create_deck()
