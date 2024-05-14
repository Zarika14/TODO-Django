from .models import  MailVerificationOTP
import random


# to send mail
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.tokens import default_token_generator
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.urls import reverse

def send_password_reset_link(user):
    """
    Send a password reset link to the user's email address.
    """
    token = default_token_generator.make_token(user)
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    reset_url = reverse('password_reset_confirm', kwargs={'uidb64': uid, 'token': token})
    reset_link = f"http://127.0.0.1:8000{reset_url}"  # Replace with your actual domain
    subject = "Password Reset"
    message = render_to_string('password_reset_email.html', {
        'user': user,
        'reset_link': reset_link,
    })
    user.email_user(subject, message)





def send_otp_for_mail_verification(otp, user):
        send_mail(
                'Mail Verification',
                f'Hii  {user.username},\n\n\n\nYour OTP:   {otp}\n\nOTP will expire after 30 minutes.\n\nThankyou',
                settings.EMAIL_HOST_USER,
                [user.email], 
                fail_silently=True)
    
def get_otp_for_mail_verification(user):
      otp = random.randint(1001, 9999)

      if MailVerificationOTP.objects.filter(user = user.id).exists():
         otp_obj = MailVerificationOTP.objects.get(user = user.id)
         otp_obj.otp = otp
         otp_obj.save()

      else :  
        otp_obj = MailVerificationOTP(otp = otp, user = user)
        otp_obj.save()

      return otp
  
  