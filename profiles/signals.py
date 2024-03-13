import logging
from django.contrib.auth.models import User
from profiles.models import Profile, ProfileStatus
from django.db.models.signals import post_save
from django.dispatch import receiver


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    else:
        pass


@receiver(post_save, sender=Profile)
def create_profile_status_message(sender, instance, created, **kwargs):
    if created:
        ProfileStatus.objects.create(
            user_profile=instance,
            status_message=f"{instance.user.username} joined club",
        )
    else:
        pass
