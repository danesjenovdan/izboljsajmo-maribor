from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings
from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _

import string
import random
import os
import csv

def send_email(subject, to_email, template, data, from_email=settings.FROM_EMAIL):
    html_body = render_to_string(template, data)
    text_body = strip_tags(html_body)

    msg = EmailMultiAlternatives(
        subject=subject,
        from_email=from_email,
        to=[to_email],
        body=text_body)
    msg.attach_alternative(html_body, "text/html")
    msg.send()


def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


def validate_file_extension(value):
    ext = os.path.splitext(value.name)[1]
    valid_extensions = ['.pdf','.doc','.docx', '.jpg', '.jpeg', '.png', '.gif']
    if not ext in valid_extensions:
        raise ValidationError(_('File not supported!'))

# SUPER_ADMIN = 'SA', _('SUPER ADMIN')
# AREA_ADMIN = 'AA', _('AREA ADMIN')
# AREA_APPRAISER = 'AP', _('AREA APPRAISER')
# CONTRACTOR_APPRAISER = 'CA', _('CONTRACTOR APPRAISER')

def import_users():
    users = {}
    from initiatives.models import User, Area, AreaAppraiserUser, SuperAdminUser, AreaAdminUser, ContractorAppraiserUser
    #id,ime,urad,area,email,role
    with open('users.csv', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            user = User.objects.filter(email=row['email'])
            user2 = User.objects.filter(username=row['email'].split("@")[0])
            if not (user or user2):
                if row['role'] == 'SA':
                    model = SuperAdminUser
                elif row['role'] == 'AA':
                    model = AreaAdminUser
                elif row['role'] == 'AP':
                    model = AreaAppraiserUser
                elif row['role'] == 'CA':
                    model = ContractorAppraiserUser
                else:
                    continue
                user = model(
                    email=row['email'],
                    role=row['role'],
                    username=row['email'].split("@")[0],
                    is_active=True,
                )
                user.save()
                user.set_password('zacasnogeslo')
                area = Area.objects.filter(name__icontains=row['area'])
                if area:
                    user.area.add(*list(area))
                user.save()

