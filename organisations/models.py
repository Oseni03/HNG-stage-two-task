from django.db import models
from django.conf import settings


# Create your models here.
class Organisation(models.Model):
    name = models.CharField(max_length=150)
    description = models.TextField()
    users = models.ManyToManyField(
        settings.AUTH_USER_MODEL, related_name="organisations"
    )
