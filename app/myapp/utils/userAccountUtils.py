from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils.translation import gettext_lazy

def send_mail(to, template, context):
    html_content = render_to_string(f'myapp/emails/{template}.html', context)
    text_content = render_to_string(f'myapp/emails/{template}.txt', context)

    msg = EmailMultiAlternatives(context['subject'], text_content, settings.DEFAULT_FROM_EMAIL, [to])
    msg.attach_alternative(html_content, 'text/html')
    msg.send()

def send_reset_password_email(request, email, token, uid):
    context = {
        'subject': gettext_lazy('Retrieve your password'),
        'uri': request.build_absolute_uri(
            reverse('retrieve_password_confirm', kwargs={'uidb64': uid, 'token': token})),
    }

    send_mail(email, 'retrieve_password_email', context)


def send_forgotten_username_email(email, username):
    context = {
        'subject': gettext_lazy('Your username'),
        'username': username,
    }

    send_mail(email, 'forgotten_username', context)