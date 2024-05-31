from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from .models import *
from django.conf import settings
from .serializers import *
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMultiAlternatives
from django.utils.translation import gettext_lazy as _
from django.utils.html import strip_tags


class ContactMessageView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        email = request.data.get('email')
        name = request.data.get('name')
        message = request.data.get('message')

        if not email:
            return Response({'error': _('Email is required.')}, status=status.HTTP_400_BAD_REQUEST)
        if not name:
            return Response({'error': _('Name is required.')}, status=status.HTTP_400_BAD_REQUEST)
        if not message:
            return Response({'error': _('Message is required.')}, status=status.HTTP_400_BAD_REQUEST)

        contact_message = ContactMessage.objects.create(email=email, name=name, message=message)
        
        email = email
        current_site = get_current_site(self.request)
        subject = 'Thank you, your message has been received'
        html_message = render_to_string('users/contact.html', {
                'user': name,
                'domain': current_site.domain,
                'site_name': settings.SITE_NAME,
            })
        from_email = 'zlidementorled@gmail.com'
        plain_message = strip_tags(html_message)
        to_email = email

        email = EmailMultiAlternatives(subject, plain_message, from_email, [to_email])
        email.attach_alternative(html_message, "text/html")
        email.send()

        return Response({'message': _('Contact message received.')}, status=status.HTTP_200_OK)
    
