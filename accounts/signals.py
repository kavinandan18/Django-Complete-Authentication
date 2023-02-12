from django.db.models.signals import post_save
from django.contrib.auth.models import Group
from django.dispatch import receiver
from .models import Profile
from django.contrib.auth import get_user_model

User = get_user_model()

@receiver(post_save,sender=User)
def User_Profile_group_Creation(sender,instance,created,**kwargs):
    if created:
        user_group,created = Group.objects.get_or_create(name='User')
        instance.groups.add(user_group)
        Profile.objects.create(user = instance)
