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

# Load environment variables
load_dotenv()

# Page configuration
st.set_page_config(
    page_title="CiteTrue GEO | Fact-Checking Engine",
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom minimal editorial CSS (Black & White with sleek accent)
st.markdown("""
<style>
    .main {
        background-color: #FAFAFA;
        color: #111111;
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
    }
    h1, h2, h3 {
        color: #111111;
        font-weight: 700;
        letter-spacing: -0.02em;
    }
    .badge-verified {
        background-color: #E8F5E9;
        color: #2E7D32;
        padding: 4px 10px;
        border-radius: 4px;
        font-weight: 600;
        font-size: 0.85rem;
        display: inline-block;
    }
    .badge-inaccurate {
        background-color: #FFF3E0;
        color: #E65100;
        padding: 4px 10px;
        border-radius: 4px;
        font-weight: 600;
        font-size: 0.85rem;
        display: inline-block;
    }
    .badge-false {
        background-color: #FFEBEE;
        color: #C62828;
        padding: 4px 10px;
        border-radius: 4px;
        font-weight: 600;
        font-size: 0.85rem;
        display: inline-block;
    }
    .metric-card {
        background: #FFFFFF;
        border: 1px solid #E0E0E0;
        padding: 16px;
        border-radius: 6px;
        text-align: center;
    }
</style>
""", unsafe_allow_html=True)

# Helper to read secrets from st.secrets or os.environ
def get_secret(key_name, default=""):
    if key_name in st.secrets:
        return st.secrets[key_name]
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
    max_claims_to_check = st.slider("Maximum claims to verify", min_value=3, max_value=20, value=10)
    
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

# File uploader
uploaded_file = st.file_uploader("Upload Document (PDF)", type=["pdf"], help="Upload client pitch decks, press releases, or whitepapers.")

col_sample, col_info = st.columns([1, 2])
with col_sample:
    use_trap_doc = st.button("📄 Load Assessment Trap Document", help="Loads pre-built trap document with 10 intentional lies and outdated stats.")

# State initialization
if "analysis_results" not in st.session_state:
    st.session_state.analysis_results = None

target_file = None
if uploaded_file is not None:
    target_file = uploaded_file
elif use_trap_doc:
    trap_path = os.path.join(os.path.dirname(__file__), "fixtures", "trap_document.pdf")
    if os.path.exists(trap_path):
        target_file = open(trap_path, "rb")
        st.info("Loaded `fixtures/trap_document.pdf` containing benchmark test claims.")
    else:
        st.warning("Trap document not yet created on disk. Please upload a PDF.")

if target_file and st.button("Run Truth-Check Audit", type="primary"):
    if not gemini_key:
        st.error("Please enter your Gemini API Key in the sidebar or `.streamlit/secrets.toml`.")
    elif not tavily_key:
        st.error("Please enter your Tavily API Key in the sidebar or `.streamlit/secrets.toml`.")
    else:
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
                    "Sources": ", ".join(verdict_data["sources"]) if verdict_data["sources"] else "None"
                })
                progress_bar.progress((i + 1) / len(claims))

            status.update(label="Fact-Check Audit Completed!", state="complete", expanded=False)
            st.session_state.analysis_results = results

# Display Results
if st.session_state.analysis_results:
    results = st.session_state.analysis_results
    df = pd.DataFrame(results)

    st.markdown("---")
    st.subheader("Audit Executive Summary")

    total_claims = len(results)
    verified_count = sum(1 for r in results if r["Verdict"] == "Verified")
    inaccurate_count = sum(1 for r in results if r["Verdict"] == "Inaccurate")
    false_count = sum(1 for r in results if r["Verdict"] == "False")

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.markdown(f"<div class='metric-card'><h3>{total_claims}</h3><p>Total Claims Audited</p></div>", unsafe_allow_html=True)
    with c2:
        st.markdown(f"<div class='metric-card'><h3 style='color:#2E7D32;'>{verified_count}</h3><p>Verified Accurate</p></div>", unsafe_allow_html=True)
    with c3:
        st.markdown(f"<div class='metric-card'><h3 style='color:#E65100;'>{inaccurate_count}</h3><p>Inaccurate / Outdated</p></div>", unsafe_allow_html=True)
    with c4:
        st.markdown(f"<div class='metric-card'><h3 style='color:#C62828;'>{false_count}</h3><p>False / Fabricated</p></div>", unsafe_allow_html=True)

    st.markdown("### Detailed Claim-Level Verification Matrix")
    
    # Custom display cards for clean PM UI
    for row in results:
        badge_class = "badge-verified" if row["Verdict"] == "Verified" else ("badge-inaccurate" if row["Verdict"] == "Inaccurate" else "badge-false")
        with st.container():
            st.markdown(f"""
            <div style='background: white; border: 1px solid #EAEAEA; border-left: 5px solid {"#2E7D32" if row["Verdict"]=="Verified" else ("#E65100" if row["Verdict"]=="Inaccurate" else "#C62828")}; padding: 14px 18px; margin-bottom: 12px; border-radius: 4px;'>
                <div style='display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;'>
                    <span style='font-size: 0.85rem; color: #666;'>Claim #{row["Claim ID"]} &bull; Category: <b>{row["Type"]}</b></span>
                    <span class='{badge_class}'>{row["Verdict"]}</span>
                </div>
                <div style='font-size: 1.05rem; font-weight: 500; margin-bottom: 8px;'>"{row["Claim"]}"</div>
                <div style='font-size: 0.95rem; margin-bottom: 6px;'><b>Corrected Real Fact:</b> {row["Corrected Fact / Ground Truth"]}</div>
                <div style='font-size: 0.88rem; color: #444; margin-bottom: 6px;'><b>Evidence:</b> {row["Evidence Summary"]}</div>
                <div style='font-size: 0.8rem; color: #777;'><b>Sources:</b> {row["Sources"]}</div>
            </div>
            """, unsafe_allow_html=True)

    # Export options
    csv = df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 Export Fact-Check Audit Report (CSV)",
        data=csv,
        file_name="citetrue_geo_audit_report.csv",
        mime="text/csv"
    )
