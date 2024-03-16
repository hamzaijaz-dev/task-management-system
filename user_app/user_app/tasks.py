"""Celery tasks for ML wrapper app."""
from django.core.mail import EmailMessage
from django.template.loader import get_template

from user_app.celery import app


@app.task(name='send_email')
def send_email(email_data):
    email_body = get_template(email_data['html_body_template_name']).render(email_data['context'])
    email = EmailMessage(
        subject=email_data['subject'],
        body=email_body,
        to=email_data['recipients'],
        from_email=email_data['from_email_address'],
    )
    email.content_subtype = 'html'
    email.send()
