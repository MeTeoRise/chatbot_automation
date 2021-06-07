from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from yamlfield.fields import YAMLField
from .utils import read_default_intents, read_default_stories


class Chatbot(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    date_created = models.DateTimeField(default=timezone.now)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('chatbot-detail', kwargs={'pk': self.pk})


class Intent(models.Model):
    yaml = YAMLField(default=read_default_intents())
    chatbot = models.OneToOneField(
        Chatbot,
        on_delete=models.CASCADE,
        primary_key=True,
        default="",
    )

    def __str__(self):
        return self.chatbot.name

    def get_absolute_url(self):
        return reverse('intent-update', kwargs={'pk': self.pk})

    def save(self, *args, **kwargs):
        super(Intent, self).save(*args, **kwargs)


class Story(models.Model):
    yaml = YAMLField(default=read_default_stories())
    chatbot = models.OneToOneField(
        Chatbot,
        on_delete=models.CASCADE,
        primary_key=True,
        default="",
    )

    def __str__(self):
        return self.chatbot.name

    def get_absolute_url(self):
        return reverse('story-update', kwargs={'pk': self.pk})

    def save(self, *args, **kwargs):
        super(Story, self).save(*args, **kwargs)

"""
class Entity(models.Model):
    name = models.CharField(max_length=100, default="")
    intent = models.ForeignKey(Intent, on_delete=models.CASCADE)
    content = models.TextField()

    def __str__(self):
        return self.name
"""

