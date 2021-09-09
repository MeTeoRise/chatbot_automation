from django.contrib import admin
from .models import Chatbot, Intent, Examples, Responses, Story, Steps, Utterances, Rule, Action, Slot, Form


admin.site.register(Chatbot)
admin.site.register(Intent)
admin.site.register(Examples)
admin.site.register(Responses)
admin.site.register(Utterances)
admin.site.register(Story)
admin.site.register(Steps)
admin.site.register(Rule)
admin.site.register(Action)
admin.site.register(Slot)
admin.site.register(Form)


