from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from .models import Book, UserClone, CustomUser
from django.contrib.auth import get_user_model


User = get_user_model()

@receiver(post_save, sender=Book)
def notify_book_creation(sender, instance, created, **kwargs):
    if created:
        print(f"New Book added: {instance.title} by {instance.author}")

@receiver(post_save, sender=User)
def notify_user_creation(sender, instance, created, **kwargs):
    if created:
        print(f"New User added: {instance.id} username is {instance.username}")

@receiver(post_save, sender=User)
def created_user_clone(sender, instance, created, **kwargs):
    if created:
        UserClone.objects.create(username=instance.username)
        print(f"UserClone entry created for: {instance.username}")


@receiver(post_save, sender=User)
def modify_username_before_save(sender, instance, **kwargs):
    instance.username = instance.username.upper()  # Capitalize username
    print(f"modified username for user {instance.username}")

import random
@receiver(post_save, sender=User)
def modify_uniquefield_in_customuser(sender, instance, created, **kwargs):
    if created:
        count = len(CustomUser.objects.all())
        get_previous_username = CustomUser.objects.all()[count-1].username
        CustomUser.objects.create(username=instance.username, unique_id=instance.username)
        print(f"entry for username: {instance.username} is saved in CustomUser table")