from django.contrib.admin.models import LogEntry, ADDITION, CHANGE, DELETION
from django.contrib.auth.models import AnonymousUser 
from django.db import models
import uuid,  os
from django.db.models.signals import pre_save, post_save
from django.dispatch.dispatcher import receiver
from django.contrib.contenttypes.models import ContentType
import django.db.models.options as options

options.DEFAULT_NAMES = options.DEFAULT_NAMES + ('auto_populate', "number_elements_to_populate")

# Create your models here.


class BaseModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)
    deleted = models.BooleanField(default=False)
    protected = models.BooleanField(default=False)

    def __str__(self):
        return self.name
    
    class Meta:
        auto_populate = True
        ordering = ['-created_at']
        abstract = True
        number_elements_to_populate = 852


class Etat(models.Model):
    EN_COURS = 1
    TERMINE = 2
    ANNULE = 3

    name = models.CharField(max_length=255)
    etiquette = models.CharField(max_length=255)
    classe = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return self.name
