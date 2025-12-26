# services/gmail_sender.py

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import os

class GmailSender:
    """Send emails using Gmail SMTP with App Password (no browser required)"""
    
    def __init__(self):
        """Initialize Gmail sender with credentials from environment variables"""
        self.gmail_user = os.getenv('GMAIL_USER')
        self.gmail_app_password = os.getenv('GMAIL_APP_PASSWORD')
        
        # Validate credentials
        if not self.gmail_user:
            raise ValueError(
                "GMAIL_USER environment variable is not set!\n"
                "Please set it to your Gmail address (e.g., your-email@gmail.com)"
            )
        if not self.gmail_app_password:
            raise ValueError(
                "GMAIL_APP_PASSWORD environment variable is not set!\n"
                "Please generate an App Password from Google Account settings:\n"
                "1. Go to https://myaccount.google.com/security\n"
                "2. Enable 2-Step Verification\n"
                "3. Go to App passwords\n"
                "4. Generate a new app password for 'Mail'\n"
                "5. Copy the 16-character password and set it as GMAIL_APP_PASSWORD"
            )
        
        print("✅ Gmail SMTP configured successfully")
    
    def send_report(self, recipient_email, subject, company_name, decision, pdf_path):
        """
        Send investment report via Gmail SMTP
        
        Args:
            recipient_email: Email address of recipient
            subject: Email subject line
            company_name: Name of the startup
            decision: Investment decision (INVEST/MAYBE/PASS)
            pdf_path: Path to the PDF report file
        
        Returns:
            bool: True if sent successfully, False otherwise
        """
        
        try:
            # Validate PDF exists
            if not os.path.exists(pdf_path):
                raise FileNotFoundError(f"PDF not found at {pdf_path}")
            
            # Create message
            message = MIMEMultipart()
            message['From'] = self.gmail_user
            message['To'] = recipient_email
            message['Subject'] = subject
            
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
            
            # Attach HTML body
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
            
            # Connect to Gmail SMTP server
            print(f"📤 Connecting to Gmail SMTP server...")
            server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
            
            # Login with app password
            print(f"🔐 Authenticating with Gmail...")
            server.login(self.gmail_user, self.gmail_app_password)
            
            # Send email
            print(f"📧 Sending email to {recipient_email}...")
            server.send_message(message)
            
            # Close connection
            server.quit()
            
            print(f"✅ Email sent successfully!")
            print(f"   From: {self.gmail_user}")
            print(f"   To: {recipient_email}")
            print(f"   Subject: {subject}")
            print(f"   PDF attached: {filename}")
            
            return True
            
        except FileNotFoundError as e:
            print(f"❌ File error: {e}")
            return False
        except smtplib.SMTPAuthenticationError as e:
            print(f"❌ Authentication failed: {e}")
            print(f"   Check that:")
            print(f"   1. GMAIL_USER is correct: {self.gmail_user}")
            print(f"   2. GMAIL_APP_PASSWORD is a valid 16-character app password")
            print(f"   3. 2-Step Verification is enabled on your Google Account")
            return False
        except smtplib.SMTPException as e:
            print(f"❌ SMTP error: {e}")
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
        
        print(f"\n📧 Sending bulk emails to {len(recipient_list)} recipients...")
        
        for i, email in enumerate(recipient_list, 1):
            print(f"\n[{i}/{len(recipient_list)}] Processing: {email}")
            success = self.send_report(email, subject, company_name, decision, pdf_path)
            
            if success:
                results['success'] += 1
            else:
                results['failed'] += 1
                results['failed_emails'].append(email)
        
        print(f"\n" + "="*50)
        print(f"📧 Bulk email summary:")
        print(f"   ✅ Successfully sent: {results['success']}")
        print(f"   ❌ Failed: {results['failed']}")
        if results['failed_emails']:
            print(f"   Failed emails: {', '.join(results['failed_emails'])}")
        print("="*50)
        
        return results
    
    def send_simple_email(self, to_email, subject, body, is_html=False):
        """
        Send a simple email without attachments
        
        Args:
            to_email: Recipient email address
            subject: Email subject
            body: Email body content
            is_html: Whether body is HTML or plain text
        
        Returns:
            bool: True if sent successfully, False otherwise
        """
        
        try:
            msg = MIMEMultipart()
            msg['From'] = self.gmail_user
            msg['To'] = to_email
            msg['Subject'] = subject
            
            if is_html:
                msg.attach(MIMEText(body, 'html'))
            else:
                msg.attach(MIMEText(body, 'plain'))
            
            server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
            server.login(self.gmail_user, self.gmail_app_password)
            server.send_message(msg)
            server.quit()
            
            print(f"✅ Simple email sent to {to_email}")
            return True
            
        except Exception as e:
            print(f"❌ Error sending simple email: {e}")
            return False


# Example usage and testing
if __name__ == "__main__":
    """Test the Gmail sender"""
    
    print("🧪 Testing Gmail Sender with SMTP...")
    print("="*50)
    
    try:
        # Initialize sender
        sender = GmailSender()
        
        # Test simple email
        print("\n📧 Sending test email...")
        success = sender.send_simple_email(
            to_email="sawarnish661@gmail.com",
            subject="Test Email - RAG Investment App",
            body="""
            <html>
                <body>
                    <h2>Gmail SMTP Test</h2>
                    <p>If you receive this email, the Gmail sender is working correctly!</p>
                    <p><strong>Configuration:</strong></p>
                    <ul>
                        <li>Using SMTP with App Password</li>
                        <li>No browser authentication required</li>
                        <li>Works in deployment environments</li>
                    </ul>
                </body>
            </html>
            """,
            is_html=True
        )
        
        if success:
            print("\n✅ Test passed! Gmail sender is working.")
        else:
            print("\n❌ Test failed. Check your environment variables.")
            
    except ValueError as e:
        print(f"\n❌ Configuration error: {e}")
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
