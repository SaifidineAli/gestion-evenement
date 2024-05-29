from django.db import models
from django.contrib.auth.models import AbstractUser
from PIL import Image


class User(AbstractUser):
    profile_photo = models.ImageField(upload_to='profile_photos/', verbose_name='Photo de profil', null=True, blank=True)
    
    IMAGE_MAX_SIZE = (800, 800)
    
    def resize_image(self):
        if self.profile_photo:
            image = Image.open(self.profile_photo)
            image.thumbnail(self.IMAGE_MAX_SIZE)
            image.save(self.profile_photo.path)
        
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.resize_image()