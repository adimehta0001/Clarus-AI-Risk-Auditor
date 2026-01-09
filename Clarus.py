import streamlit as st
from PyPDF2 import PdfReader
import google.generativeai as genai
from langchain_community.tools import DuckDuckGoSearchRun
import time
st.set_page_config(page_title="Clarus | The Risk Agent", page_icon="⚖️", layout="wide")
st.markdown("""
    <style>
    .stAlert { border-radius: 10px; }
    .report-text { font-family: 'Courier New', monospace; font-size: 14px; }
    </style>
    """, unsafe_allow_html=True)
st.sidebar.header("Clarus ⚖️")
st.sidebar.caption("Autonomous Due Diligence Agent")
api_key = st.sidebar.text_input("Gemini API Key", type="password")
uploaded_file = st.sidebar.file_uploader("Upload Contract (PDF)", type="pdf")
st.sidebar.markdown("---")
def extract_text_from_pdf(pdf_file):
    pdf_reader = PdfReader(pdf_file)
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text()
    return text

def search_web(query):
    """Deep searches the web for red flags."""
    search = DuckDuckGoSearchRun()
    try:
        return search.run(f"{query} fraud lawsuit bankruptcy scandal settlement")
    except:
        return "Search connection timed out."

st.title("Clarus 3.0")
st.markdown("### 🕵️‍♂️ Context-Aware Risk Auditor")

if uploaded_file and api_key:

    with st.spinner("Reading legal document..."):
        raw_text = extract_text_from_pdf(uploaded_file)
        st.success(f"Document Loaded. Length: {len(raw_text)} chars")

    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('models/gemini-flash-latest')

    if st.button("Run Full Audit"):

        with st.status("🔍 Extracting Entities...", expanded=True) as status:
            extraction_prompt = f"""
            Identify the legal entities (Companies/Parties) in this text. 
            Return ONLY a comma-separated list. No other text.
            Text: {raw_text[:5000]}
            """
            response_1 = model.generate_content(extraction_prompt)
            entities = [e.strip() for e in response_1.text.split(",") if len(e) > 2]
            
            st.write(f"**Identified Targets:** {entities}")
            status.update(label="✅ Entities Extracted", state="complete")

        web_evidence = {}
        with st.status("🌍 Running Background Checks...", expanded=True) as status:
            progress_bar = st.progress(0)
            
            for i, entity in enumerate(entities[:3]): # Limit to top 3
                st.write(f"Investigating: **{entity}**...")
                evidence = search_web(entity)
                web_evidence[entity] = evidence
                time.sleep(1) # Be polite to the search engine
                progress_bar.progress((i + 1) / len(entities[:3]))
            
            status.update(label="✅ Background Check Complete", state="complete")

        st.divider()
        st.subheader("⚖️ Final Risk Report")
        
        with st.spinner("Synthesizing Contract + Web Evidence..."):
            final_prompt = f"""
            You are Clarus, a Senior Risk Partner.
            
            TASK: 
            Analyze the CONTRACT TEXT and the WEB EVIDENCE below.
            
            1. **Contract Risks:** Highlight dangerous clauses (Indemnity, Payment, Termination).
            2. **External Risks:** Flag if any entity has recent fraud/bankruptcy news based on the web evidence.
            3. **Final Recommendation:** GO or NO-GO.
            
            ---
            CONTRACT TEXT:
            {raw_text[:5000]}
            
            ---
            WEB EVIDENCE:
            {str(web_evidence)}
            """
            
            final_report = model.generate_content(final_prompt)
            st.markdown(final_report.text)
            
            # Flash warning if "Fraud" is detected
            if "fraud" in final_report.text.lower() or "bankruptcy" in final_report.text.lower():
                st.error("🚨 CRITICAL ALERT: EXTERNAL RED FLAGS DETECTED")
            else:
                st.success("✅ No Critical External Red Flags")

elif not api_key:

    st.info("Enter API Key to initialize.")
