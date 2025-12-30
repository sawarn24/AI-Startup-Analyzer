# main.py - Main entry point with routing

import streamlit as st
from streamlit import session_state as ss
import time

# Must be the first Streamlit command
st.set_page_config(
    page_title="AI Startup Analyzer",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Initialize session state for page navigation
if 'current_page' not in ss:
    ss.current_page = 'landing'

# Shared CSS for consistent theming across pages
SHARED_CSS = """
<style>/* Base layout: avoid horizontal overflow and include padding in box-sizing */
    html, body, .stApp { box-sizing: border-box; margin: 0; padding: 0; overflow-x: hidden; }
    *, *:before, *:after { box-sizing: inherit; }

    .stApp {
        background-color: #0E1117;
        color: #FAFAFA;
    }

    header, footer { visibility: hidden; }
    /* Make room for fixed navbar and provide 100px gutters on both sides */
        .block-container { padding-top: 72px; padding-left: 0.1rem; padding-right: 0.1rem; max-width: 1200px; margin: 0 auto; }

    /* NAVBAR */
    .navbar {
        position: fixed;
        top: 0;
        left: 0;
        right: 0;
        height: 64px;
        background: #F3F4F6;
        backdrop-filter: blur(10px);
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 0 1.5rem;
        z-index: 1000;
        border-bottom: 1px solid #E5E7EB;
    }

    .nav-left { font-size: 20px; font-weight: 700; color: #0E1117; }

    .nav-right a {
        margin-left: 18px;
        color: #1F2937;
        text-decoration: none;
        font-size: 15px;
        font-weight: 600;
    }

    .nav-right a:hover { 
        color: #6366F1;
        cursor: pointer;
    }
    /* HERO */
    /* Reduced top padding so the hero sits closer under the navbar */
    /* Reduced bottom padding to bring Features closer */
    .hero { padding: 0.1rem 0.1rem 0.1rem 0.1rem; }

    .hero-title { 
    line-height: 1.15; 
    }
    .hero-welcome {
    display: inline-block;
    overflow: hidden;
    white-space: nowrap;

    animation: typing 1.6s steps(26, end) forwards;

    font-size: 40px;
    font-weight: 600;
    margin-right: 0.6rem;
    color: #D1D5DB;   /* soft gray */
    vertical-align: middle;
    width: 26ch;
}

    .hero-brand { display: inline-block; font-size: 83px; font-weight: 900; line-height:1; background: linear-gradient(90deg,#7C3AED,#06B6D4); -webkit-background-clip: text; background-clip: text; color: transparent; vertical-align: middle; }

    @keyframes typing { from { width: 0ch; } to { width: 26ch; } }
    @keyframes blink-caret { from, to { border-color: transparent; } 50% { border-color: rgba(255,255,255,0.85); } }

    .hero-desc {
        font-size: 19px;
        color: #D1D5DB;
        margin-top: 1.4rem;
        max-width: 720px;
    }

    /* BUTTON */
    .stButton > button {
        background: linear-gradient(90deg,#6366F1,#06B6D4);
        color: white;
        border-radius: 12px;
        padding: 0.85rem 2.2rem;
        border: none;
        font-size: 16px;
        margin-top: 2rem;
        margin-bottom: 0rem !important;
        box-shadow: 0 10px 30px rgba(99,102,241,0.12);
        transition: transform 0.12s ease, box-shadow 0.12s ease;
    }

    .stButton > button:hover { transform: translateY(-3px); box-shadow: 0 18px 40px rgba(99,102,241,0.18); }
    .stButton { margin-bottom: 0 !important; }

    /* ILLUSTRATION CONTAINER */
    .illustration-container {
        position: relative;
        width: 100%;
        height: auto; /* allow content to size naturally */
        margin-top: 0; /* remove extra vertical offset */
        padding-top: 0.5rem;
    }

    /* FLOATING BOT */
    .bot {
        position: absolute;
        right: 0px;
        top: 40px; /* Moved down from 20px */
        width: 380px;
        max-width: 100%;
        animation: float 4s ease-in-out infinite;
        z-index: 2;
        opacity: 0.98;
        border-radius: 8px;
        background: transparent;
        border: none;
        box-shadow: none;
        transform-origin: center;
        transition: transform 0.18s ease;
        margin-bottom: 0rem !important;
    }

    .bot:hover { transform: translateY(-6px) scale(1.02); }

    /* RUNNING FIGURE WITH DOCUMENT */
    .running-figure {
        position: absolute;
        right: 120px;
        top: 110px; /* Moved down from 100px */
        width: 280px;
        max-width: 70%;
        z-index: 1;
        opacity: 0.92;
        animation: runToward 3.5s ease-in-out infinite;
        transform-origin: center;
        transition: transform 0.18s ease;
        margin-bottom: 0rem !important;
    }

    .running-figure:hover { transform: scale(1.03); }

    @keyframes approach { 0% { transform: translateX(8px); } 50% { transform: translateX(0px); } 100% { transform: translateX(8px); } }

    @keyframes runToward { 0% { transform: translateX(-12px); } 50% { transform: translateX(2px); } 100% { transform: translateX(-12px); } }

    /* FEATURE CARD */
    .feature-card {
        padding: 1.5rem;
        border-radius: 14px;
        background: linear-gradient(180deg, #0f1724, #0b1220);
        border: 1px solid rgba(255,255,255,0.03);
        height: 100%;
        transition: transform 0.14s ease, box-shadow 0.14s ease;
    }

    .feature-card:hover { transform: translateY(-6px); box-shadow: 0 18px 40px rgba(2,6,23,0.6); }
    

    /* ABOUT */
    .about {
        background-color: #E5E7EB;
        padding: 1rem;
        border-radius: 16px;
        border: 1px solid #1F2937;
        margin-top: 2rem; /* Increased from 3rem */
    }
    .anchor {
    display: block;
    position: relative;
    top: -64px;   /* EXACT navbar height */
    visibility: hidden;
    }


    /* Responsive adjustments */
    @media (max-width: 900px) {
        .hero-title { font-size: 42px; }
        .hero-welcome { font-size: 24px; }
        .hero-brand { font-size: 34px; }
        .hero-desc { font-size: 16px; max-width: 100%; }
        .nav-right a { margin-left: 12px; font-size: 14px; }
        .navbar { padding: 0 1rem; }
        .bot { display: none; }
        .feature-card { margin-bottom: 1rem; }
        .stButton > button { padding: 0.6rem 1.2rem; }
        /* smaller left padding on medium screens, but still provide gutter */
        .hero { padding: 2rem 2.5rem 3rem 2.5rem; }
        .block-container { padding-left: 1.6rem; padding-right: 1.6rem; }
    }

    @media (max-width: 480px) {
        .hero-title { font-size: 28px; }
        .hero-welcome { font-size: 18px; }
        .hero-brand { font-size: 26px; }
        .nav-right { display: none; }
        .nav-left { font-size: 18px; }
        .feature-card h3 { font-size: 16px; }
        .hero { padding-left: 1rem; }
        .block-container { padding-left: 1rem; padding-right: 1rem; }
    }

    /* Metric cards for analyzer page */
    .metric-card {
        background: linear-gradient(180deg, #0f1724, #0b1220);
        padding: 1.5rem;
        border-radius: 10px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.3);
        border-left: 4px solid #6366F1;
        margin-bottom: 1rem;
    }
    
    .success-card {
        background: linear-gradient(180deg, #1a2e1a, #0f1f0f);
        border-left: 4px solid #34a853;
    }
    
    .warning-card {
        background: linear-gradient(180deg, #2e2a1a, #1f1b0f);
        border-left: 4px solid #fbbc04;
    }
    
    .danger-card {
        background: linear-gradient(180deg, #2e1a1a, #1f0f0f);
        border-left: 4px solid #ea4335;
    }

    /* File uploader styling */
    .stFileUploader {
        background: linear-gradient(180deg, #0f1724, #0b1220);
        border: 1px solid rgba(255,255,255,0.05);
        border-radius: 10px;
        padding: 1rem;
    }

    /* Tabs styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background-color: transparent;
    }

    .stTabs [data-baseweb="tab"] {
        background-color: #1a1f2e;
        border-radius: 8px 8px 0 0;
        color: #D1D5DB;
        padding: 12px 24px;
        font-weight: 500;
    }

    .stTabs [aria-selected="true"] {
        background: linear-gradient(90deg, #6366F1, #06B6D4);
        color: white;
    }

    /* Success/Warning/Error messages */
    .stSuccess, .stWarning, .stError, .stInfo {
        background: linear-gradient(180deg, #0f1724, #0b1220);
        border-radius: 8px;
        border-left-width: 4px;
    }

    /* Expander */
    .streamlit-expanderHeader {
        background: linear-gradient(180deg, #0f1724, #0b1220);
        border-radius: 8px;
        color: #FAFAFA;
    }

    /* START ANALYSIS BUTTON - FIXED STYLING */
    div[data-testid="column"]:has(button[kind="primary"]) button,
    button[key="analyze_btn"] {
        background: linear-gradient(90deg, #6366F1, #06B6D4) !important;
        color: white !important;
        height: 3.5rem !important;
        width: 100% !important;
        max-width: 600px !important;
        border-radius: 12px !important;
        font-size: 18px !important;
        font-weight: 700 !important;
        border: none !important;
        box-shadow: 0 10px 30px rgba(99,102,241,0.3) !important;
        transition: all 0.3s ease !important;
        margin-top: 1.5rem !important;
        margin-bottom: 2rem !important;
        letter-spacing: 1px !important;
    }

    div[data-testid="column"]:has(button[kind="primary"]) button:hover,
    button[key="analyze_btn"]:hover {
        background: linear-gradient(90deg, #5558E3, #0599B8) !important;
        transform: translateY(-3px) !important;
        box-shadow: 0 15px 40px rgba(99,102,241,0.4) !important;
    }

    div[data-testid="column"]:has(button[kind="primary"]) button:disabled,
    button[key="analyze_btn"]:disabled {
        background: linear-gradient(90deg, #4B5563, #6B7280) !important;
        opacity: 0.5 !important;
        cursor: not-allowed !important;
    }

    @media (max-width: 900px) {
        .navbar { padding: 0 1rem; }
        .block-container { padding-left: 1rem; padding-right: 1rem; }
        
        div[data-testid="column"]:has(button[kind="primary"]) button,
        button[key="analyze_btn"] {
            font-size: 16px !important;
            height: 3rem !important;
        }
    }
</style>
"""

# Import page modules
def landing_page():
    """Landing page content"""
    st.markdown(SHARED_CSS, unsafe_allow_html=True)
    
    # ---------------- NAVBAR ----------------
    st.markdown("""
    <div class="navbar">
        <div class="nav-left">🤖 AI Startup Analyzer</div>
        <div class="nav-right">
            <a href="#home">Home</a>
            <a href="#about">About</a>
            <a href="#login">Login</a>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ---------------- HERO SECTION ----------------
    col1, col2 = st.columns([1.5, 1])

    with col1:
        st.markdown('<div class="hero" id="home">', unsafe_allow_html=True)

        st.markdown(
            '<div class="hero-title"><span class="hero-welcome">Turn Decks Into Decision by —</span><span class="hero-brand"> AI Startup Analyzer</span></div>',
            unsafe_allow_html=True
        )

        st.markdown(
            '<div class="hero-desc">'
            'A smart AI system designed to analyze early-stage startups. '
            'Upload pitch decks, explore market benchmarks, and generate '
            'investor-ready insights — faster and smarter.'
            '</div>',
            unsafe_allow_html=True
        )
        if st.button("🚀 Start Evaluating Startup Potential Now →"):
            with st.status("Go and upload decks...", expanded=False):
                ss.current_page = "analyzer"
                st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class="illustration-container">
            <img class="bot" src="https://cdn-icons-png.flaticon.com/512/4712/4712109.png">
            <img class="running-figure" src="https://cdn-icons-png.flaticon.com/512/2389/2389652.png">
        </div>
        """, unsafe_allow_html=True)


    # ---------------- FEATURES ----------------
    st.markdown(
        "<h3 style='margin-top:0.8rem; margin-bottom:1rem;'>✨ What You Can Do</h3>",
        unsafe_allow_html=True
    )

    f1, f2, f3 = st.columns(3)

    with f1:
        st.markdown("""
        <div class="feature-card">
            <h3>📄 Document Intelligence</h3>
            <p>Automatically extract insights from pitch decks, PDFs, and reports.</p>
        </div>
        """, unsafe_allow_html=True)

    with f2:
        st.markdown("""
        <div class="feature-card">
            <h3>🌍 Market Benchmarking</h3>
            <p>Analyze startups across regions, sectors, and competitive landscapes.</p>
        </div>
        """, unsafe_allow_html=True)

    with f3:
        st.markdown("""
        <div class="feature-card">
            <h3>🤖 AI-Generated Reports</h3>
            <p>Get structured summaries, risks, and growth opportunities instantly.</p>
        </div>
        """, unsafe_allow_html=True)

    # ---------------- ABOUT SECTION ----------------

    st.markdown("""
    <div id="about" class="anchor"></div>

    <div class="feature-card about">
        <h1>About</h1>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("## Empowering Smarter Startup Decisions with AI-Powered Startup Analyst")

    # First row of cards
    c1, c2, c3 = st.columns(3)

    with c1:
        st.markdown("""
        <div class="feature-card">
            <h3>🤖 Multi-Agent Intelligence</h3>
            <p>Specialized AI agents handle parsing, analysis, and report generation seamlessly.</p>
        </div>
        """, unsafe_allow_html=True)

    with c2:
        st.markdown("""
        <div class="feature-card">
            <h3>💡 RAG-Powered Insights</h3>
            <p>Combines uploaded documents and external data for context-aware recommendations.</p>
        </div>
        """, unsafe_allow_html=True)

    with c3:
        st.markdown("""
        <div class="feature-card">
            <h3>📊 Interactive Dashboard</h3>
            <p>Visualize KPIs, metrics, and trends in real-time with a sleek dashboard.</p>
        </div>
        """, unsafe_allow_html=True)

    # Second row of cards
    c4, c5 = st.columns(2)

    with c4:
        st.markdown("""
        <div class="feature-card">
            <h3>📧 Automated Reports</h3>
            <p>Professional summaries including SWOT, risk, and growth potential.</p>
        </div>
        """, unsafe_allow_html=True)

    with c5:
        st.markdown("""
        <div class="feature-card">
            <h3>⚡ Reliable & Scalable</h3>
            <p>Built with Python, LangChain, and OpenAI for scalable and accurate results.</p>
        </div>
        """, unsafe_allow_html=True)

    # Bottom paragraph
    st.markdown("""
    <p style='margin-top:2rem; font-size:16px;'>
    AI Startup Analyzer reduces analysis time from hours to minutes, providing 
    <strong>accurate, unbiased, and actionable insights</strong> for investors, founders, and analysts.
    </p>
    """, unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

    # ---------------- FOOTER ----------------
    st.markdown(
        """
        <hr style="margin-top:50px;">
        <p style="text-align:center; color:#9CA3AF;">
        Built with ❤️ using Streamlit & LangChain
        </p>
        """,
        unsafe_allow_html=True
    )



def analyzer_page():
    """Main analyzer page"""
    import os
    import uuid
    import json
    from datetime import datetime
    import plotly.graph_objects as go
    import plotly.express as px
    from services.document_processor import DocumentProcessor
    from services.rag_system import RAGSystem
    from services.agent_orchestrator import AgentOrchestrator
    from services.professional_report_generator import ProfessionalReportGenerator
    from services.gmail_sender import GmailSender
    
    st.markdown(SHARED_CSS, unsafe_allow_html=True)
    
    # Navbar with Back button - FIXED with Streamlit button
    col_nav1, col_nav2 = st.columns([6, 1])
    
    with col_nav1:
        st.markdown("""
        <div style="padding: 1rem 0 0 1rem;">
            <span style="font-size: 20px; font-weight: 700; color: #0E1117;">🤖 AI Startup Analyzer</span>
        </div>
        """, unsafe_allow_html=True)
    
    with col_nav2:
        if st.button("← Back to Home", key="back_to_home"):
            ss.current_page = 'landing'
            st.rerun()
    
    st.markdown("<br>", unsafe_allow_html=True)

     # Main tabs
    tab1, tab2, tab3 = st.tabs(["📤 Upload & Analyze", "📊 Analysis Results", "📈 Advanced Insights"])
    
    # Initialize session state
    if 'analysis_results' not in ss:
        ss.analysis_results = None
    if 'startup_id' not in ss:
        ss.startup_id = None
    
       
    # ---------------- TAB 1: UPLOAD & ANALYZE ----------------
    with tab1:
        # Page Header
        header_container = st.container()

        with header_container:
            # Create two columns: one for text (85%) and one for the time box (15%)
            col1, col2 = st.columns([5, 1], vertical_alignment="bottom")

            with col1:
                st.markdown("""
                    <h2 style="margin:0;">📤 Upload Startup Documents</h2>
                    <p style="color:#9CA3AF; margin-top:0.4rem;">
                        Securely upload documents to generate an AI-powered startup evaluation
                    </p>
                """, unsafe_allow_html=True)

            with col2:
                # We use a small amount of HTML here just to style the box background
                st.markdown("""
                    <div style="
                        background-color: #1F2937;
                        padding: 8px 12px;
                        border-radius: 8px;
                        border: 1px solid #374151;
                        text-align: center;
                        font-size: 0.8rem;
                        color: #E5E7EB;
                        white-space: nowrap;
                        margin-bottom: 15px;">
                        ⏱ Estimated time: 2–3 minutes
                    </div>
                """, unsafe_allow_html=True)
    
    # This adds the horizontal line across the whole width
        st.markdown('<hr style="margin: 0 0 2rem 0; border: 0; border-top: 1px solid #1F2937;">', unsafe_allow_html=True)

        # Main layout
        left, right = st.columns([3, 2], gap="large")

        # ---------- LEFT: Pitch Deck ----------
        with left:
            st.markdown("### 📌 Pitch Deck")
            st.markdown(
                "<p style='color:#9CA3AF;'>Primary document used for core analysis</p>",
                unsafe_allow_html=True
            )
            st.markdown("""
                    <style>
                        /* Targets the text label of the file uploader */
                        .stFileUploader label p {
                            color: white !important;
                        }
                    </style>
                """, unsafe_allow_html=True)

            pitch_deck = st.file_uploader(
                "Upload Pitch Deck (PDF only)",
                type=["pdf"],
                key="pitch_deck"
            )

            if pitch_deck:
                st.success(f"✅ {pitch_deck.name} uploaded successfully")

            st.markdown("<br>", unsafe_allow_html=True)

           

        # ---------- RIGHT: Optional Docs ----------
        with right:
            st.markdown("### 🔎 Supporting Documents")
            st.markdown(
                "<p style='color:#9CA3AF;'>Optional but improves depth & accuracy</p>",
                unsafe_allow_html=True
            )

            with st.expander("📞 Call Transcripts"):
                transcripts = st.file_uploader(
                    "Upload transcripts",
                    type=["txt", "docx", "pdf"],
                    accept_multiple_files=True,
                    key="transcripts"
                )
                if transcripts:
                    for t in transcripts:
                        st.success(f"✅ {t.name}")

            with st.expander("📧 Email Threads"):
                emails = st.file_uploader(
                    "Upload email communications",
                    type=["txt", "docx"],
                    accept_multiple_files=True,
                    key="emails"
                )
                if emails:
                    for e in emails:
                        st.success(f"✅ {e.name}")

            with st.expander("📝 Founder Updates"):
                updates = st.file_uploader(
                    "Upload founder updates",
                    type=["txt", "docx", "pdf"],
                    accept_multiple_files=True,
                    key="updates"
                )
                if updates:
                    for u in updates:
                        st.success(f"✅ {u.name}")

        # Analyze button - FIXED with centered container
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Center the button using columns
        col_btn1, col_btn2, col_btn3 = st.columns([1, 2, 1])
        
        with col_btn2:
            if st.button("🚀 START ANALYSIS", disabled=not pitch_deck, key="analyze_btn", type="primary", use_container_width=True):
                with st.spinner("🔄 Processing documents and running AI analysis..."):
                    try:
                        # Initialize systems
                        processor = DocumentProcessor()
                        rag = RAGSystem()
                        orchestrator = AgentOrchestrator(rag)
                        
                        # Generate unique ID
                        startup_id = str(uuid.uuid4())
                        ss.startup_id = startup_id
                        
                        # Progress tracking
                        progress_bar = st.progress(0)
                        status_text = st.empty()
                        
                        # Step 1: Process documents
                        status_text.text("📄 Processing documents...")
                        progress_bar.progress(10)
                        
                        uploaded_files = {
                            'pitch_deck': pitch_deck,
                            'transcripts': transcripts if transcripts else [],
                            'emails': emails if emails else [],
                            'updates': updates if updates else []
                        }
                        
                        extracted_data = processor.process_uploaded_files(uploaded_files)
                        progress_bar.progress(25)
                        
                        # Step 2: Add to RAG
                        status_text.text("🧠 Building knowledge base...")
                        rag.add_documents(extracted_data, startup_id)
                        progress_bar.progress(40)
                        
                        # Step 3: Run agents
                        status_text.text("🤖 Running AI agents...")
                        
                        # Simulate agent progress
                        for i in range(1, 7):
                            progress_bar.progress(40 + (i * 10))
                        
                        # Run analysis
                        results = orchestrator.analyze_startup(startup_id)
                        
                        # Store results
                        ss.analysis_results = results
                        
                        progress_bar.progress(100)
                        status_text.text("✅ Analysis complete!")
                        
                        st.success("🎉 Analysis complete! Check the **Analysis Results** tab.")
                        
                    except Exception as e:
                        st.error(f"❌ Error during analysis: {str(e)}")
                        st.exception(e)
                    
        # ---------- ANALYSIS SUMMARY (FULL WIDTH BOTTOM) ----------
        st.markdown("<br><br>", unsafe_allow_html=True)

        st.markdown("""
        <div style="
            background: #0B1220;
            border: 1px solid #1F2937;
            border-radius: 16px;
            padding: 1.5rem;">
            <h4 style="margin-top:0;">📊 Analysis Workflow</h4>
            <ul style="color:#D1D5DB; line-height:1.8;">
                <li>📄 Documents parsed using LangChain</li>
                <li>🧠 Embedded & stored in vector database</li>
                <li>🤖 6 AI agents analyze in parallel</li>
                <li>🔒 Investment-grade report generated</li>
            </ul>
        
        </div>
        """, unsafe_allow_html=True)
    
    # TAB 2: RESULTS
    with tab2:
        if ss.analysis_results is None:
            st.info("📤 Upload documents in the first tab to start analysis")
        else:
            results = ss.analysis_results
            company_info = results['extracted_data']['company_info']
            recommendation = results['recommendation']
            risk_analysis = results['risk_analysis']
            benchmark_data = results.get('benchmark_data', {})
            growth_assessment = results.get('growth_assessment', {})
            
            st.markdown(f"## 🏢 {company_info['name']}")
            
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("Sector", company_info['sector'])
            with col2:
                st.metric("Stage", company_info['stage'])
            with col3:
                st.metric("Location", company_info['location'])
            with col4:
                founded = company_info.get('founded_year', 'N/A')
                st.metric("Founded", founded if founded else "N/A")
            
            st.divider()
            
            # Decision Card
            decision = recommendation['decision']
            confidence = recommendation['confidence']
            
            if decision == "INVEST":
                card_class = "success-card"
                emoji = "✅"
                color = "#34a853"
            elif decision == "MAYBE":
                card_class = "warning-card"
                emoji = "⚠️"
                color = "#fbbc04"
            else:
                card_class = "danger-card"
                emoji = "❌"
                color = "#ea4335"
            
            st.markdown(f"""
            <div class="metric-card {card_class}">
                <h2>{emoji} Investment Decision: {decision}</h2>
                <p style="font-size: 1.2rem;">Confidence: <strong>{confidence}%</strong></p>
                <p style="font-size: 1.1rem; margin-top: 1rem;">{recommendation['investment_thesis']}</p>
            </div>
            """, unsafe_allow_html=True)
            
            st.divider()
            
            # KEY METRICS
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.markdown("### 📊 Deal Score")
                fig = go.Figure(go.Indicator(
                    mode="gauge+number",
                    value=recommendation['deal_score'],
                    domain={'x': [0, 1], 'y': [0, 1]},
                    gauge={
                        'axis': {'range': [None, 100]},
                        'bar': {'color': color},
                        'steps': [
                            {'range': [0, 40], 'color': "#2e1a1a"},
                            {'range': [40, 65], 'color': "#2e2a1a"},
                            {'range': [65, 100], 'color': "#1a2e1a"}
                        ],
                        'threshold': {
                            'line': {'color': "red", 'width': 4},
                            'thickness': 0.75,
                            'value': 65
                        }
                    }
                ))
                fig.update_layout(
                    height=200, 
                    margin=dict(l=20, r=20, t=20, b=20),
                    paper_bgcolor='rgba(0,0,0,0)',
                    font=dict(color='#D1D5DB')
                )
                st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                st.markdown("### 🚨 Risk Score")
                risk_score = risk_analysis.get('risk_score', 50)
                fig = go.Figure(go.Indicator(
                    mode="gauge+number",
                    value=risk_score,
                    domain={'x': [0, 1], 'y': [0, 1]},
                    gauge={
                        'axis': {'range': [None, 100]},
                        'bar': {'color': "#ea4335" if risk_score > 70 else "#fbbc04" if risk_score > 40 else "#34a853"},
                        'steps': [
                            {'range': [0, 40], 'color': "#1a2e1a"},
                            {'range': [40, 70], 'color': "#2e2a1a"},
                            {'range': [70, 100], 'color': "#2e1a1a"}
                        ]
                    }
                ))
                fig.update_layout(
                    height=200, 
                    margin=dict(l=20, r=20, t=20, b=20),
                    paper_bgcolor='rgba(0,0,0,0)',
                    font=dict(color='#D1D5DB')
                )
                st.plotly_chart(fig, use_container_width=True)
            
            with col3:
                st.markdown("### 📈 Growth Score")
                growth_score = growth_assessment.get('overall_growth_score', 5) * 10
                fig = go.Figure(go.Indicator(
                    mode="gauge+number",
                    value=growth_score,
                    domain={'x': [0, 1], 'y': [0, 1]},
                    gauge={
                        'axis': {'range': [None, 100]},
                        'bar': {'color': "#6366F1"},
                        'steps': [
                            {'range': [0, 40], 'color': "#2e1a1a"},
                            {'range': [40, 70], 'color': "#2e2a1a"},
                            {'range': [70, 100], 'color': "#1a2e1a"}
                        ]
                    }
                ))
                fig.update_layout(
                    height=200, 
                    margin=dict(l=20, r=20, t=20, b=20),
                    paper_bgcolor='rgba(0,0,0,0)',
                    font=dict(color='#D1D5DB')
                )
                st.plotly_chart(fig, use_container_width=True)
            
            with col4:
                st.markdown("### 🎯 Benchmark Score")
                benchmark_score = benchmark_data.get('benchmark_score', 50)
                fig = go.Figure(go.Indicator(
                    mode="gauge+number",
                    value=benchmark_score,
                    domain={'x': [0, 1], 'y': [0, 1]},
                    gauge={
                        'axis': {'range': [None, 100]},
                        'bar': {'color': "#34a853"},
                        'steps': [
                            {'range': [0, 40], 'color': "#2e1a1a"},
                            {'range': [40, 60], 'color': "#2e2a1a"},
                            {'range': [60, 100], 'color': "#1a2e1a"}
                        ]
                    }
                ))
                fig.update_layout(
                    height=200, 
                    margin=dict(l=20, r=20, t=20, b=20),
                    paper_bgcolor='rgba(0,0,0,0)',
                    font=dict(color='#D1D5DB')
                )
                st.plotly_chart(fig, use_container_width=True)
            
            st.divider()
            
            # Strengths & Concerns
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("### ✅ Key Strengths")
                for strength in recommendation['key_strengths']:
                    st.success(f"**{strength}**")
            
            with col2:
                st.markdown("### ⚠️ Key Concerns")
                for concern in recommendation['key_concerns']:
                    st.warning(f"**{concern}**")
            
            st.divider()
            
            # RED FLAGS
            if risk_analysis['red_flags']:
                st.markdown("### 🚨 Red Flags Detected")
                
                for flag in risk_analysis['red_flags']:
                    severity = flag['severity']
                    
                    if severity == "CRITICAL":
                        color = "#ea4335"
                        icon = "🔴"
                    elif severity == "HIGH":
                        color = "#fbbc04"
                        icon = "🟠"
                    elif severity == "MEDIUM":
                        color = "#4285f4"
                        icon = "🟡"
                    else:
                        color = "#5f6368"
                        icon = "⚪"
                    
                    with st.expander(f"{icon} **{severity}**: {flag['title']}"):
                        st.markdown(f"**Description:** {flag['description']}")
                        st.markdown(f"**Impact:** {flag['impact']}")
                        if flag.get('evidence'):
                            st.markdown("**Evidence:**")
                            for evidence in flag['evidence']:
                                st.markdown(f"- {evidence}")
            else:
                st.success("✅ No major red flags detected!")
            
            st.divider()
            
            # FOLLOW-UP QUESTIONS
            st.markdown("### 💡 Suggested Follow-up Questions")
            for i, question in enumerate(recommendation['follow_up_questions'], 1):
                st.info(f"**{i}.** {question}")
            
            st.divider()
            
            # EXPORT OPTIONS
            st.markdown("### 📥 Export Report")
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                # Download JSON
                json_str = json.dumps(results, indent=2, default=str)
                st.download_button(
                    label="📄 Download JSON",
                    data=json_str,
                    file_name=f"analysis_{company_info['name']}_{datetime.now().strftime('%Y%m%d')}.json",
                    mime="application/json",
                    type="primary"
                )
            
            with col2:
                # Download summary text
                summary = f"""
STARTUP ANALYSIS REPORT
{'='*50}

Company: {company_info['name']}
Sector: {company_info['sector']}
Stage: {company_info['stage']}

RECOMMENDATION: {decision}
Confidence: {confidence}%
Deal Score: {recommendation['deal_score']}/100

INVESTMENT THESIS:
{recommendation['investment_thesis']}

KEY STRENGTHS:
{chr(10).join(f'- {s}' for s in recommendation['key_strengths'])}

KEY CONCERNS:
{chr(10).join(f'- {c}' for c in recommendation['key_concerns'])}

RED FLAGS: {len(risk_analysis['red_flags'])}
Risk Score: {risk_analysis['risk_score']}/100

Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
"""
                st.download_button(
                    label="📝 Download Summary",
                    data=summary,
                    file_name=f"summary_{company_info['name']}_{datetime.now().strftime('%Y%m%d')}.txt",
                    mime="text/plain",
                    type="primary"
                )
            
            st.divider()
            
            # ============================================================
            # PROFESSIONAL PDF REPORT & EMAIL SECTION
            # ============================================================
            
            st.markdown("### 📄 Professional PDF Report with Charts")
            
            col1, col2 = st.columns([1, 1])
            
            with col1:
                st.info("""
                **Professional Report Includes:**
                
                ✅ Executive Summary with Decision
                
                📊 Growth Dimension Radar Chart
                
                📈 Multi-Score Comparison Charts
                
                🚨 Detailed Risk Analysis
                
                💡 Evidence-Based Insights
                
                ❓ Follow-up Questions
                
                🎯 Recommended Next Steps
                """)
            
            with col2:
                # Generate PDF button
                if st.button("📄 Generate Professional PDF Report", key="gen_pdf"):
                    with st.spinner("🎨 Creating professional report with charts..."):
                        try:
                            # Create reports directory
                            os.makedirs("reports", exist_ok=True)
                            
                            # Generate filename
                            pdf_filename = f"investment_report_{company_info['name'].replace(' ', '_')}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
                            pdf_path = os.path.join("reports", pdf_filename)
                            
                            # Generate report
                            report_generator = ProfessionalReportGenerator()
                            generated_path = report_generator.generate_report(results, pdf_path)
                            
                            # Store in session state
                            ss['pdf_path'] = generated_path
                            ss['pdf_filename'] = pdf_filename
                            
                            st.success(f"✅ Professional PDF report generated successfully!")
                            st.balloons()
                            
                        except Exception as e:
                            st.error(f"❌ Error generating PDF: {str(e)}")
                            st.exception(e)
            
            # Show download button if PDF exists
            if 'pdf_path' in ss and os.path.exists(ss['pdf_path']):
                
                st.success(f"✅ Report ready: **{ss['pdf_filename']}**")
                
                # Download button
                with open(ss['pdf_path'], 'rb') as pdf_file:
                    pdf_data = pdf_file.read()
                    
                    st.download_button(
                        label="⬇️ Download PDF Report",
                        data=pdf_data,
                        file_name=ss['pdf_filename'],
                        mime="application/pdf",
                        key="download_pdf",
                        type="primary"
                    )
                
                st.divider()
                
                # ============================================================
                # EMAIL SECTION
                # ============================================================
                st.markdown("""
                <style>
                /* Make all text visible */
                .stTextInput label, .stTextArea label {
                    color: white !important;
                }
                
                /* Expander headers */
                .streamlit-expanderHeader {
                    color: white !important;
                }
                
                /* Section headers */
                h3, h2, h1 {
                    color: white !important;
                }
                
                /* Help text */
                .stTextInput small, .stTextArea small {
                    color: #cccccc !important;
                }
                
                /* Markdown text in expanders */
                .stMarkdown p, .stMarkdown strong {
                    color: white !important;
                }
                </style>
                """, unsafe_allow_html=True)

                
                st.markdown("### 📧 Send Report to Investors via Gmail")
                
                # Single recipient
                with st.expander("📨 Send to Single Investor", expanded=True):
                    investor_email = st.text_input(
                        "Investor Email Address",
                        placeholder="investor@example.com",
                        help="Enter the email address of the investor",
                        key="single_email"
                    )
                    
                    email_subject = st.text_input(
                        "Email Subject (Optional)",
                        value=f"Investment Analysis: {company_info['name']} - {recommendation['decision']}",
                        key="email_subject"
                    )
                    
                    col_send1, col_send2 = st.columns([1, 2])
                    
                    with col_send1:
                        if st.button("📧 Send Email", disabled=not investor_email, key="send_single"):
                            with st.spinner("📨 Sending email via Gmail..."):
                                try:
                                    gmail_sender = GmailSender()
                                    
                                    success = gmail_sender.send_report(
                                        recipient_email=investor_email,
                                        subject=email_subject,
                                        company_name=company_info['name'],
                                        decision=recommendation['decision'],
                                        pdf_path=ss['pdf_path']
                                    )
                                    
                                    if success:
                                        st.success(f"✅ Report sent successfully to **{investor_email}**")
                                        st.balloons()
                                    else:
                                        st.error("❌ Failed to send email. Check console for details.")
                                        
                                except FileNotFoundError as e:
                                    st.error(str(e))
                                    st.info("💡 Please configure Gmail credentials in environment variables")
                                except Exception as e:
                                    st.error(f"❌ Error: {str(e)}")
                                    st.exception(e)
                
                # Multiple recipients
                with st.expander("📨 Send to Multiple Investors"):
                    st.markdown("**Enter email addresses (one per line):**")
                    
                    bulk_emails = st.text_area(
                        "Investor Email List",
                        placeholder="investor1@example.com\ninvestor2@example.com\ninvestor3@example.com",
                        height=150,
                        key="bulk_emails"
                    )
                    
                    if st.button("📧 Send to All", disabled=not bulk_emails, key="send_bulk"):
                        with st.spinner("📨 Sending emails..."):
                            try:
                                # Parse emails
                                email_list = [email.strip() for email in bulk_emails.split('\n') if email.strip()]
                                
                                if not email_list:
                                    st.warning("⚠️ No valid email addresses found")
                                else:
                                    st.info(f"Sending to {len(email_list)} recipients...")
                                    
                                    gmail_sender = GmailSender()
                                    
                                    results_bulk = gmail_sender.send_bulk_reports(
                                        recipient_list=email_list,
                                        subject=email_subject,
                                        company_name=company_info['name'],
                                        decision=recommendation['decision'],
                                        pdf_path=ss['pdf_path']
                                    )
                                    
                                    # Show results
                                    col_r1, col_r2 = st.columns(2)
                                    
                                    with col_r1:
                                        st.metric("✅ Successfully Sent", results_bulk['success'])
                                    
                                    with col_r2:
                                        st.metric("❌ Failed", results_bulk['failed'])
                                    
                                    if results_bulk['failed'] > 0:
                                        st.warning(f"Failed emails: {', '.join(results_bulk['failed_emails'])}")
                                    else:
                                        st.success("🎉 All emails sent successfully!")
                                        st.balloons()
                                        
                            except Exception as e:
                                st.error(f"❌ Error: {str(e)}")
                                st.exception(e)
                
                st.divider()
                
                # Email preview
                with st.expander("👀 Preview Email Content"):
                    if recommendation['decision'] == "INVEST":
                        preview_color = "#34a853"
                        preview_emoji = "✅"
                    elif recommendation['decision'] == "MAYBE":
                        preview_color = "#fbbc04"
                        preview_emoji = "⚠️"
                    else:
                        preview_color = "#ea4335"
                        preview_emoji = "❌"
                    
                    st.markdown(f"""
                    **Subject:** {email_subject}
                    
                    **Body Preview:**
                    
                    ---
                    
                    Dear Investor,
                    
                    Our AI-powered multi-agent analysis system has completed a comprehensive evaluation of **{company_info['name']}**.
                    
                    **{preview_emoji} Investment Decision: {recommendation['decision']}**
                    
                    **Report Highlights:**
                    - Executive Summary with key metrics
                    - Growth Analysis with radar charts
                    - Risk Assessment with red flags
                    - Market Validation research
                    - Follow-up questions and next steps
                    
                    Please find the detailed PDF report attached.
                    
                    ---
                    
                    *Professional HTML email will be sent with charts and styling*
                    """)
            
            else:
                st.warning("⚠️ Generate the PDF report first using the button above")
    
    # TAB 3: ADVANCED INSIGHTS
    with tab3:
        if ss.analysis_results is None:
            st.info("📤 Upload documents in the first tab to start analysis")
        else:
            results = ss.analysis_results
            growth_assessment = results.get('growth_assessment', {})
            benchmark_data = results.get('benchmark_data', {})
            
            st.header("📈 Advanced Insights")
            
            # Growth Dimensions Radar Chart
            st.subheader("🎯 Growth Dimension Scores")
            
            growth_scores = growth_assessment.get('growth_scores', {})
            
            categories = ['Market<br>Opportunity', 'Competitive<br>Moat', 'Product<br>Innovation', 
                         'Scalability', 'Team<br>Execution']
            values = [
                growth_scores.get('market_opportunity', {}).get('score', 5),
                growth_scores.get('competitive_moat', {}).get('score', 5),
                growth_scores.get('product_innovation', {}).get('score', 5),
                growth_scores.get('scalability', {}).get('score', 5),
                growth_scores.get('team_execution', {}).get('score', 5)
            ]
            
            fig = go.Figure()
            
            fig.add_trace(go.Scatterpolar(
                r=values,
                theta=categories,
                fill='toself',
                name='Startup Score',
                line=dict(color='#6366F1', width=2),
                fillcolor='rgba(99, 102, 241, 0.3)'
            ))
            
            fig.add_trace(go.Scatterpolar(
                r=[7, 7, 7, 7, 7],
                theta=categories,
                fill='toself',
                name='Target Score',
                line=dict(color='#06B6D4', width=1, dash='dash'),
                fillcolor='rgba(6, 182, 212, 0.1)'
            ))
            
            fig.update_layout(
                polar=dict(
                    radialaxis=dict(
                        visible=True,
                        range=[0, 10],
                        gridcolor='rgba(255,255,255,0.1)',
                        tickfont=dict(color='#D1D5DB')
                    ),
                    angularaxis=dict(
                        gridcolor='rgba(255,255,255,0.1)',
                        tickfont=dict(color='#D1D5DB')
                    ),
                    bgcolor='rgba(0,0,0,0)'
                ),
                showlegend=True,
                height=500,
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                font=dict(color='#D1D5DB'),
                legend=dict(
                    font=dict(color='#D1D5DB'),
                    bgcolor='rgba(15, 23, 36, 0.8)'
                )
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
            st.divider()
            
            # Detailed breakdowns
            col1, col2 = st.columns(2)
            
            with col1:
                st.subheader("📊 Benchmarking Details")
                
                comparisons = benchmark_data.get('comparisons', {})
                
                if comparisons:
                    for metric, data in comparisons.items():
                        if isinstance(data, dict):
                            status = data.get('status', 'Unknown')
                            startup_val = data.get('startup_value', 'Unknown')
                            sector_avg = data.get('sector_average', 'Unknown')
                            
                            with st.expander(f"**{metric.replace('_', ' ').title()}**"):
                                col_a, col_b = st.columns(2)
                                with col_a:
                                    st.metric("Startup Value", startup_val)
                                with col_b:
                                    st.metric("Sector Average", sector_avg)
                                
                                if status == "Above Average":
                                    st.success(f"✅ Status: {status}")
                                elif status == "Below Average":
                                    st.warning(f"⚠️ Status: {status}")
                                else:
                                    st.info(f"ℹ️ Status: {status}")
                                
                                if 'notes' in data and data['notes']:
                                    st.markdown(f"**Notes:** {data['notes']}")
                else:
                    st.info("No benchmarking data available")
            
            with col2:
                st.subheader("🚀 Growth Potential Details")
                
                if growth_scores:
                    for dimension, data in growth_scores.items():
                        if isinstance(data, dict):
                            score = data.get('score', 0)
                            
                            # Color code based on score
                            if score >= 7:
                                score_color = "🟢"
                            elif score >= 5:
                                score_color = "🟡"
                            else:
                                score_color = "🔴"
                            
                            with st.expander(f"{score_color} **{dimension.replace('_', ' ').title()}** - Score: {score}/10"):
                                st.progress(score / 10)
                                st.markdown(f"**Reasoning:** {data.get('reasoning', 'N/A')}")
                                
                                if 'evidence' in data and data['evidence']:
                                    st.markdown("**Evidence:**")
                                    for evidence in data['evidence']:
                                        st.markdown(f"- {evidence}")
                else:
                    st.info("No growth assessment data available")
            
            st.divider()
            
            # Market validation
            st.subheader("🌍 Market Validation")
            
            market_research = results.get('market_research', {})
            validations = market_research.get('validations', {})
            
            if validations:
                val_cols = st.columns(2)
                
                for idx, (val_type, val_data) in enumerate(validations.items()):
                    if isinstance(val_data, dict):
                        with val_cols[idx % 2]:
                            with st.expander(f"**{val_type.replace('_', ' ').title()}**"):
                                claimed = val_data.get('claimed', 'N/A')
                                found = val_data.get('found', 'N/A')
                                status = val_data.get('status', 'N/A')
                                notes = val_data.get('notes', 'N/A')
                                
                                st.markdown(f"**Claimed:** {claimed}")
                                st.markdown(f"**Found:** {found}")
                                
                                if status == "Verified":
                                    st.success(f"✅ Status: {status}")
                                elif status == "Unverified":
                                    st.warning(f"⚠️ Status: {status}")
                                else:
                                    st.info(f"ℹ️ Status: {status}")
                                
                                st.markdown(f"**Notes:** {notes}")
            else:
                st.info("No market validation data available")
            
            st.divider()
            
            # Risk Distribution Chart
            st.subheader("🚨 Risk Distribution")
            
            risk_analysis = results.get('risk_analysis', {})
            red_flags = risk_analysis.get('red_flags', [])
            
            if red_flags:
                # Count by severity
                severity_counts = {'CRITICAL': 0, 'HIGH': 0, 'MEDIUM': 0, 'LOW': 0}
                for flag in red_flags:
                    severity = flag.get('severity', 'LOW')
                    severity_counts[severity] = severity_counts.get(severity, 0) + 1
                
                fig_risk = go.Figure(data=[
                    go.Bar(
                        x=list(severity_counts.keys()),
                        y=list(severity_counts.values()),
                        marker=dict(
                            color=['#ea4335', '#fbbc04', '#4285f4', '#34a853'],
                            line=dict(color='rgba(255,255,255,0.1)', width=1)
                        ),
                        text=list(severity_counts.values()),
                        textposition='auto',
                    )
                ])
                
                fig_risk.update_layout(
                    title="Risk Flags by Severity",
                    xaxis_title="Severity Level",
                    yaxis_title="Number of Flags",
                    height=400,
                    paper_bgcolor='rgba(0,0,0,0)',
                    plot_bgcolor='rgba(0,0,0,0)',
                    font=dict(color='#D1D5DB'),
                    xaxis=dict(
                        gridcolor='rgba(255,255,255,0.1)',
                        tickfont=dict(color='#D1D5DB')
                    ),
                    yaxis=dict(
                        gridcolor='rgba(255,255,255,0.1)',
                        tickfont=dict(color='#D1D5DB')
                    )
                )
                
                st.plotly_chart(fig_risk, use_container_width=True)
            else:
                st.success("✅ No significant risks detected!")
            
            st.divider()
            
            # Score Comparison Chart
            st.subheader("📊 Multi-Dimensional Score Comparison")
            
            scores_data = {
                'Deal Score': results['recommendation'].get('deal_score', 0),
                'Growth Score': growth_assessment.get('overall_growth_score', 5) * 10,
                'Risk Score': 100 - risk_analysis.get('risk_score', 50),  # Inverted for better visualization
                'Benchmark Score': benchmark_data.get('benchmark_score', 50)
            }
            
            fig_scores = go.Figure(data=[
                go.Bar(
                    x=list(scores_data.keys()),
                    y=list(scores_data.values()),
                    marker=dict(
                        color=['#6366F1', '#06B6D4', '#34a853', '#fbbc04'],
                        line=dict(color='rgba(255,255,255,0.1)', width=1)
                    ),
                    text=[f"{v:.1f}" for v in scores_data.values()],
                    textposition='auto',
                )
            ])
            
            fig_scores.update_layout(
                title="Comparative Score Analysis (out of 100)",
                xaxis_title="Score Category",
                yaxis_title="Score Value",
                height=400,
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                font=dict(color='#D1D5DB'),
                xaxis=dict(
                    gridcolor='rgba(255,255,255,0.1)',
                    tickfont=dict(color='#D1D5DB')
                ),
                yaxis=dict(
                    range=[0, 100],
                    gridcolor='rgba(255,255,255,0.1)',
                    tickfont=dict(color='#D1D5DB')
                )
            )
            
            st.plotly_chart(fig_scores, use_container_width=True)
    
    # Footer
    st.divider()
    st.markdown("""
    <div style='text-align: center; color: #9CA3AF; padding: 2rem;'>
        <p>🚀 <strong>AI Startup Analyzer</strong> | Powered by Google Cloud & Gemini 2.0</p>
        <p>Built with Streamlit • LangChain • ChromaDB • Multi-Agent AI System</p>
    </div>
    """, unsafe_allow_html=True)


# ============================================================
# MAIN ROUTING LOGIC
# ============================================================

if ss.current_page == 'landing':
    landing_page()
else:
    analyzer_page()
