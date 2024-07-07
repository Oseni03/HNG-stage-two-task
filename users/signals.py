from django.db.models.signals import post_save
from django.dispatch import receiver

from organisations.models import Organisation

from .models import User


@receiver(post_save, sender=User)
def user_default_organisation(sender, instance, created, **kwargs):
    if created:
        org = Organisation.objects.create(name=f"{instance.first_name.strip()}'s organisation")
        instance.organisations.add(org)
        instance.save()