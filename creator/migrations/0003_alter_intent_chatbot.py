# Generated by Django 3.2 on 2021-06-19 09:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('creator', '0002_examples_intent'),
    ]

    operations = [
        migrations.AlterField(
            model_name='intent',
            name='chatbot',
            field=models.ForeignKey(blank=True, default='', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='Chatbot', to='creator.chatbot'),
        ),
    ]
