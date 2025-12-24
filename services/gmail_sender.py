# services/gmail_sender.py

from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import base64
import os
import pickle

SCOPES = ['https://www.googleapis.com/auth/gmail.send']
CREDENTIALS_FILE = '/tmp/credentials.json'
TOKEN_FILE = '/tmp/token.pickle'
class GmailSender:
    """Send emails using Gmail API with PDF attachments"""
    
    def __init__(self):
        self.creds = None
        self.service = None
        self._authenticate()
    
    def _authenticate(self):
        """Authenticate with Gmail API"""
        
        # Check if we have saved credentials
        if os.path.exists('token.pickle'):
            with open('token.pickle', 'rb') as token:
                self.creds = pickle.load(token)
        
        # If no valid credentials, let user log in
        if not self.creds or not self.creds.valid:
            if self.creds and self.creds.expired and self.creds.refresh_token:
                self.creds.refresh(Request())
            else:
               if not os.path.exists(CREDENTIALS_FILE):
                    # Fallback: check current directory (for local development)
                    if os.path.exists('credentials.json'):
                        credentials_path = 'credentials.json'
                    else:
                        raise FileNotFoundError(
                            "credentials.json not found! Please ensure environment variables are set:\n"
                            "- GMAIL_CLIENT_ID\n"
                            "- GMAIL_CLIENT_SECRET\n\n"
                            "For local development:\n"
                            "1. Go to https://console.cloud.google.com/\n"
                            "2. Enable Gmail API\n"
                            "3. Create OAuth 2.0 credentials\n"
                            "4. Download as 'credentials.json'"
                        )
               else:
                credentials_path = CREDENTIALS_FILE
                
                flow = InstalledAppFlow.from_client_secrets_file(credentials_path, SCOPES)
                self.creds = flow.run_local_server(port=0)
            
            # Save credentials for next time
            with open(TOKEN_FILE, 'wb') as token:
                pickle.dump(self.creds, token)
        
        self.service = build('gmail', 'v1', credentials=self.creds)
        print("✅ Gmail API authenticated successfully")
    
    def send_report(self, recipient_email, subject, company_name, decision, pdf_path):
        """
        Send investment report via Gmail API
        
        Args:
            recipient_email: Email address of recipient
            subject: Email subject line
            company_name: Name of the startup
            decision: Investment decision (INVEST/MAYBE/PASS)
            pdf_path: Path to the PDF report file
        """
        
        try:
            # Validate PDF exists
            if not os.path.exists(pdf_path):
                raise FileNotFoundError(f"PDF not found at {pdf_path}")
            
            # Create message
            message = MIMEMultipart()
            message['to'] = recipient_email
            message['subject'] = subject
            
            # Determine colors based on decision
            if decision == "INVEST":
                decision_color = "#34a853"
                decision_emoji = "✅"
            elif decision == "MAYBE":
                decision_color = "#fbbc04"
                decision_emoji = "⚠️"
            else:
                decision_color = "#ea4335"
                decision_emoji = "❌"
            
            # HTML email body with professional styling
            html_body = f"""
            <html>
              <head>
                <style>
                  body {{ font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; margin: 0; padding: 0; }}
                  .header {{ background: linear-gradient(90deg, #4285f4, #34a853, #fbbc04, #ea4335); height: 8px; }}
                  .container {{ padding: 30px; max-width: 600px; margin: 0 auto; }}
                  .logo {{ text-align: center; margin-bottom: 30px; }}
                  .decision-box {{ 
                    background: {decision_color}15; 
                    border-left: 5px solid {decision_color}; 
                    padding: 20px; 
                    margin: 25px 0;
                    border-radius: 5px;
                  }}
                  .decision-text {{ 
                    color: {decision_color}; 
                    font-size: 24px; 
                    font-weight: bold; 
                    margin: 0;
                  }}
                  .section {{ margin: 20px 0; }}
                  .section-title {{ 
                    color: #4285f4; 
                    font-size: 16px; 
                    font-weight: bold; 
                    margin-bottom: 10px;
                  }}
                  ul {{ padding-left: 20px; }}
                  li {{ margin: 8px 0; color: #333; }}
                  .footer {{ 
                    background: #f8f9fa; 
                    padding: 20px; 
                    margin-top: 30px; 
                    border-radius: 5px;
                    font-size: 12px; 
                    color: #5f6368;
                  }}
                  .cta-button {{
                    background: #4285f4;
                    color: white;
                    padding: 12px 25px;
                    text-decoration: none;
                    border-radius: 5px;
                    display: inline-block;
                    margin: 20px 0;
                    font-weight: bold;
                  }}
                </style>
              </head>
              <body>
                <div class="header"></div>
                
                <div class="container">
                  <div class="logo">
                    <h1 style="color: #4285f4; margin: 0;">🚀 AI Startup Analyzer</h1>
                    <p style="color: #5f6368; margin: 5px 0;">Investment Analysis Report</p>
                  </div>
                  
                  <p style="font-size: 16px;">Dear Investor,</p>
                  
                  <p style="line-height: 1.6;">
                    Our AI-powered multi-agent analysis system has completed a comprehensive evaluation of 
                    <strong>{company_name}</strong>. Please find the detailed investment report attached to this email.
                  </p>
                  
                  <div class="decision-box">
                    <p class="decision-text">{decision_emoji} Investment Decision: {decision}</p>
                  </div>
                  
                  <div class="section">
                    <div class="section-title">📊 Report Highlights:</div>
                    <ul>
                      <li><strong>Executive Summary</strong> - Investment decision and key metrics</li>
                      <li><strong>Company Overview</strong> - Business model and team analysis</li>
                      <li><strong>Growth Analysis</strong> - Multi-dimensional scoring with radar charts</li>
                      <li><strong>Risk Assessment</strong> - Comprehensive red flag analysis</li>
                      <li><strong>Market Validation</strong> - Third-party research and benchmarking</li>
                      <li><strong>Actionable Insights</strong> - Follow-up questions and next steps</li>
                    </ul>
                  </div>
                  
                  <div class="section">
                    <div class="section-title">🤖 Analysis Methodology:</div>
                    <p style="line-height: 1.6; color: #333;">
                      This report was generated by our 6-agent AI system, analyzing pitch decks, financial data, 
                      call transcripts, and market research. Each agent specializes in a specific dimension:
                    </p>
                    <ul>
                      <li>Agent 1: Data Extraction & Structuring</li>
                      <li>Agent 2: Sector Benchmarking</li>
                      <li>Agent 3: Risk Detection & Red Flags</li>
                      <li>Agent 4: Market Research & Validation</li>
                      <li>Agent 5: Growth Potential Assessment</li>
                      <li>Agent 6: Investment Recommendation</li>
                    </ul>
                  </div>
                  
                  <p style="line-height: 1.6; margin-top: 30px;">
                    The attached PDF contains detailed analysis, professional charts, and evidence-based insights 
                    to support your investment decision-making process.
                  </p>
                  
                  <div style="text-align: center; margin: 30px 0;">
                    <p style="font-size: 14px; color: #5f6368;">
                      <em>Please review the attached report for complete details</em>
                    </p>
                  </div>
                  
                  <div class="footer">
                    <p style="margin: 5px 0;"><strong>AI Startup Analyzer</strong></p>
                    <p style="margin: 5px 0;">Powered by Google Gemini 2.0 Flash, LangChain, ChromaDB</p>
                    <p style="margin: 15px 0 5px 0; font-size: 11px;">
                      <em>This automated analysis should be used as part of a comprehensive due diligence process. 
                      The AI-generated insights are based on available data and should be validated through 
                      direct founder interactions and additional research.</em>
                    </p>
                  </div>
                </div>
                
                <div class="header"></div>
              </body>
            </html>
            """
            
            message.attach(MIMEText(html_body, 'html'))
            
            # Attach PDF
            with open(pdf_path, 'rb') as f:
                pdf_data = f.read()
            
            part = MIMEBase('application', 'octet-stream')
            part.set_payload(pdf_data)
            encoders.encode_base64(part)
            
            filename = os.path.basename(pdf_path)
            part.add_header('Content-Disposition', f'attachment; filename="{filename}"')
            message.attach(part)
            
            # Encode message
            raw = base64.urlsafe_b64encode(message.as_bytes()).decode()
            
            # Send via Gmail API
            send_message = {'raw': raw}
            result = self.service.users().messages().send(
                userId='me',
                body=send_message
            ).execute()
            
            print(f"✅ Email sent successfully via Gmail API")
            print(f"   To: {recipient_email}")
            print(f"   Subject: {subject}")
            print(f"   Message ID: {result['id']}")
            print(f"   PDF attached: {filename}")
            
            return True
            
        except FileNotFoundError as e:
            print(f"❌ File error: {e}")
            return False
        except Exception as e:
            print(f"❌ Error sending email: {e}")
            import traceback
            traceback.print_exc()
            return False
    
    def send_bulk_reports(self, recipient_list, subject, company_name, decision, pdf_path):
        """
        Send report to multiple recipients
        
        Args:
            recipient_list: List of email addresses
            subject, company_name, decision, pdf_path: Same as send_report()
        
        Returns:
            dict with success/failure counts
        """
        
        results = {
            'success': 0,
            'failed': 0,
            'failed_emails': []
        }
        
        for email in recipient_list:
            success = self.send_report(email, subject, company_name, decision, pdf_path)
            
            if success:
                results['success'] += 1
            else:
                results['failed'] += 1
                results['failed_emails'].append(email)
        
        print(f"\n📧 Bulk email summary:")
        print(f"   ✅ Sent: {results['success']}")
        print(f"   ❌ Failed: {results['failed']}")
        

        return results


