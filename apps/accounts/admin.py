from django.contrib import admin
from .models import Profile, ProfileImage, Address

admin.site.register(Address)
admin.site.register(Profile)
admin.site.register(ProfileImage)