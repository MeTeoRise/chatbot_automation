from django.urls import path
from .views import ChatbotListView, ChatbotDetailView, ChatbotCreateView, ChatbotUpdateView, ChatbotDeleteView, \
    IntentUpdateView, IntentListView, IntentCreateView, IntentDeleteView, \
    ExamplesListView, UpdateExamples, ExamplesCreateView, ExamplesDeleteView, \
    ResponsesUpdateView, ResponsesListView, ResponsesCreateView, ResponsesDeleteView, \
    StoryListView, StoryUpdateView, StoryCreateView, StoryDeleteView, \
    StepsListView, StepsCreateView, StepsDeleteView, UpdateSteps
from . import views

urlpatterns = [
    path('', ChatbotListView.as_view(), name='creator-home'),
    path('chatbot/<int:pk>', ChatbotDetailView.as_view(), name='chatbot-detail'),
    path('chatbot/create/', ChatbotCreateView.as_view(), name='chatbot-create'),
    path('chatbot/<int:pk>/update/', ChatbotUpdateView.as_view(), name='chatbot-update'),
    path('chatbot/<int:pk>/delete/', ChatbotDeleteView.as_view(), name='chatbot-delete'),
    path('about/', views.about, name='creator-about'),
    path('chatbot/<int:pk>/intents/', IntentListView.as_view(), name='intent-list'),
    path('chatbot/<int:pk>/intents/create/', IntentCreateView.as_view(), name='intent-create'),
    path('chatbot/intent/delete/<int:pk>/', IntentDeleteView.as_view(), name='intent-delete'),
    path('chatbot/<int:pk>/intents/update/', IntentUpdateView.as_view(), name='intent-update'),
    path('chatbot/intent/<int:pk>/examples/', ExamplesListView.as_view(), name='examples-list'),
    path('chatbot/intents/update/<int:pk>/', UpdateExamples.as_view(), name='examples-update'),
    path('chatbot/intent/<int:pk>/examples/create/', ExamplesCreateView.as_view(), name='examples-create'),
    path('chatbot/intent/examples/delete/<int:pk>/', ExamplesDeleteView.as_view(), name='examples-delete'),
    path('chatbot/<int:pk>/responses/', ResponsesListView.as_view(), name='responses-list'),
    path('chatbot/<int:pk>/responses/create/', ResponsesCreateView.as_view(), name='responses-create'),
    path('chatbot/response/delete/<int:pk>/', ResponsesDeleteView.as_view(), name='responses-delete'),
    path('chatbot/<int:pk>/responses/update/', ResponsesUpdateView.as_view(), name='responses-update'),
    path('chatbot/<int:pk>/stories/', StoryListView.as_view(), name='story-list'),
    path('chatbot/<int:pk>/stories/create/', StoryCreateView.as_view(), name='story-create'),
    path('chatbot/story/delete/<int:pk>/', StoryDeleteView.as_view(), name='story-delete'),
    path('chatbot/<int:pk>/stories/update/', StoryUpdateView.as_view(), name='story-update'),
    path('chatbot/story/<int:pk>/steps/', StepsListView.as_view(), name='steps-list'),
    path('chatbot/story/update/<int:pk>/', UpdateSteps.as_view(), name='steps-update'),
    path('chatbot/story/<int:pk>/steps/create/', StepsCreateView.as_view(), name='steps-create'),
    path('chatbot/story/steps/delete/<int:pk>/', StepsDeleteView.as_view(), name='steps-delete'),
    path('chatbot/train/<int:pk>', views.training, name='chatbot-train'),
    path('chatbot/test/<int:pk>', views.testing, name='chatbot-test'),
    path('chatbot/download/<int:pk>', views.downloading, name='chatbot-download'),
]

#path('chatbot/intent/<int:pk>', IntentUpdateView.as_view(), name='intent-update'),
#path('chatbot/intent/<int:pk>', IntentDetailView.as_view(), name='intent-detail'),
