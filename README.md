# ⚖️ Clarus: Autonomous Due Diligence Agent

**"Trust, but verify. Then verify again with AI."**

### **The Problem**
In high-stakes corporate finance, a contract is only as good as the counterparty signing it. Traditional contract analysis tools (OCR) can read the *text*, but they cannot assess the *context*. They don't know if the supplier was sued yesterday or if the partner filed for bankruptcy this morning.

### **The Solution: Clarus**
Clarus is an **Agentic AI System** that bridges the gap between **Document Intelligence** and **Real-World Investigation**.

It does not just summarize legal text; it extracts entities, performs live background checks via web search, and synthesizes a final "Risk Verdict" based on both the contract's clauses and the counterparty's reputation.

---

### **🚀 Key Capabilities**
* **📄 Legal Logic Analysis:** powered by **Google Gemini 1.5 Flash**, it identifies aggressive indemnity clauses, missing termination rights, and non-standard payment terms.
* **🕵️‍♂️ Autonomous Background Checks:** Automatically extracts company names and performs deep-web searches (DuckDuckGo) for fraud, litigation, and bankruptcy news.
* **🚨 Cross-Referenced Verdicts:** Flagging a contract not just because the *terms* are bad, but because the *partner* is compromised (e.g., detecting a bankrupt counterparty in a valid-looking service agreement).

### **🛠️ The Tech Stack**
* **Orchestration:** LangChain (Python)
* **LLM Engine:** Google Gemini Pro (1.5 Flash)
* **Search Tool:** DuckDuckGo Search API
* **Frontend:** Streamlit

### **📉 Example Use Case (The "FTX" Test)**
* **Input:** A standard service agreement involving "FTX Trading Ltd."
* **Contract Analysis:** The tool flagged "Payment in FTT Tokens" as a liquidity risk.
* **External Analysis:** The tool detected "FTX Trading Ltd" is currently in bankruptcy proceedings and its founder is incarcerated.
* **Final Verdict:** **CRITICAL NO-GO.**

---
*Built by [Aditya Mehta ] - Transforming Risk Management with Agentic AI.*