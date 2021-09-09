from django.urls import path
from .views import ChatbotListView, ChatbotDetailView, ChatbotCreateView, ChatbotUpdateView, ChatbotDeleteView, \
    IntentUpdateView, IntentListView, IntentCreateView, IntentDeleteView, \
    ExamplesListView, UpdateExamples, ExamplesCreateView, ExamplesDeleteView, \
    ResponsesUpdateView, ResponsesListView, ResponsesCreateView, ResponsesDeleteView, \
    StoryListView, StoryUpdateView, StoryCreateView, StoryDeleteView, \
    StepsListView, StepsCreateView, StepsDeleteView, UpdateSteps, \
    UtterancesListView, UtterancesCreateView, UtterancesDeleteView, UpdateUtterances, \
    RulesListView, RulesUpdateView, RulesDeleteView, RuleCreateView, \
    ActionsListView, ActionsUpdateView, ActionCreateView, ActionsDeleteView, \
    SlotsUpdateView, SlotsDeleteView, SlotsListView, SlotCreateView, \
    FormsUpdateView, FormsDeleteView, FormsListView, FormCreateView
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

    path('chatbot/response/<int:pk>/utterances/', UtterancesListView.as_view(), name='utterances-list'),
    path('chatbot/response/update/<int:pk>/', UpdateUtterances.as_view(), name='utterances-update'),
    path('chatbot/story/<int:pk>/utterances/create/', UtterancesCreateView.as_view(), name='utterances-create'),
    path('chatbot/story/utterances/delete/<int:pk>/', UtterancesDeleteView.as_view(), name='utterances-delete'),

    path('chatbot/<int:pk>/stories/', StoryListView.as_view(), name='story-list'),
    path('chatbot/<int:pk>/stories/create/', StoryCreateView.as_view(), name='story-create'),
    path('chatbot/story/delete/<int:pk>/', StoryDeleteView.as_view(), name='story-delete'),
    path('chatbot/<int:pk>/stories/update/', StoryUpdateView.as_view(), name='story-update'),

    path('chatbot/story/<int:pk>/steps/', StepsListView.as_view(), name='steps-list'),
    path('chatbot/story/update/<int:pk>/', UpdateSteps.as_view(), name='steps-update'),
    path('chatbot/story/<int:pk>/steps/create/', StepsCreateView.as_view(), name='steps-create'),
    path('chatbot/story/steps/delete/<int:pk>/', StepsDeleteView.as_view(), name='steps-delete'),

    path('chatbot/<int:pk>/rules/', RulesListView.as_view(), name='rules-list'),
    path('chatbot/<int:pk>/rules/create/', RuleCreateView.as_view(), name='rules-create'),
    path('chatbot/rule/delete/<int:pk>/', RulesDeleteView.as_view(), name='rules-delete'),
    path('chatbot/<int:pk>/rules/update/', RulesUpdateView.as_view(), name='rules-update'),

    path('chatbot/<int:pk>/actions/', ActionsListView.as_view(), name='actions-list'),
    path('chatbot/<int:pk>/actions/create/', ActionCreateView.as_view(), name='actions-create'),
    path('chatbot/action/delete/<int:pk>/', ActionsDeleteView.as_view(), name='actions-delete'),
    path('chatbot/<int:pk>/actions/update/', ActionsUpdateView.as_view(), name='actions-update'),

    path('chatbot/<int:pk>/slots/', SlotsListView.as_view(), name='slots-list'),
    path('chatbot/<int:pk>/slots/create/', SlotCreateView.as_view(), name='slots-create'),
    path('chatbot/slot/delete/<int:pk>/', SlotsDeleteView.as_view(), name='slots-delete'),
    path('chatbot/<int:pk>/slots/update/', SlotsUpdateView.as_view(), name='slots-update'),

    path('chatbot/<int:pk>/forms/', FormsListView.as_view(), name='forms-list'),
    path('chatbot/<int:pk>/forms/create/', FormCreateView.as_view(), name='forms-create'),
    path('chatbot/form/delete/<int:pk>/', FormsDeleteView.as_view(), name='forms-delete'),
    path('chatbot/<int:pk>/forms/update/', FormsUpdateView.as_view(), name='forms-update'),

    path('chatbot/train/<int:pk>', views.training, name='chatbot-train'),
    path('chatbot/test/<int:pk>', views.testing, name='chatbot-test'),
    path('chatbot/download/<int:pk>', views.downloading, name='chatbot-download'),
]
