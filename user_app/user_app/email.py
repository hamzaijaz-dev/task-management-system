"""Email logic."""

from django.conf import settings
from django.template import loader

from user_app.tasks import send_email


class BaseEmailMessage:
    """Base class for sending emails."""

    from_email_address = settings.FROM_EMAIL_ADDRESS
    html_body_template_name = ''
    subject = ''

    def _initialize_subject(self, context):
        """Initialize subject from file if necessary."""
        if '.txt' in self.subject:
            subject = loader.render_to_string(self.subject, context)
            self.subject = ''.join(subject.splitlines())
        return self.subject

    def _serialize_data(self, recipients, context):
        """Serialize data for celery task."""
        return {
            'subject': self._initialize_subject(context),
            'from_email_address': self.from_email_address,
            'recipients': recipients,
            'html_body_template_name': self.html_body_template_name,
            'context': context,
        }

    def send(self, recipients, context=None):
        """Send email."""
        send_email.delay(self._serialize_data(recipients, context))


class CreateTodo(BaseEmailMessage):
    subject = 'Todo is created'
    html_body_template_name = 'emails/create_todo.html'
