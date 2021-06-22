from django.contrib import admin
from .models import Chatbot, Intent, Examples, Responses, Story, Steps


admin.site.register(Chatbot)
admin.site.register(Intent)
admin.site.register(Examples)
admin.site.register(Responses)
admin.site.register(Story)
admin.site.register(Steps)

