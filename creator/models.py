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


class Utterances(models.Model):
    text = models.CharField(max_length=200, default="")
    image = models.URLField(max_length=200, default="", null=True, blank=True)
    response = models.ManyToManyField(Responses)

    def __str__(self):
        return self.text

    def get_absolute_url(self):
        return reverse('utterances-list', kwargs={'pk': self.pk})

    def save(self, *args, **kwargs):
        super(Utterances, self).save(*args, **kwargs)


class Action(models.Model):
    name = models.CharField(max_length=100, default="")
    run_contents = models.TextField()
    chatbot = models.ForeignKey(
        Chatbot,
        related_name='Chatbot_action',
        on_delete=models.CASCADE,
        default='',
        blank=True,
        null=True,
    )

    def __str__(self):
        return f'{self.name}'

    def get_absolute_url(self):
        return reverse('actions-list', kwargs={'pk': self.pk})

    def save(self, *args, **kwargs):
        super(Action, self).save(*args, **kwargs)


class Form(models.Model):
    name = models.CharField(max_length=100, default="")
    intent = models.ForeignKey(Intent, on_delete=models.CASCADE)
    chatbot = models.ForeignKey(
        Chatbot,
        related_name='Chatbot_form',
        on_delete=models.CASCADE,
        default='',
        blank=True,
        null=True,
    )

    def __str__(self):
        return f'{self.name}'

    def get_absolute_url(self):
        return reverse('forms-list', kwargs={'pk': self.pk})

    def save(self, *args, **kwargs):
        super(Form, self).save(*args, **kwargs)


class Slot(models.Model):
    name = models.CharField(max_length=100, default="")
    type = models.CharField(max_length=100, default="")
    influence_conversation = models.BooleanField(default=False)
    value = models.CharField(max_length=150, default="")
    form = models.ManyToManyField(Form, blank=True)
    chatbot = models.ForeignKey(
        Chatbot,
        related_name='Chatbot_slot',
        on_delete=models.CASCADE,
        default='',
        blank=True,
        null=True,
    )

    def __str__(self):
        return f'{self.name}'

    def get_absolute_url(self):
        return reverse('slots-list', kwargs={'pk': self.pk})

    def save(self, *args, **kwargs):
        super(Slot, self).save(*args, **kwargs)


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
    intent = models.ForeignKey(Intent, on_delete=models.CASCADE, blank=True, null=True)
    response = models.ForeignKey(Responses, on_delete=models.CASCADE, blank=True, null=True)
    action = models.ForeignKey(Action, on_delete=models.CASCADE, blank=True, null=True)
    form = models.ForeignKey(Form, on_delete=models.CASCADE, blank=True, null=True)
    order = SortOrderField("Sort")
    story = models.ManyToManyField(Story)

    def __str__(self):
        return f'{self.intent.name} {self.action.name}'

    def get_absolute_url(self):
        return reverse('steps-list', kwargs={'pk': self.pk})

    def save(self, *args, **kwargs):
        super(Steps, self).save(*args, **kwargs)


class Rule(models.Model):
    name = models.CharField(max_length=100, default="")
    intent = models.ForeignKey(Intent, on_delete=models.CASCADE)
    action = models.ForeignKey(Responses, on_delete=models.CASCADE)
    chatbot = models.ForeignKey(
        Chatbot,
        related_name='Chatbot_rule',
        on_delete=models.CASCADE,
        default='',
        blank=True,
        null=True,
    )

    def __str__(self):
        return f'{self.intent.name} {self.action.name}'

    def get_absolute_url(self):
        return reverse('rules-list', kwargs={'pk': self.pk})

    def save(self, *args, **kwargs):
        super(Rule, self).save(*args, **kwargs)


