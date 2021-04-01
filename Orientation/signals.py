from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from Orientation.models import *


# @receiver(pre_save, sender=APOSRegion)
# def update_near(sender, instance, **kwargs):
#     instance.num = instance.length_near
#     pass
