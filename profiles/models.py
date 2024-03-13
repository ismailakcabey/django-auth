from django.db import models
from django.contrib.auth.models import User
from PIL import Image

# Create your models here.


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    bio = models.TextField(blank=True, null=True)
    city = models.TextField(blank=True, null=True)
    photo = models.ImageField(blank=True, null=True, upload_to="profiles_photos/%Y-%m")

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        # image resize
        if self.photo:
            img = Image.open(self.photo.path)
            if img.height > 600 or img.width > 600:
                output_size = (600, 600)
                img.thumbnail(output_size)
                img.save(self.photo.path)

    class Meta:
        verbose_name_plural = "Profile"

    def __str__(self) -> str:
        return self.user.username


class ProfileStatus(models.Model):
    user_profile = models.ForeignKey(
        Profile, on_delete=models.CASCADE, related_name="profile_status"
    )
    status_message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Profile_Status"

    def __str__(self) -> str:
        return str(self.user_profile)
