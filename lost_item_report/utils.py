import os
import uuid
from typing import List

from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils import timezone
from django.utils.html import strip_tags

def send_email_functionality(emails: List[str], item_name, template_name: str, **kwargs):
    subject = kwargs.get('subject', 'New Item Available In Similar Category')
    from_email = kwargs.get('from_email', '<no-reply@nsu-lf.com>')
    print(kwargs)
    logo_url = 'https://upload.wikimedia.org/wikipedia/en/thumb/e/e0/North_South_University_Monogram.svg/120px-North_South_University_Monogram.svg.png'

    # render HTML email template
    html_content = render_to_string(template_name, {
        'website_name': "NSU LF",
        'current_year': "2023",
        'logo_url': logo_url,
        'item_name': item_name,
        'model_version': kwargs.get("model_version"),
        'description': kwargs.get("description"),
        'location': kwargs.get("location"),
        'date_lost': kwargs.get("date_lost"),
    })

    # create plain text version of the email
    text_content = strip_tags(html_content)

    # create the email message object
    email_message = EmailMultiAlternatives(subject, text_content, from_email, emails)
    email_message.attach_alternative(html_content, 'text/html')

    # send the email
    email_message.send()


def get_upload_path(instance, filename):
    # Get the filename without the path
    _, extension = os.path.splitext(filename)
    filename = f'{uuid.uuid4().hex}{extension}'

    # Generate the relative path for storing the image
    today = timezone.now().date()
    upload_path = f'media/{today.year}/{today.month}/{today.day}/{filename}'

    return upload_path