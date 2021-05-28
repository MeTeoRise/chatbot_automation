from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse


class Chatbot(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    date_created = models.DateTimeField(default=timezone.now)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('chatbot-detail', kwargs={'pk': self.pk})

