from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings


def send_email(subject, to_email, template, data):
    html_body = render_to_string(template, data)
    text_body = strip_tags(html_body)

    msg = EmailMultiAlternatives(
        subject=subject,
        from_email=settings.FROM_EMAIL,
        to=[to_email],
        body=text_body)
    msg.attach_alternative(html_body, "text/html")
    msg.send()
