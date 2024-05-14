from django.contrib import admin
from .models import CustomUser, MailVerificationOTP

# Register your models here.
admin.site.register(CustomUser)
admin.site.register(MailVerificationOTP)