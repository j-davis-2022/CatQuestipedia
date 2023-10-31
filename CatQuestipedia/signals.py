from django.db.models.signals import pre_save
from django.dispatch import receiver
from .models import *

@receiver(pre_save, sender=Characters)
def edit_page(sender, instance, **kwargs):
    print("The " + str(instance) + " page has been edited.")
