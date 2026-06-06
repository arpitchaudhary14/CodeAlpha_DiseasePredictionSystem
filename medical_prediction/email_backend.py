import os
import json
import urllib.request
import logging
from django.core.mail.backends.base import BaseEmailBackend


class WebhookEmailBackend(BaseEmailBackend):
    """
    A custom Django email backend that sends emails via a Google Apps Script
    Webhook (HTTPS) to bypass Render's SMTP port blocking on free tier.
    Falls back gracefully if the webhook URL is not configured.
    """

    def send_messages(self, email_messages):
        webhook_url = os.getenv('GMAIL_WEBHOOK_URL', '')

        if not webhook_url:
            logging.warning("GMAIL_WEBHOOK_URL not set. Emails will not be sent.")
            return 0

        sent_count = 0
        for message in email_messages:
            try:
                # Prefer HTML content, fall back to plain text
                html_body = None
                if message.alternatives:
                    for content, mimetype in message.alternatives:
                        if mimetype == 'text/html':
                            html_body = content
                            break

                data = {
                    'to': message.to[0],
                    'subject': message.subject,
                    'htmlBody': html_body if html_body else message.body.replace('\n', '<br>'),
                }

                req = urllib.request.Request(
                    webhook_url,
                    data=json.dumps(data).encode('utf-8'),
                    headers={'Content-Type': 'application/json'}
                )
                urllib.request.urlopen(req, timeout=10)
                sent_count += 1
                logging.info(f"Email sent via webhook to {message.to[0]}")
            except Exception as e:
                logging.error(f"Webhook email failed for {message.to}: {e}")
                if not self.fail_silently:
                    raise

        return sent_count
