from django.db import models
from ..base.models import BaseModel
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
import uuid
from ..base.emails import sendAccountActivationEmail


class Profile(BaseModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    isEmailVerified = models.BooleanField(default=False)
    emailToken = models.CharField(max_length=255, blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    forgetPasswordToken = models.CharField(max_length=100, null=True, blank=True)
    location = models.CharField(max_length=100, null=True, blank=True)
    phone = models.CharField(max_length=20, null=True, blank=True)

    def __str__(self):
        return self.user.username

class ProfileImage(BaseModel):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="profile_images")
    image = models.ImageField(upload_to='profile')

    def __str__(self):
        return f"Profile Image of {self.profile.user.username}"
    
class Cart(BaseModel):
    user = models.ForeignKey(User,on_delete=models.CASCADE, related_name='carts')
    isPaid = models.BooleanField(default=False)
    amount = models.IntegerField(null=True)
    
    def __str__(self):
        return f"Cart for {self.user.username}"


@receiver(post_save , sender = User)
def sendEmailToken(sender , instance , created , **kwargs):
    try:
        if created:
            emailToken = str(uuid.uuid4())
            Profile.objects.create(user = instance , emailToken = emailToken)
            email = instance.email
            sendAccountActivationEmail(email , emailToken)
    except Exception as e:
        print(e)