from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Chatbot, Intent, Story


@receiver(post_save, sender=Chatbot)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Intent.objects.create(chatbot=instance)
        Story.objects.create(chatbot=instance)


@receiver(post_save, sender=Chatbot)
def save_profile(sender, instance, **kwargs):
    instance.intent.save()
    instance.story.save()
