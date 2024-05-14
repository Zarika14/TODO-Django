from uuid import UUID
from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid

# Create your models here.
class CustomUser(AbstractUser): 
    
    id = models.UUIDField(
        default=uuid.uuid4, editable=False, db_index=True, primary_key=True
    )
    username = models.CharField(max_length = 50)
    email = models.EmailField(unique=True, null = False, blank = False)
    is_verified = models.BooleanField(default = False)
    
    

    # password in serializer
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.username
    
# Define related_name arguments for groups and user_permissions
CustomUser._meta.get_field('groups').remote_field.related_name = 'custom_user_groups'
CustomUser._meta.get_field('user_permissions').remote_field.related_name = 'custom_user_permissions'    

class MailVerificationOTP(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, unique=True)
    otp = models.PositiveIntegerField(null=True, blank=False)
    updated_at = models.DateTimeField(auto_now=True)
    