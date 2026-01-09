import streamlit as st
from PyPDF2 import PdfReader
import google.generativeai as genai
from langchain_community.tools import DuckDuckGoSearchRun
import time

# --- CONFIGURATION ---
st.set_page_config(page_title="Clarus | The Risk Agent", page_icon="⚖️", layout="wide")

# --- SIDEBAR ---
st.sidebar.title("Clarus ⚖️")
st.sidebar.markdown("**Intelligent Audit & Compliance Agent**")
api_key = st.sidebar.text_input("Enter Gemini API Key", type="password")
uploaded_file = st.sidebar.file_uploader("Upload Legal Document (PDF)", type="pdf")
st.sidebar.markdown("---")
st.sidebar.caption("Powered by Gemini Pro & DuckDuckGo")

# --- TOOLS ---
def extract_text_from_pdf(pdf_file):
    pdf_reader = PdfReader(pdf_file)
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text()
    return text

def web_background_check(entity_name):
    """Searches the live web for red flags."""
    search = DuckDuckGoSearchRun()
    query = f"{entity_name} fraud lawsuit bankruptcy scandal"
    try:
        results = search.run(query)
        return results
    except:
        return "No public red flags found or connection timed out."

# --- MAIN INTERFACE ---
st.title("Clarus 2.0")
st.subheader("Autonomous Risk & Background Auditor")

if uploaded_file is not None and api_key:
    # 1. READ
    with st.spinner("Clarus is reading the contract..."):
        raw_text = extract_text_from_pdf(uploaded_file)
        if len(raw_text) < 50:
             st.error("⚠️ Document appears empty.")
             st.stop()
        st.success(f"Document ingested. Length: {len(raw_text)} chars.")

    # 2. CONFIGURE BRAIN
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-1.5-flash')

    # 3. INTERROGATE
    query = st.text_input("Interrogate the Document:", placeholder="Ex: Analyze the indemnity clause")

    if query:
        # STEP A: ANALYZE CONTRACT
        with st.spinner("Analyzing legal text..."):
            system_prompt = f"""
            You are Clarus, a Senior Auditor. 
            1. Answer the user's question based strictly on the text below.
            2. EXTRACT the names of any Companies or Individuals mentioned in the text.
            3. Return the output in this format:
               - ANALYSIS: [Your answer]
               - ENTITIES: [List of names found, separated by commas]
            
            DOCUMENT: {raw_text}
            USER QUESTION: {query}
            """
            response = model.generate_content(system_prompt)
            full_response = response.text
            
            # Simple parsing to separate Analysis from Entities
            if "ENTITIES:" in full_response:
                analysis_part, entities_part = full_response.split("ENTITIES:")
            else:
                analysis_part = full_response
                entities_part = "None"

        # STEP B: THE DETECTIVE WORK (Live Search)
        st.markdown("### 📝 Contract Analysis")
        st.write(analysis_part.replace("ANALYSIS:", "").strip())
        
        entities = [e.strip() for e in entities_part.split(",") if e.strip() and "None" not in e]
        
        if entities:
            st.markdown("### 🕵️‍♂️ Background Investigation (Live Web)")
            progress_bar = st.progress(0)
            
            for i, entity in enumerate(entities[:3]): # Limit to top 3 to save time
                with st.spinner(f"Investigating {entity} for fraud/litigation..."):
                    flag_report = web_background_check(entity)
                    st.warning(f"**Target:** {entity}")
                    st.caption(f"**Search Findings:** {flag_report[:300]}...") # Show snippet
                    progress_bar.progress((i + 1) / len(entities[:3]))
            
            st.success("Investigation Complete.")
            
elif not api_key:
    st.info("👈 Enter API Key to activate Clarus.")