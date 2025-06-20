import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import List, Dict
import logging
from app.utils.config_manager import ConfigManager

class EmailNotifier:
    def __init__(self, server_url: str = 'http://localhost:5000', config_file: str = 'email_config.json'):
        """
        Initialize email notifier with server URL and config file path.
        Args:
            server_url: Base URL of the server for generating links
            config_file: Path to the email config file
        """
        self.server_url = server_url.rstrip('/')
        self.config_file = config_file
    
    def send_issue_notification(self, to_emails: List[str], specific_function: str, 
                               issues: List[Dict], batch_id: str = None) -> bool:
        """
        Send issue notification email to specified recipients.
        Args:
            to_emails: List of email addresses to send to
            specific_function: The specific function these issues belong to
            issues: List of issue dictionaries
            batch_id: Optional batch ID for tracking
        Returns:
            bool: True if email sent successfully, False otherwise
        """
        if not to_emails:
            logging.warning("No email addresses provided for notification")
            return False
        
        # 每次发送邮件时动态读取最新配置
        config = ConfigManager.get_email_config(self.config_file)
        smtp_server = config.get('SMTP_SERVER', 'localhost')
        smtp_port = config.get('SMTP_PORT', 587)
        username = config.get('SMTP_USERNAME', None)
        password = config.get('SMTP_PASSWORD', None)
        use_tls = config.get('SMTP_USE_TLS', True)
        email_from = config.get('EMAIL_FROM', username or 'noreply@example.com')
        
        try:
            # Create message
            msg = MIMEMultipart()
            msg['Subject'] = f'New Issue Notification - {specific_function}'
            msg['From'] = email_from
            msg['To'] = ', '.join(to_emails)
            
            # Create email body
            body = self._create_email_body(specific_function, issues, batch_id)
            msg.attach(MIMEText(body, 'plain', 'utf-8'))
            
            # Send email
            with smtplib.SMTP(smtp_server, smtp_port) as server:
                if use_tls:
                    server.starttls()
                if username and password:
                    server.login(username, password)
                server.send_message(msg)
                
            logging.info(f"Notification email sent successfully to {len(to_emails)} recipients for {specific_function}")
            return True
            
        except Exception as e:
            logging.error(f"Failed to send notification email: {str(e)}")
            return False
    
    def _create_email_body(self, specific_function: str, issues: List[Dict], batch_id: str = None) -> str:
        """
        Create the email body content (English).
        
        Args:
            specific_function: The specific function name
            issues: List of issue dictionaries
            batch_id: Optional batch ID
            
        Returns:
            str: Formatted email body
        """
        body = f"""New Issue Notification

Specific Function: {specific_function}
Batch ID: {batch_id or 'N/A'}
Number of Issues: {len(issues)}

Issue Details:
"""
        
        for i, issue in enumerate(issues, 1):
            body += f"""
{i}. Issue #{issue.get('global_id', 'N/A')}
    - Carline: {issue.get('carline', 'N/A')}
    - Function Domain: {issue.get('function_domain', 'N/A')}
    - Issue Type: {issue.get('issue_type', 'N/A')}
    - Brief Description: {issue.get('brief_issue_en', issue.get('brief_issue', 'N/A'))}
    - Create Time: {issue.get('create_time', 'N/A')}
    - Status: {issue.get('status', 'New')}
"""
        
        # Add server access links
        body += f"""

Please handle these issues in a timely manner.

Access Links:
- Engineer Issue List: {self.server_url}/engineer/issues

This email was sent automatically by the system. Please do not reply.
"""
        return body

class MockEmailNotifier(EmailNotifier):
    """
    Mock email notifier for testing purposes.
    Stores sent emails in memory instead of actually sending them.
    """
    
    def __init__(self):
        super().__init__()
        self.sent_emails = []
        
    def send_issue_notification(self, to_emails: List[str], specific_function: str, 
                               issues: List[Dict], batch_id: str = None) -> bool:
        """
        Mock implementation that stores email data instead of sending.
        """
        email_data = {
            'to_emails': to_emails,
            'specific_function': specific_function,
            'issues': issues,
            'batch_id': batch_id,
            'body': self._create_email_body(specific_function, issues, batch_id)
        }
        self.sent_emails.append(email_data)
        logging.info(f"Mock email notification stored: {specific_function} -> {len(to_emails)} recipients")
        return True
        
    def get_sent_emails(self) -> List[Dict]:
        """Get all sent emails for testing."""
        return self.sent_emails.copy()
        
    def clear_sent_emails(self):
        """Clear sent emails list for testing."""
        self.sent_emails.clear() 