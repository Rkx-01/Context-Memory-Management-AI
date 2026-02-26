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
