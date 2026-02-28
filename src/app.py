import streamlit as st
import datetime
import pandas as pd
from memory_system import MemoryManager, MemoryNode
from main import setup_scenario_1, setup_scenario_2

st.set_page_config(
    page_title="Contextual Intelligence Edge",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Premium SaaS CSS Injection ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

    /* Global Typography & Background */
    :root {
        --text-color: #111827;
        --bg-color: #f4f6f8;
    }
    
    html, body, [class*="css"], .stApp {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif !important;
        background-color: var(--bg-color) !important;
        color: var(--text-color) !important;
    }
    
    /* Override Streamlit's aggressive text coloring in certain containers */
    .stMarkdown, p, div {
        color: var(--text-color);
    }
    
    /* specifically target sidebar text */
    [data-testid="stSidebar"] * {
        color: #111827 !important;
    }
    
    [data-testid="stMarkdownContainer"] {
        color: var(--text-color) !important;
    }

    /* Target specific header elements */
    h1, h2, h3, h4, h5, h6 {
        color: #0f172a !important;
    }

    /* Target the text in the metric containers */
    [data-testid="stMetricValue"], [data-testid="stMetricLabel"] {
        color: #111827 !important;
    }
    
    /* Ensure the main app container background is light */
    .stApp > header {
        background-color: transparent;
    }
    
    .stApp {
        background-color: var(--bg-color);
    }
    
    /* Hide Streamlit Branding elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Typography Overrides */
    h1, h2 {
        font-weight: 600 !important;
        letter-spacing: -0.02em !important;
        color: #0f172a !important;
    }
    h3, h4, h5 {
        font-weight: 500 !important;
        color: #334155 !important;
    }

    /* Sidebar Clean-up */
    [data-testid="stSidebar"] {
        background-color: #ffffff !important;
        border-right: 1px solid #e2e8f0;
    }
    
    /* Action Cards (Incoming Context) */
    .trigger-card {
        background: #ffffff;
        border: 1px solid #e5e7eb;
        border-radius: 12px;
        padding: 24px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05), 0 2px 4px -1px rgba(0, 0, 0, 0.03);
        margin-bottom: 24px;
        position: relative;
        overflow: hidden;
    }
    .trigger-card::before {
        content: '';
        position: absolute;
        top: 0; left: 0; right: 0; height: 4px;
        background: linear-gradient(90deg, #3b82f6, #8b5cf6);
    }
    .trigger-alert::before {
        background: linear-gradient(90deg, #ef4444, #f97316);
    }
    .trigger-header {
        font-size: 0.85rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        color: #6b7280;
        margin-bottom: 12px;
        display: flex;
        align-items: center;
        gap: 8px;
    }
    .trigger-body {
        font-size: 1.15rem;
        font-weight: 500;
        color: #111827;
        margin-bottom: 16px;
        line-height: 1.5;
    }
    
    /* Meta Data Tag styling */
    .meta-row {
        display: flex;
        gap: 16px;
        border-top: 1px solid #f3f4f6;
        padding-top: 16px;
        margin-top: 16px;
    }
    .meta-tag {
        display: inline-flex;
        flex-direction: column;
    }
    .meta-label {
        font-size: 0.75rem;
        color: #9ca3af;
        text-transform: uppercase;
        font-weight: 600;
        margin-bottom: 4px;
    }
    .meta-value {
        font-size: 0.875rem;
        color: #374151;
        font-family: 'Inter', monospace;
        font-weight: 500;
    }

    /* Retrieved Memory Nodes */
    .node-item {
        background: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 8px;
        padding: 16px 20px;
        margin-bottom: 16px;
        transition: all 0.2s ease;
        border-left: 4px solid #cbd5e1;
    }
    .node-item:hover {
        transform: translateY(-2px);
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.05), 0 4px 6px -2px rgba(0, 0, 0, 0.025);
    }
    
    /* Type-specific borders */
    .border-issue { border-left-color: #ef4444; }
    .border-event { border-left-color: #3b82f6; }
    .border-rule  { border-left-color: #10b981; }

    .node-top {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 10px;
    }
    .node-badge {
        font-size: 0.7rem;
        font-weight: 600;
        letter-spacing: 0.02em;
        padding: 4px 10px;
        border-radius: 6px;
        text-transform: uppercase;
        background: #f1f5f9;
        color: #475569;
    }
    .node-score {
        font-family: 'Inter', monospace;
        font-size: 0.85rem;
        font-weight: 600;
        color: #0f172a;
        background: #f8fafc;
        padding: 4px 8px;
        border-radius: 4px;
        border: 1px solid #e2e8f0;
    }
    .node-content {
        font-size: 0.95rem;
        color: #334155;
        line-height: 1.5;
        margin-bottom: 12px;
    }
    .node-bottom {
        display: flex;
        gap: 16px;
        font-size: 0.8rem;
        color: #64748b;
    }
    .node-bottom span {
        display: flex;
        align-items: center;
        gap: 4px;
    }

    /* Summary Box */
    .summary-box {
        background: #f8fafc;
        border: 1px solid #e2e8f0;
        border-radius: 8px;
        padding: 16px;
        margin-top: 24px;
    }
    .summary-box h4 {
        margin-top: 0;
        color: #0f172a;
        font-size: 0.9rem;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
</style>
""", unsafe_allow_html=True)


# --- Application Layout ---
col_head1, col_head2 = st.columns([3, 1])
with col_head1:
    st.markdown("<h1 style='margin-bottom:0;'>Contextual Edge Intelligence</h1>", unsafe_allow_html=True)
    st.markdown("<p style='color:#64748b; font-size:1.1rem; margin-top:5px;'>Automated entity resolution and historical context retrieval pipeline.</p>", unsafe_allow_html=True)
with col_head2:
    st.markdown("<div style='text-align:right; padding-top:20px;'><span style='background:#10b981; color:white; padding:4px 12px; border-radius:12px; font-size:0.8rem; font-weight:600;'>SYSTEM ONLINE</span></div>", unsafe_allow_html=True)

st.markdown("<hr style='margin-top:10px; margin-bottom:30px; border-color:#e2e8f0;'/>", unsafe_allow_html=True)

with st.sidebar:
    st.markdown("### 🗂 Workspace Target")
    scenario_choice = st.radio(
        "Select Active Pipeline:",
        [
            "Invoice QA (Supplier XYZ)", 
            "Support Triage (TechCorp)"
        ],
        label_visibility="collapsed"
    )
    
    st.markdown("<br/>", unsafe_allow_html=True)
    st.markdown("### ⚙️ Engine Tuning")
    st.markdown("<p style='font-size:0.8rem; color:#64748b;'>Adjust Proximity Algorithm (P<sub>total</sub>) weights on the fly.</p>", unsafe_allow_html=True)
    
    w_temp = st.slider("🕒 Temporal Weight", 0.0, 2.0, 1.0, 0.1)
    w_rel = st.slider("🕸 Relational Distance", 0.0, 2.0, 1.0, 0.1)
    w_sem = st.slider("🧠 Semantic Overlap", 0.0, 2.0, 1.0, 0.1)
    
    st.markdown("<hr/>", unsafe_allow_html=True)
    st.markdown("<p style='font-size:0.75rem; color:#94a3b8; text-align:center;'>Graph DB Connected • Latency: 12ms</p>", unsafe_allow_html=True)


def render_node(node, score, current_time):
    """Renders a historical memory node."""
    age_days = (current_time - node.timestamp).days
    
    if node.is_evergreen:
        age_str = "Status: Evergreen Policy"
        border_class = "border-rule"
        icon = "📌"
    else:
        age_str = f"Age: {age_days}d"
        border_class = "border-issue" if "Issue" in node.node_type or "frustrat" in node.content.lower() else "border-event"
        icon = "📅"
        
    html = f"""
    <div class="node-item {border_class}">
        <div class="node-top">
            <span class="node-badge">{node.node_type}</span>
            <span class="node-score">Score: {score:.3f}</span>
        </div>
        <div class="node-content">
            {node.content}
        </div>
        <div class="node-bottom">
            <span>{icon} {age_str}</span>
            <span>🆔 {node.node_id}</span>
        </div>
    </div>
    """
    st.markdown(html, unsafe_allow_html=True)


# --- Scenario Execution ---
col_main, col_side = st.columns([1.1, 1.8], gap="large")

if "Invoice QA" in scenario_choice:
    mm, current_time = setup_scenario_1()
    mm.w_temp, mm.w_rel, mm.w_sem = w_temp, w_rel, w_sem
    
    invoice_data = MemoryNode("INV_123", "Invoice", "Process PO-9921 from Supplier XYZ for ₹2,50,000.", current_time)
    invoice_data.add_edge("SUP_XYZ", "BELONGS_TO")
    mm.add_node(invoice_data)
    
    with col_main:
        st.markdown("### Trigger Source")
        st.markdown(f"""
        <div class="trigger-card">
            <div class="trigger-header">
                <svg width="16" height="16" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"></path></svg>
                Incoming Transaction
            </div>
            <div class="trigger-body">{invoice_data.content}</div>
            <div class="meta-row">
                <div class="meta-tag">
                    <span class="meta-label">Entity Ref</span>
                    <span class="meta-value">SUP_XYZ</span>
                </div>
                <div class="meta-tag">
                    <span class="meta-label">Amount</span>
                    <span class="meta-value">₹2,50,000</span>
                </div>
                <div class="meta-tag">
                    <span class="meta-label">Time</span>
                    <span class="meta-value">{current_time.strftime('%H:%M:%S UTC')}</span>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        with st.expander("Raw Graph Payload Response"):
            st.json({
                "nodes_traversed": 412,
                "query_latency_ms": 14.2,
                "confidence_interval": 0.92
            })

    with col_side:
        st.markdown("### Retrieved Contextual Subgraph")
        results = mm.retrieve_context(invoice_data, current_time, query="quality delay shipment", top_k=3)
        
        for node, score in results:
            render_node(node, score, current_time)
            
        st.markdown("""
        <div class="summary-box">
            <h4>⚡ Synthesized Recommendation</h4>
            <span style="color:#ef4444; font-weight:600;">ACTION REQUIRED:</span> 
            System detected a severe quality breach (Score > 2.0) directly linked to Supplier XYZ from Q2. Additionally, current evergreen parameters indicate high-risk thermal degradation for current shipments. 
            <br/><br/>
            <strong>Route to:</strong> Level 2 Procurements Analyst & physical QA terminal.
        </div>
        """, unsafe_allow_html=True)


elif "Support Triage" in scenario_choice:
    mm, current_time = setup_scenario_2()
    mm.w_temp, mm.w_rel, mm.w_sem = w_temp, w_rel, w_sem
    
    ticket_data = MemoryNode("TICKET_900", "Ticket", "P0 Escalation: TechCorp pipeline integration returning 500 errors across all endpoints.", current_time)
    ticket_data.add_edge("CUST_TC", "SUBMITTED_BY")
    mm.add_node(ticket_data)
    
    with col_main:
        st.markdown("### Trigger Source")
        st.markdown(f"""
        <div class="trigger-card trigger-alert">
            <div class="trigger-header" style="color:#ef4444;">
                <svg width="16" height="16" fill="currentColor" viewBox="0 0 20 20"><path fill-rule="evenodd" d="M8.257 3.099c.765-1.36 2.722-1.36 3.486 0l5.58 9.92c.75 1.334-.213 2.98-1.742 2.98H4.42c-1.53 0-2.493-1.646-1.743-2.98l5.58-9.92zM11 13a1 1 0 11-2 0 1 1 0 012 0zm-1-8a1 1 0 00-1 1v3a1 1 0 002 0V6a1 1 0 00-1-1z" clip-rule="evenodd"></path></svg>
                Critical Alert
            </div>
            <div class="trigger-body">{ticket_data.content}</div>
            <div class="meta-row">
                <div class="meta-tag">
                    <span class="meta-label">Customer</span>
                    <span class="meta-value">TechCorp Inc.</span>
                </div>
                <div class="meta-tag">
                    <span class="meta-label">SLA Limit</span>
                    <span class="meta-value">60 Mins</span>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        st.metric("Customer Health Index", "68/100", "-12 points", delta_color="inverse")
        st.metric("Current ARR", "₹50L", "Active")

    with col_side:
        st.markdown("### Retrieved Contextual Subgraph")
        results = mm.retrieve_context(ticket_data, current_time, query="integration technical competitors", top_k=4)
        
        for node, score in results:
            render_node(node, score, current_time)
            
        st.markdown("""
        <div class="summary-box">
            <h4>⚡ Synthesized Recommendation</h4>
            <span style="color:#ef4444; font-weight:600;">FLIGHT RISK:</span> 
            High churn probability. Contract was recently renewed but explicitly contained competitor evaluations (Highest Relational Score). Standard responses will fail based on evergreen stakeholder preferences.
            <br/><br/>
            <strong>Route to:</strong> Tier 3 Engineering Squad (Lead by CTO). Suppress automated level-1 summaries.
        </div>
        """, unsafe_allow_html=True)
