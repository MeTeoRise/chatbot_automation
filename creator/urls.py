from django.urls import path
from .views import ChatbotListView, ChatbotDetailView, ChatbotCreateView, ChatbotUpdateView, ChatbotDeleteView
from . import views

urlpatterns = [
    path('', ChatbotListView.as_view(), name='creator-home'),
    path('chatbot/<int:pk>', ChatbotDetailView.as_view(), name='chatbot-detail'),
    path('chatbot/create/', ChatbotCreateView.as_view(), name='chatbot-create'),
    path('chatbot/<int:pk>/update/', ChatbotUpdateView.as_view(), name='chatbot-update'),
    path('chatbot/<int:pk>/delete/', ChatbotDeleteView.as_view(), name='chatbot-delete'),
    path('about/', views.about, name='creator-about'),
]