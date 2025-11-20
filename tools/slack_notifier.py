"""
Slack Notification Tool for Code Review Agent
Sends notifications to Slack when critical events occur
"""

import os
import json
import requests
from typing import Optional


def create_slack_notifier_function():
    """
    Creates a tool function to send notifications to Slack
    """
    
    def send_slack_notification(
        message: str,
        severity: str = "INFO",
        channel: Optional[str] = None,
        include_details: bool = True
    ) -> str:
        """
        Send notification to Slack channel.
        
        Args:
            message: Main notification message
            severity: Severity level (CRITICAL, HIGH, MEDIUM, LOW, INFO)
            channel: Slack channel (default from env)
            include_details: Include detailed formatting
            
        Returns:
            JSON string with status
        """
        
        # Get Slack webhook URL from environment
        webhook_url = os.getenv('SLACK_WEBHOOK_URL')
        
        if not webhook_url:
            return json.dumps({
                "status": "error",
                "message": "SLACK_WEBHOOK_URL not configured in .env"
            }, ensure_ascii=False, indent=2)
        
        # Emoji mapping for severity
        emoji_map = {
            "CRITICAL": "🔴",
            "HIGH": "🟠",
            "MEDIUM": "🟡",
            "LOW": "🟢",
            "INFO": "ℹ️",
            "SUCCESS": "✅"
        }
        
        emoji = emoji_map.get(severity.upper(), "📢")
        
        # Build Slack message payload
        if include_details:
            payload = {
                "blocks": [
                    {
                        "type": "header",
                        "text": {
                            "type": "plain_text",
                            "text": f"{emoji} Code Review Alert",
                            "emoji": True
                        }
                    },
                    {
                        "type": "section",
                        "fields": [
                            {
                                "type": "mrkdwn",
                                "text": f"*Severity:*\n{severity}"
                            },
                            {
                                "type": "mrkdwn",
                                "text": f"*Timestamp:*\n<!date^{int(__import__('time').time())}^{{date_short_pretty}} {{time}}|Now>"
                            }
                        ]
                    },
                    {
                        "type": "section",
                        "text": {
                            "type": "mrkdwn",
                            "text": message
                        }
                    },
                    {
                        "type": "divider"
                    }
                ]
            }
        else:
            # Simple text message
            payload = {
                "text": f"{emoji} {message}"
            }
        
        # Add channel override if provided
        if channel:
            payload["channel"] = channel
        
        # Send to Slack
        try:
            response = requests.post(
                webhook_url,
                json=payload,
                headers={"Content-Type": "application/json"},
                timeout=10
            )
            
            if response.status_code == 200:
                return json.dumps({
                    "status": "success",
                    "message": f"Notification sent to Slack ({severity})"
                }, ensure_ascii=False, indent=2)
            else:
                return json.dumps({
                    "status": "error",
                    "message": f"Slack API error: {response.status_code}",
                    "details": response.text
                }, ensure_ascii=False, indent=2)
                
        except requests.exceptions.Timeout:
            return json.dumps({
                "status": "error",
                "message": "Slack request timeout after 10s"
            }, ensure_ascii=False, indent=2)
            
        except Exception as e:
            return json.dumps({
                "status": "error",
                "message": f"Failed to send Slack notification: {str(e)}"
            }, ensure_ascii=False, indent=2)
    
    return send_slack_notification


# Helper function for common notification patterns
def notify_critical_issues(pr_number: int, repo: str, critical_count: int, issue_summary: str):
    """
    Quick helper to notify about critical issues found
    """
    notifier = create_slack_notifier_function()
    
    message = f"""
*Critical Issues Found in PR #{pr_number}*
Repository: `{repo}`
Critical Issues: *{critical_count}*

{issue_summary}

<https://github.com/{repo}/pull/{pr_number}|View Pull Request>
"""
    
    return notifier(
        message=message,
        severity="CRITICAL",
        include_details=True
    )


def notify_review_complete(pr_number: int, repo: str, total_issues: int, decision: str):
    """
    Quick helper to notify when review is complete
    """
    notifier = create_slack_notifier_function()
    
    decision_emoji = {
        "APPROVE": "✅",
        "REQUEST CHANGES": "❌",
        "COMMENT": "⚠️"
    }
    
    emoji = decision_emoji.get(decision, "📋")
    
    message = f"""
{emoji} *Code Review Complete for PR #{pr_number}*
Repository: `{repo}`
Total Issues: *{total_issues}*
Decision: *{decision}*

<https://github.com/{repo}/pull/{pr_number}|View Pull Request>
"""
    
    severity = "HIGH" if decision == "REQUEST CHANGES" else "SUCCESS"
    
    return notifier(
        message=message,
        severity=severity,
        include_details=True
    )
