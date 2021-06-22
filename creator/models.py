from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from sort_order_field import SortOrderField


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
    name = models.CharField(max_length=100, default="", null=True)
    chatbot = models.ForeignKey(
        Chatbot,
        related_name='Chatbot',
        on_delete=models.CASCADE,
        default='',
        blank=True,
        null=True,
    )

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('intent-list', kwargs={'pk': self.pk})

    def save(self, *args, **kwargs):
        super(Intent, self).save(*args, **kwargs)


class Examples(models.Model):
    example = models.CharField(max_length=200, default="")
    intent = models.ManyToManyField(Intent)

    def __str__(self):
        return self.example

    def get_absolute_url(self):
        return reverse('examples-list', kwargs={'pk': self.pk})

    def save(self, *args, **kwargs):
        super(Examples, self).save(*args, **kwargs)


class Responses(models.Model):
    name = models.CharField(max_length=100, default="", null=True)
    response = models.CharField(max_length=100, default="", null=True)
    chatbot = models.ForeignKey(
        Chatbot,
        related_name='Chatbot_responses',
        on_delete=models.CASCADE,
        default='',
        blank=True,
        null=True,
    )

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('responses-list', kwargs={'pk': self.pk})

    def save(self, *args, **kwargs):
        super(Responses, self).save(*args, **kwargs)


class Story(models.Model):
    name = models.CharField(max_length=100, default="", null=True)
    chatbot = models.ForeignKey(
        Chatbot,
        related_name='Chatbot_story',
        on_delete=models.CASCADE,
        default='',
        blank=True,
        null=True,
    )

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('story-list', kwargs={'pk': self.pk})

    def save(self, *args, **kwargs):
        super(Story, self).save(*args, **kwargs)


class Steps(models.Model):
    intent = models.ForeignKey(Intent, on_delete=models.CASCADE)
    action = models.ForeignKey(Responses, on_delete=models.CASCADE)
    order = SortOrderField("Sort")
    story = models.ManyToManyField(Story)

    def __str__(self):
        return f'{self.intent.name} {self.action.name}'

    def get_absolute_url(self):
        return reverse('steps-list', kwargs={'pk': self.pk})

    def save(self, *args, **kwargs):
        super(Steps, self).save(*args, **kwargs)


