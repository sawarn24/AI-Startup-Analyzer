import streamlit as st
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
if not os.path.exists('/tmp/credentials.json'):  # ✅ Check /tmp
    credentials = {
        "installed": {
            "client_id": os.environ.get('GMAIL_CLIENT_ID'),
            "client_secret": os.environ.get('GMAIL_CLIENT_SECRET'),
            "project_id": "hack-482015",
            "auth_uri": "https://accounts.google.com/o/oauth2/auth",
            "token_uri": "https://oauth2.googleapis.com/token",
            "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
            "redirect_uris": ["http://localhost"]
        }
    }
    
    with open('/tmp/credentials.json', 'w') as f:  # ✅ Write to /tmp
        json.dump(credentials, f)

# Page config
st.set_page_config(
    page_title="AI Startup Analyzer",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        background: linear-gradient(90deg, #4285f4, #34a853, #fbbc04, #ea4335);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        padding: 1rem;
    }
    
    .sub-header {
        text-align: center;
        color: #5f6368;
        font-size: 1.2rem;
        margin-bottom: 2rem;
    }
    
    .metric-card {
        background: white;
        padding: 1.5rem;
        border-radius: 10px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        border-left: 4px solid #4285f4;
    }
    
    .success-card {
        background: #e6f4ea;
        border-left: 4px solid #34a853;
    }
    
    .warning-card {
        background: #fef7e0;
        border-left: 4px solid #fbbc04;
    }
    
    .danger-card {
        background: #fce8e6;
        border-left: 4px solid #ea4335;
    }
    
    .agent-status {
        padding: 0.5rem 1rem;
        border-radius: 20px;
        font-weight: bold;
        display: inline-block;
        margin: 0.5rem;
    }
    
    .status-complete {
        background: #e6f4ea;
        color: #1e8e3e;
    }
    
    .status-processing {
        background: #fef7e0;
        color: #f9ab00;
    }
    
    .stButton>button {
        width: 100%;
        background: linear-gradient(90deg, #4285f4, #34a853);
        color: white;
        font-size: 1.1rem;
        padding: 0.75rem;
        border-radius: 10px;
        border: none;
        font-weight: bold;
    }
    
    .stButton>button:hover {
        background: linear-gradient(90deg, #3367d6, #2d8f3f);
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'analysis_results' not in st.session_state:
    st.session_state.analysis_results = None
if 'startup_id' not in st.session_state:
    st.session_state.startup_id = None

# Header
st.markdown('<h1 class="main-header">🚀 AI Startup Analyzer</h1>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">Powered by Google AI Technologies | Multi-Agent Analysis System</p>', unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.image("https://www.gstatic.com/images/branding/product/1x/google_cloud_48dp.png", width=50)
    st.title("About")
    st.info("""
    **AI-Powered Investment Analysis**
    
    This system uses 6 specialized AI agents to analyze startups:
    
    🔍 **Agent 1:** Data Extraction  
    📊 **Agent 2:** Benchmarking  
    🚨 **Agent 3:** Risk Detection  
    🌐 **Agent 4:** Market Research  
    🚀 **Agent 5:** Growth Assessment  
    💰 **Agent 6:** Recommendation
    
    **Powered by:**
    - Gemini 2.0 Flash
    - LangChain RAG
    - ChromaDB
    - Vertex AI
    """)
    
    st.divider()
    
    st.subheader("🛠️ Google Technologies")
    tech_stack = [
        "✅ Gemini 2.0 Flash",
        "✅ LangChain",
        "✅ ChromaDB Vectors",
        "✅ Document AI",
        "✅ Cloud Vision",
        "✅ Natural Language API",
        "✅ Google Search API"
    ]
    for tech in tech_stack:
        st.write(tech)

# Main content
tab1, tab2, tab3 = st.tabs(["📤 Upload & Analyze", "📊 Analysis Results", "📈 Advanced Insights"])

# TAB 1: UPLOAD
with tab1:
    st.header("Upload Startup Documents")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("### 📄 Required Documents")
        pitch_deck = st.file_uploader(
            "**Pitch Deck (Required)**",
            type=['pdf'],
            help="Upload the startup's pitch deck in PDF format",
            key="pitch_deck"
        )
        
        if pitch_deck:
            st.success(f"✅ Uploaded: {pitch_deck.name}")
        
        st.markdown("### 📝 Optional Documents")
        
        with st.expander("🎙️ Call Transcripts"):
            transcripts = st.file_uploader(
                "Upload call transcripts",
                type=['txt', 'docx', 'pdf'],
                accept_multiple_files=True,
                key="transcripts"
            )
            if transcripts:
                for t in transcripts:
                    st.success(f"✅ {t.name}")
        
        with st.expander("📧 Email Threads"):
            emails = st.file_uploader(
                "Upload email communications",
                type=['txt', 'docx'],
                accept_multiple_files=True,
                key="emails"
            )
            if emails:
                for e in emails:
                    st.success(f"✅ {e.name}")
        
        with st.expander("📋 Founder Updates"):
            updates = st.file_uploader(
                "Upload founder update emails/reports",
                type=['txt', 'docx', 'pdf'],
                accept_multiple_files=True,
                key="updates"
            )
            if updates:
                for u in updates:
                    st.success(f"✅ {u.name}")
    
    with col2:
        st.markdown("### 📊 Analysis Summary")
        st.info("""
        **What happens next:**
        
        1️⃣ Documents are parsed with LangChain
        
        2️⃣ Content stored in vector database
        
        3️⃣ 6 AI agents analyze in parallel
        
        4️⃣ Comprehensive report generated
        
        ⏱️ **Time:** 2-3 minutes
        """)
    
    st.divider()
    
    # Analyze button
    if st.button("🚀 START ANALYSIS", disabled=not pitch_deck):
        with st.spinner("🔄 Processing documents and running AI analysis..."):
            try:
                # Initialize systems
                processor = DocumentProcessor()
                rag = RAGSystem()
                orchestrator = AgentOrchestrator(rag)
                
                # Generate unique ID
                startup_id = str(uuid.uuid4())
                st.session_state.startup_id = startup_id
                
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
                
                # Create agent status display
                agent_status = st.empty()
                
                def update_agent_status(agent_num, status):
                    agents = [
                        "🔍 Data Extraction",
                        "📊 Benchmarking",
                        "🚨 Risk Detection",
                        "🌐 Market Research",
                        "🚀 Growth Assessment",
                        "💰 Recommendation"
                    ]
                    
                    status_html = "<div style='padding: 1rem;'>"
                    for i, agent in enumerate(agents, 1):
                        if i < agent_num:
                            status_html += f'<span class="agent-status status-complete">✅ {agent}</span>'
                        elif i == agent_num:
                            status_html += f'<span class="agent-status status-processing">⏳ {agent}</span>'
                        else:
                            status_html += f'<span class="agent-status">⚪ {agent}</span>'
                    status_html += "</div>"
                    agent_status.markdown(status_html, unsafe_allow_html=True)
                
                # Simulate agent progress
                for i in range(1, 7):
                    update_agent_status(i, "processing")
                    progress_bar.progress(40 + (i * 10))
                
                # Run analysis
                results = orchestrator.analyze_startup(startup_id)
                
                # Store results
                st.session_state.analysis_results = results
                
                progress_bar.progress(100)
                status_text.text("✅ Analysis complete!")
                
                st.balloons()
                st.success("🎉 Analysis complete! Check the **Analysis Results** tab.")
                
                # Auto-switch to results tab
                st.rerun()
                
            except Exception as e:
                st.error(f"❌ Error during analysis: {str(e)}")
                st.exception(e)

# TAB 2: RESULTS
with tab2:
    if st.session_state.analysis_results is None:
        st.info("👆 Upload documents in the first tab to start analysis")
    else:
        results = st.session_state.analysis_results
        
        # Extract key data
        company_info = results['extracted_data']['company_info']
        recommendation = results['recommendation']
        risk_analysis = results['risk_analysis']
        benchmark_data = results.get('benchmark_data', {})
        growth_assessment = results.get('growth_assessment', {})
        
        # Header with company info
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
        
        # RECOMMENDATION CARD
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
                        {'range': [0, 40], 'color': "#fce8e6"},
                        {'range': [40, 65], 'color': "#fef7e0"},
                        {'range': [65, 100], 'color': "#e6f4ea"}
                    ],
                    'threshold': {
                        'line': {'color': "red", 'width': 4},
                        'thickness': 0.75,
                        'value': 65
                    }
                }
            ))
            fig.update_layout(height=200, margin=dict(l=20, r=20, t=20, b=20))
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
                        {'range': [0, 40], 'color': "#e6f4ea"},
                        {'range': [40, 70], 'color': "#fef7e0"},
                        {'range': [70, 100], 'color': "#fce8e6"}
                    ]
                }
            ))
            fig.update_layout(height=200, margin=dict(l=20, r=20, t=20, b=20))
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
                    'bar': {'color': "#4285f4"},
                    'steps': [
                        {'range': [0, 40], 'color': "#fce8e6"},
                        {'range': [40, 70], 'color': "#fef7e0"},
                        {'range': [70, 100], 'color': "#e6f4ea"}
                    ]
                }
            ))
            fig.update_layout(height=200, margin=dict(l=20, r=20, t=20, b=20))
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
                        {'range': [0, 40], 'color': "#fce8e6"},
                        {'range': [40, 60], 'color': "#fef7e0"},
                        {'range': [60, 100], 'color': "#e6f4ea"}
                    ]
                }
            ))
            fig.update_layout(height=200, margin=dict(l=20, r=20, t=20, b=20))
            st.plotly_chart(fig, use_container_width=True)
        
        st.divider()
        
        # STRENGTHS & CONCERNS
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
        st.markdown("### 🤔 Suggested Follow-up Questions")
        for i, question in enumerate(recommendation['follow_up_questions'], 1):
            st.info(f"**{i}.** {question}")
        
        st.divider()
        
        # EXPORT OPTIONS
        st.markdown("### 📥 Export Report")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            # Download JSON
            json_str = json.dumps(results, indent=2)
            st.download_button(
                label="📄 Download JSON",
                data=json_str,
                file_name=f"analysis_{company_info['name']}_{datetime.now().strftime('%Y%m%d')}.json",
                mime="application/json"
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
                mime="text/plain"
            )
# Add these imports at the top of app.py



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
                st.session_state['pdf_path'] = generated_path
                st.session_state['pdf_filename'] = pdf_filename
                
                st.success(f"✅ Professional PDF report generated successfully!")
                st.balloons()
                
            except Exception as e:
                st.error(f"❌ Error generating PDF: {str(e)}")
                st.exception(e)

# Show download button if PDF exists
if 'pdf_path' in st.session_state and os.path.exists(st.session_state['pdf_path']):
    
    st.success(f"✅ Report ready: **{st.session_state['pdf_filename']}**")
    
    # Download button
    with open(st.session_state['pdf_path'], 'rb') as pdf_file:
        pdf_data = pdf_file.read()
        
        st.download_button(
            label="📥 Download PDF Report",
            data=pdf_data,
            file_name=st.session_state['pdf_filename'],
            mime="application/pdf",
            key="download_pdf"
        )
    
    st.divider()
    
    # ============================================================
    # EMAIL SECTION
    # ============================================================
    
    st.markdown("### 📧 Send Report to Investors via Gmail")
    
    st.info("""
    **Gmail API Setup (First Time Only):**
    
    1️⃣ Download `credentials.json` from Google Cloud Console
    
    2️⃣ Place it in your project root directory
    
    3️⃣ Click "Send Email" - browser will open for authentication
    
    4️⃣ Grant permissions - token will be saved for future use
    
    **Free Tier:** Unlimited emails with your Gmail account!
    """)
    
    # Single recipient
    with st.expander("📤 Send to Single Investor", expanded=True):
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
                with st.spinner("📨 Sending email via Gmail API..."):
                    try:
                        gmail_sender = GmailSender()
                        
                        success = gmail_sender.send_report(
                            recipient_email=investor_email,
                            subject=email_subject,
                            company_name=company_info['name'],
                            decision=recommendation['decision'],
                            pdf_path=st.session_state['pdf_path']
                        )
                        
                        if success:
                            st.success(f"✅ Report sent successfully to **{investor_email}**")
                            st.balloons()
                        else:
                            st.error("❌ Failed to send email. Check console for details.")
                            
                    except FileNotFoundError as e:
                        st.error(str(e))
                        st.info("👆 Please download credentials.json from Google Cloud Console")
                    except Exception as e:
                        st.error(f"❌ Error: {str(e)}")
                        st.exception(e)
    
    # Multiple recipients
    with st.expander("📤 Send to Multiple Investors"):
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
                            pdf_path=st.session_state['pdf_path']
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
    with st.expander("👁️ Preview Email Content"):
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
    st.warning("⬆️ Generate the PDF report first using the button above")

# TAB 3: ADVANCED INSIGHTS
with tab3:
    if st.session_state.analysis_results is None:
        st.info("👆 Upload documents in the first tab to start analysis")
    else:
        results = st.session_state.analysis_results
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
            line=dict(color='#4285f4', width=2),
            fillcolor='rgba(66, 133, 244, 0.3)'
        ))
        
        fig.add_trace(go.Scatterpolar(
            r=[7, 7, 7, 7, 7],
            theta=categories,
            fill='toself',
            name='Target Score',
            line=dict(color='#34a853', width=1, dash='dash'),
            fillcolor='rgba(52, 168, 83, 0.1)'
        ))
        
        fig.update_layout(
            polar=dict(
                radialaxis=dict(
                    visible=True,
                    range=[0, 10]
                )
            ),
            showlegend=True,
            height=500
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        st.divider()
        
        # Detailed breakdowns
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("📊 Benchmarking Details")
            
            comparisons = benchmark_data.get('comparisons', {})
            
            for metric, data in comparisons.items():
                if isinstance(data, dict):
                    status = data.get('status', 'Unknown')
                    startup_val = data.get('startup_value', 'Unknown')
                    sector_avg = data.get('sector_average', 'Unknown')
                    
                    with st.expander(f"**{metric.replace('_', ' ').title()}**"):
                        st.write(f"**Startup:** {startup_val}")
                        st.write(f"**Sector Average:** {sector_avg}")
                        st.write(f"**Status:** {status}")
                        if 'notes' in data:
                            st.write(f"**Notes:** {data['notes']}")
        
        with col2:
            st.subheader("🚀 Growth Potential Details")
            
            for dimension, data in growth_scores.items():
                if isinstance(data, dict):
                    score = data.get('score', 0)
                    
                    with st.expander(f"**{dimension.replace('_', ' ').title()}** - Score: {score}/10"):
                        st.write(f"**Reasoning:** {data.get('reasoning', 'N/A')}")
                        if 'evidence' in data and data['evidence']:
                            st.write("**Evidence:**")
                            for evidence in data['evidence']:
                                st.write(f"- {evidence}")
        
        st.divider()
        
        # Market validation
        st.subheader("🌐 Market Validation")
        
        market_research = results.get('market_research', {})
        validations = market_research.get('validations', {})
        
        for val_type, val_data in validations.items():
            if isinstance(val_data, dict):
                with st.expander(f"**{val_type.replace('_', ' ').title()}**"):
                    st.write(f"**Claimed:** {val_data.get('claimed', 'N/A')}")
                    st.write(f"**Found:** {val_data.get('found', 'N/A')}")
                    st.write(f"**Status:** {val_data.get('status', 'N/A')}")
                    st.write(f"**Notes:** {val_data.get('notes', 'N/A')}")

# Footer
st.divider()
st.markdown("""
<div style='text-align: center; color: #5f6368; padding: 2rem;'>
    <p>🚀 <strong>AI Startup Analyzer</strong> | Powered by Google Cloud & Gemini 2.0</p>
    <p>Built with Streamlit • LangChain • ChromaDB • Multi-Agent AI System</p>
</div>

""", unsafe_allow_html=True)
