"""
CiteTrue GEO - Truth Layer & Automated Fact-Checking Platform
Built for Cog Culture Management Trainee PM Assessment
"""
import os
import streamlit as st
import pandas as pd
from dotenv import load_dotenv

from src.extract import parse_pdf_text, extract_claims_from_text
from src.search import search_web
from src.verify import judge_claim
from src.llm import STATUS, reset_status

# Load environment variables
load_dotenv()

# Page configuration
st.set_page_config(
    page_title="CiteTrue GEO | Fact-Checking Engine",
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom minimal editorial CSS with dark/light mode compatibility and elevated readability
st.markdown("""
<style>
    /* Clean typography & root adjustments */
    body, [data-testid="stAppViewContainer"] {
        font-family: -apple-system, BlinkMacSystemFont, "Inter", "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
    }
    
    /* Audit Metric Summary Cards */
    .metric-card {
        background: #18191C;
        border: 1px solid #2B2D31;
        border-radius: 10px;
        padding: 20px 14px;
        text-align: center;
        box-shadow: 0 2px 8px rgba(0,0,0,0.25);
    }
    .metric-number {
        font-size: 2.2rem;
        font-weight: 800;
        line-height: 1.1;
        margin-bottom: 6px;
    }
    .metric-label {
        font-size: 0.85rem;
        font-weight: 500;
        color: #A0A5AD;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }

    /* Verification Claim Card */
    .claim-card {
        background-color: #16171B;
        border: 1px solid #282A2F;
        border-radius: 10px;
        padding: 22px 24px;
        margin-bottom: 18px;
        box-shadow: 0 4px 14px rgba(0,0,0,0.2);
        transition: transform 0.15s ease, border-color 0.15s ease;
    }
    .claim-card:hover {
        border-color: #3F4249;
    }

    /* Badges */
    .badge-pill {
        padding: 5px 12px;
        border-radius: 6px;
        font-weight: 700;
        font-size: 0.82rem;
        text-transform: uppercase;
        letter-spacing: 0.04em;
        display: inline-flex;
        align-items: center;
    }
    .badge-verified {
        background: rgba(46, 125, 50, 0.18);
        color: #4CAF50;
        border: 1px solid rgba(76, 175, 80, 0.4);
    }
    .badge-inaccurate {
        background: rgba(230, 81, 0, 0.18);
        color: #FF9800;
        border: 1px solid rgba(255, 152, 0, 0.4);
    }
    .badge-false {
        background: rgba(198, 40, 40, 0.18);
        color: #EF5350;
        border: 1px solid rgba(239, 83, 80, 0.4);
    }
    .badge-unverified {
        background: rgba(156, 163, 175, 0.18);
        color: #9CA3AF;
        border: 1px solid rgba(156, 163, 175, 0.4);
    }

    /* Claim Text and Content */
    .claim-quote {
        font-size: 1.12rem;
        font-weight: 600;
        color: #F3F4F6;
        line-height: 1.5;
        margin-top: 10px;
        margin-bottom: 14px;
        border-left: 3px solid #E53935;
        padding-left: 12px;
    }
    .claim-fact-box {
        background: #1F2127;
        border-radius: 6px;
        padding: 12px 16px;
        margin-bottom: 12px;
        font-size: 0.95rem;
        color: #E2E4E9;
        line-height: 1.45;
    }
    .claim-evidence {
        font-size: 0.9rem;
        color: #B0B5BF;
        line-height: 1.45;
        margin-bottom: 12px;
    }

    /* Clickable Source Pills */
    .source-pills-container {
        display: flex;
        flex-wrap: wrap;
        gap: 8px;
        align-items: center;
        margin-top: 6px;
    }
    .source-link-pill {
        display: inline-flex;
        align-items: center;
        background: #23252C;
        color: #60A5FA !important;
        border: 1px solid #374151;
        padding: 4px 12px;
        border-radius: 16px;
        font-size: 0.8rem;
        text-decoration: none !important;
        font-weight: 500;
        transition: all 0.15s ease-in-out;
    }
    .source-link-pill:hover {
        background: #2D3748;
        color: #93C5FD !important;
        border-color: #60A5FA;
        text-decoration: none !important;
    }
</style>
""", unsafe_allow_html=True)

# Helper to read secrets from st.secrets or os.environ safely
def get_secret(key_name, default=""):
    try:
        if key_name in st.secrets:
            return st.secrets[key_name]
    except Exception:
        pass
    return os.environ.get(key_name, default)

# Sidebar configuration
with st.sidebar:
    st.markdown("### ⚙️ API Configuration")
    st.caption("CiteTrue cross-references document statistics with live web search.")
    
    gemini_key = st.text_input(
        "Gemini API Key",
        value=get_secret("GEMINI_API_KEY"),
        type="password",
        help="Used for structured claim extraction and truth judgment reasoning."
    )
    
    tavily_key = st.text_input(
        "Tavily API Key",
        value=get_secret("TAVILY_API_KEY"),
        type="password",
        help="Used to retrieve live ground-truth web search snippets."
    )
    
    st.markdown("---")
    max_claims_to_check = st.slider("Maximum claims to verify", 10, 15, 15)
    
    st.markdown("---")
    st.markdown("### 📌 About CiteTrue GEO")
    st.caption(
        "A feature designed for **Cog Culture's GEO (Generative Engine Optimization)** practice. "
        "Standard GEO tools count brand mentions. CiteTrue audits whether LLM responses and client collaterals "
        "quote verified, outdated, or hallucinated facts."
    )

# Header Section
st.title("CiteTrue GEO — Automated Fact-Checking Layer")
st.markdown(
    "**Objective:** Upload marketing collaterals or brand audit PDFs. "
    "CiteTrue isolates specific statistical and date claims, cross-references them against live web data, "
    "and detects outdated or hallucinated figures with verified real-world corrections."
)

# Step 1: Primary Document Uploader
st.markdown("### 📤 Step 1: Upload Document to Fact-Check")
primary_uploaded_file = st.file_uploader(
    "Upload PDF (Marketing Collateral / PR / Research Deck / Any Document)", 
    type=["pdf"], 
    key="primary_doc_uploader",
    help="Upload the primary document whose claims, dates, and stats you want to verify."
)

st.markdown("---")

# Step 2: Recruiter Benchmark & Trap Document Testing
st.markdown("### 🎯 Step 2: Assessment Benchmark & Trap Document Testing")
st.caption("Recruiters can evaluate the system using their own custom trap document, or by running the pre-built benchmark test document.")

tab_custom_trap, tab_preset_trap = st.tabs(["📁 Upload Your Custom Trap Document", "⚡ Use Pre-Built Assessment Trap Document"])

with tab_custom_trap:
    custom_trap_file = st.file_uploader(
        "Upload your Trap Document (PDF containing intentional lies & outdated stats)",
        type=["pdf"],
        key="custom_trap_uploader",
        help="Upload the recruiter trap document to test if CiteTrue correctly catches fake numbers and outdated statistics."
    )

with tab_preset_trap:
    st.markdown("**Pre-Built Evaluation Suite (`fixtures/trap_document.pdf`)**")
    st.caption("Contains 8 benchmark test claims: Swiggy IPO, Zomato-Blinkit acquisition valuation, Apollo Hospitals beds, and PepsiCo CEO.")
    col_load, col_view, col_spacer = st.columns([1.5, 1.2, 2.5])
    with col_load:
        use_trap_doc = st.button("📄 Load Assessment Trap Document", help="Loads pre-built trap document with intentional lies and outdated stats.")
    with col_view:
        view_trap_doc = st.button("👁️ View Document", help="Inspect the raw text and claims inside the trap document before running.")

# State initialization
if "analysis_results" not in st.session_state:
    st.session_state.analysis_results = None
if "selected_document_source" not in st.session_state:
    st.session_state.selected_document_source = None

# Dialog for previewing the Trap Document content
@st.dialog("📄 Assessment Trap Document Preview")
def preview_trap_doc_dialog():
    trap_path = os.path.join(os.path.dirname(__file__), "fixtures", "trap_document.pdf")
    if os.path.exists(trap_path):
        pages = parse_pdf_text(trap_path)
        st.markdown("**Document Title:** Enterprise Market Analysis & Technology Audit (2025/2026)")
        st.caption("This document contains intentional truthful facts, outdated stats, and fabricated figures used to benchmark fact-checking accuracy.")
        st.markdown("---")
        for p in pages:
            st.markdown(f"**Page {p['page_number']} Content:**")
            st.code(p["text"], language="markdown")
        st.markdown("---")
        st.caption("💡 Click 'Load Assessment Trap Document' on the main screen to run the verification engine on this document.")
    else:
        st.error("Trap document file not found at fixtures/trap_document.pdf")

if view_trap_doc:
    preview_trap_doc_dialog()

if use_trap_doc:
    st.session_state.selected_document_source = "preset_trap"
    st.toast("✅ Assessment Trap Document loaded successfully!", icon="📄")

if custom_trap_file is not None:
    st.session_state.selected_document_source = "custom_trap"

if primary_uploaded_file is not None and custom_trap_file is None and not use_trap_doc and st.session_state.selected_document_source != "preset_trap":
    st.session_state.selected_document_source = "primary_upload"

# Active Document Indicator Banner
target_file = None
active_doc_name = ""

if custom_trap_file is not None:
    target_file = custom_trap_file
    active_doc_name = f"Custom Trap Document: {custom_trap_file.name}"
    st.success(f"🎯 **Active Target:** `{active_doc_name}` ready to fact-check.")
elif st.session_state.selected_document_source == "preset_trap":
    trap_path = os.path.join(os.path.dirname(__file__), "fixtures", "trap_document.pdf")
    if os.path.exists(trap_path):
        target_file = open(trap_path, "rb")
        active_doc_name = "Pre-built Assessment Trap Document (fixtures/trap_document.pdf)"
        st.success(f"🎯 **Active Target:** `{active_doc_name}` ready to fact-check.")
    else:
        st.warning("Trap document not yet created on disk. Please upload a PDF.")
elif primary_uploaded_file is not None:
    target_file = primary_uploaded_file
    active_doc_name = f"Primary Document: {primary_uploaded_file.name}"
    st.info(f"📄 **Active Target:** `{active_doc_name}` ready to fact-check.")
else:
    st.info("👆 Please upload a document or select the Assessment Trap Document above to begin.")

if target_file and st.button("Run Truth-Check Audit", type="primary"):
    if not gemini_key:
        st.error("Please enter your Gemini API Key in the sidebar or `.streamlit/secrets.toml`.")
    elif not tavily_key:
        st.error("Please enter your Tavily API Key in the sidebar or `.streamlit/secrets.toml`.")
    else:
        reset_status()
        with st.status("Executing CiteTrue GEO Pipeline...", expanded=True) as status:
            st.write("📖 **Step 1:** Extracting text from document...")
            pages_data = parse_pdf_text(target_file)
            st.write(f"Parsed {len(pages_data)} pages.")

            st.write("🔍 **Step 2:** Extracting specific quantitative claims (dates, metrics, stats)...")
            claims = extract_claims_from_text(pages_data, gemini_api_key=gemini_key, max_claims=max_claims_to_check)
            st.write(f"Extracted {len(claims)} testable claims.")

            st.write("🌐 **Step 3 & 4:** Querying live web and verifying accuracy with citations...")
            progress_bar = st.progress(0)
            results = []

            for i, c in enumerate(claims):
                query = c.get("search_query") or c.get("quote")
                search_results = search_web(query, api_key=tavily_key, max_results=3)
                verdict_data = judge_claim(c, search_results, gemini_api_key=gemini_key)
                
                results.append({
                    "Claim ID": c.get("claim_id", i+1),
                    "Claim": c.get("quote"),
                    "Type": c.get("claim_type", "statistic"),
                    "Verdict": verdict_data["verdict"],
                    "Corrected Fact / Ground Truth": verdict_data["corrected_fact"],
                    "Evidence Summary": verdict_data["evidence_summary"],
                    "Sources": verdict_data.get("sources", []),
                    "Sources_str": ", ".join(verdict_data.get("sources", [])) if verdict_data.get("sources") else "None"
                })
                progress_bar.progress((i + 1) / len(claims))

            status.update(label="Fact-Check Audit Completed!", state="complete", expanded=False)
            st.session_state.analysis_results = results

# Display Results
if st.session_state.analysis_results:
    if STATUS.get("extract_mode") == "regex" or STATUS.get("llm_fail", 0) > 0:
        st.warning("Gemini was rate-limited; some claims show Unverified. Retry in a minute.")

    results = st.session_state.analysis_results
    df = pd.DataFrame(results)

    st.markdown("---")
    st.subheader("Audit Executive Summary")

    total_claims = len(results)
    verified_count = sum(1 for r in results if r["Verdict"] == "Verified")
    inaccurate_count = sum(1 for r in results if r["Verdict"] == "Inaccurate")
    false_count = sum(1 for r in results if r["Verdict"] == "False")
    unverified_count = sum(1 for r in results if r["Verdict"] == "Unverified")

    c1, c2, c3, c4, c5 = st.columns(5)
    with c1:
        st.markdown(f"""
        <div class='metric-card'>
            <div class='metric-number' style='color:#F3F4F6;'>{total_claims}</div>
            <div class='metric-label'>Total Audited</div>
        </div>
        """, unsafe_allow_html=True)
    with c2:
        st.markdown(f"""
        <div class='metric-card'>
            <div class='metric-number' style='color:#4CAF50;'>{verified_count}</div>
            <div class='metric-label'>Verified</div>
        </div>
        """, unsafe_allow_html=True)
    with c3:
        st.markdown(f"""
        <div class='metric-card'>
            <div class='metric-number' style='color:#FF9800;'>{inaccurate_count}</div>
            <div class='metric-label'>Inaccurate</div>
        </div>
        """, unsafe_allow_html=True)
    with c4:
        st.markdown(f"""
        <div class='metric-card'>
            <div class='metric-number' style='color:#EF5350;'>{false_count}</div>
            <div class='metric-label'>False</div>
        </div>
        """, unsafe_allow_html=True)
    with c5:
        st.markdown(f"""
        <div class='metric-card'>
            <div class='metric-number' style='color:#9CA3AF;'>{unverified_count}</div>
            <div class='metric-label'>Unverified</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<div style='margin-top: 30px;'></div>", unsafe_allow_html=True)
    st.subheader("Detailed Claim-Level Verification Matrix")
    
    # Custom display cards for clean PM UI
    for row in results:
        v = row["Verdict"]
        if v == "Verified":
            badge_class = "badge-verified"
            border_accent = "#4CAF50"
        elif v == "Inaccurate":
            badge_class = "badge-inaccurate"
            border_accent = "#FF9800"
        elif v == "False":
            badge_class = "badge-false"
            border_accent = "#EF5350"
        else:
            badge_class = "badge-unverified"
            border_accent = "#9CA3AF"
        
        # Build clickable source pills
        sources_list = row.get("Sources", [])
        if isinstance(sources_list, str):
            sources_list = [s.strip() for s in sources_list.split(",") if s.strip() and s.strip() != "None"]
            
        pills_html = ""
        if sources_list:
            for s_url in sources_list:
                clean_url = s_url.strip()
                if clean_url.startswith("http"):
                    # Extract domain for clean aesthetic pill label
                    try:
                        from urllib.parse import urlparse
                        domain = urlparse(clean_url).netloc.replace("www.", "")
                        label = domain if domain else "Source Link"
                    except Exception:
                        label = "Source Link"
                    pills_html += f"<a href='{clean_url}' target='_blank' rel='noopener noreferrer' class='source-link-pill'>🔗 {label} ↗</a> "
                else:
                    pills_html += f"<span style='color:#9CA3AF; font-size:0.8rem;'>{clean_url}</span> "
        else:
            pills_html = "<span style='color:#9CA3AF; font-size:0.85rem; font-style:italic;'>No public external web citations found</span>"

        with st.container():
            st.markdown(f"""
            <div class='claim-card' style='border-left: 5px solid {border_accent};'>
                <div style='display: flex; justify-content: space-between; align-items: center; margin-bottom: 6px;'>
                    <span style='font-size: 0.82rem; font-weight: 600; color: #9CA3AF; letter-spacing: 0.05em; text-transform: uppercase;'>
                        Claim #{row["Claim ID"]} &nbsp;•&nbsp; Type: <span style='color: #E2E8F0;'>{row["Type"]}</span>
                    </span>
                    <span class='badge-pill {badge_class}'>{row["Verdict"]}</span>
                </div>
                <div class='claim-quote'>"{row["Claim"]}"</div>
                <div class='claim-fact-box'>
                    <div style='font-size: 0.8rem; font-weight: 700; color: #9CA3AF; text-transform: uppercase; letter-spacing: 0.05em; margin-bottom: 3px;'>
                        Corrected Real-World Fact / Consensus
                    </div>
                    <div style='font-size: 0.98rem; font-weight: 500;'>{row["Corrected Fact / Ground Truth"]}</div>
                </div>
                <div class='claim-evidence'>
                    <b style='color: #D1D5DB;'>Evidence Analysis:</b> {row["Evidence Summary"]}
                </div>
                <div style='margin-top: 10px;'>
                    <div style='font-size: 0.8rem; font-weight: 600; color: #9CA3AF; margin-bottom: 5px; text-transform: uppercase; letter-spacing: 0.04em;'>
                        Authoritative Sources (Clickable):
                    </div>
                    <div class='source-pills-container'>
                        {pills_html}
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)

    # Export options
    export_df = df.drop(columns=["Sources"], errors="ignore")
    export_df = export_df.rename(columns={"Sources_str": "Sources"})
    csv = export_df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 Export Fact-Check Audit Report (CSV)",
        data=csv,
        file_name="citetrue_geo_audit_report.csv",
        mime="text/csv"
    )
