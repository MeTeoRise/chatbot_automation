from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.utils.encoding import smart_str
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.http import HttpResponse, FileResponse
from .models import Chatbot, Intent, Examples, Responses, Story, Steps, Utterances, Rule, Action, Slot, Form
from .utils import chatbot_create, chatbot_delete, chatbot_train, chatbot_start, chatbot_stop
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from extra_views import ModelFormSetView
import shutil
import os


def home(request):
    context = {
        'chatbots': Chatbot.objects.all()
    }
    return render(request, 'creator/home.html', context)


def about(request):
    return render(request, 'creator/about.html')


class ChatbotListView(LoginRequiredMixin, ListView):
    model = Chatbot
    template_name = 'creator/home.html'
    context_object_name = 'chatbots'
    ordering = ['-date_created']

    def get_queryset(self):
        return Chatbot.objects.filter(user=self.request.user)


class ChatbotDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = Chatbot

    def test_func(self):
        chatbot = self.get_object()
        if self.request.user == chatbot.user:
            return True
        return False

    def dispatch(self, request, *args, **kwargs):
        chatbot_stop()
        return super(ChatbotDetailView, self).dispatch(request, *args, **kwargs)


class ChatbotCreateView(LoginRequiredMixin, CreateView):
    model = Chatbot
    fields = ['name', 'description']

    def form_valid(self, form):
        messages.success(self.request, "Chatbot was created successfully.")
        form.instance.user = self.request.user
        name = form.cleaned_data['name']
        chatbot_create(name)
        return super().form_valid(form)


class ChatbotUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Chatbot
    fields = ['name', 'description']

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def test_func(self):
        chatbot = self.get_object()
        if self.request.user == chatbot.user:
            return True
        return False


class ChatbotDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Chatbot
    success_url = '/'

    success_message = "Chatbot was deleted successfully."

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, self.success_message)
        obj = self.get_object()
        chatbot_delete(obj.name)
        return super(ChatbotDeleteView, self).delete(request, *args, **kwargs)

    def test_func(self):
        chatbot = self.get_object()
        if self.request.user == chatbot.user:
            return True
        return False


class IntentListView(LoginRequiredMixin, ListView):
    model = Intent

    def get_queryset(self):
        return Intent.objects.filter(chatbot_id = self.kwargs['pk'])

    def get_context_data(self, **kwargs):
        context = super(IntentListView, self).get_context_data(**kwargs)
        context['prim_key'] = self.kwargs['pk']
        return context


class IntentCreateView(LoginRequiredMixin, CreateView):
    model = Intent
    fields = ['name', 'chatbot']

    def form_valid(self, form):
        messages.success(self.request, "Intent was created successfully.")
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('intent-list', kwargs={'pk': self.object.chatbot.pk})

    def get_context_data(self, **kwargs):
        context = super(IntentCreateView, self).get_context_data(**kwargs)
        context['prim_key'] = self.kwargs['pk']
        return context


class IntentDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Intent

    def get_success_url(self):
        return reverse('intent-list', kwargs={'pk': self.object.chatbot.pk})

    success_message = "Intent was deleted successfully."

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, self.success_message)
        return super(IntentDeleteView, self).delete(request, *args, **kwargs)

    def test_func(self):
        intent = self.get_object()
        if self.request.user == intent.chatbot.user:
            return True
        return False

    def get_context_data(self, **kwargs):
        context = super(IntentDeleteView, self).get_context_data(**kwargs)
        intent = get_object_or_404(Intent, pk=self.kwargs['pk'])
        chatbot = get_object_or_404(Chatbot, pk=intent.chatbot.pk)
        context['prim_key'] = chatbot.pk
        return context


class IntentDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = Intent

    def test_func(self):
        intent = self.get_object()
        if self.request.user == intent.chatbot.user:
            return True
        return False

    def get_queryset(self):
        intent = get_object_or_404(Intent, pk=self.kwargs['pk'])
        chatbot = get_object_or_404(Chatbot, pk=intent.chatbot.pk)
        intent = Intent.objects.filter(chatbot_id=chatbot.pk)
        return intent


class IntentUpdateView(LoginRequiredMixin, ModelFormSetView):
    model = Intent
    template_name = 'creator/intent_update.html'
    fields = ['name', 'chatbot']

    def get_queryset(self):
        intent = Intent.objects.filter(chatbot_id=self.kwargs['pk'])
        return intent

    def get_context_data(self, **kwargs):
        context = super(IntentUpdateView, self).get_context_data(**kwargs)
        context['prim_key'] = self.kwargs['pk']
        return context


class ExamplesListView(LoginRequiredMixin, ListView):
    model = Examples

    def get_queryset(self):
        return Examples.objects.filter(intent=self.kwargs['pk'])

    def get_context_data(self, **kwargs):
        context = super(ExamplesListView, self).get_context_data(**kwargs)
        intent = get_object_or_404(Intent, pk=self.kwargs['pk'])
        chatbot = get_object_or_404(Chatbot, pk=intent.chatbot.pk)
        context['prim_key'] = chatbot.pk
        context['url_key'] = self.kwargs['pk']
        return context


class UpdateExamples(ModelFormSetView):
    model = Examples
    template_name = 'creator/example_update.html'
    fields = ['example', 'intent']

    def get_queryset(self):
        examples = Examples.objects.filter(intent=self.kwargs['pk'])
        return examples

    def get_context_data(self, **kwargs):
        context = super(UpdateExamples, self).get_context_data(**kwargs)
        intent = get_object_or_404(Intent, pk=self.kwargs['pk'])
        context['prim_key'] = intent.pk
        return context


class ExamplesCreateView(LoginRequiredMixin, CreateView):
    model = Examples
    fields = ['example', 'intent']

    def form_valid(self, form):
        messages.success(self.request, "Example was created successfully.")
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_success_url(self, **kwargs):
        return reverse('examples-list', kwargs={'pk': self.kwargs['pk']})

    def get_context_data(self, **kwargs):
        context = super(ExamplesCreateView, self).get_context_data(**kwargs)
        context['prim_key'] = self.kwargs['pk']
        return context


class ExamplesDeleteView(LoginRequiredMixin, DeleteView):
    model = Examples

    def get_success_url(self):
        return reverse('examples-list', kwargs={'pk': self.object.intent.all()[0].pk})

    success_message = "Example was deleted successfully."

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, self.success_message)
        return super(ExamplesDeleteView, self).delete(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(ExamplesDeleteView, self).get_context_data(**kwargs)
        example = get_object_or_404(Examples, pk=self.kwargs['pk'])
        intent = get_object_or_404(Intent, pk=example.intent.all()[0].pk)
        context['prim_key'] = intent.pk
        context['url_key'] = example.pk
        return context


class ResponsesListView(LoginRequiredMixin, ListView):
    model = Responses

    def get_queryset(self):
        return Responses.objects.filter(chatbot_id=self.kwargs['pk'])

    def get_context_data(self, **kwargs):
        context = super(ResponsesListView, self).get_context_data(**kwargs)
        context['prim_key'] = self.kwargs['pk']
        return context


class ResponsesCreateView(LoginRequiredMixin, CreateView):
    model = Responses
    fields = ['name', 'chatbot']

    def form_valid(self, form):
        messages.success(self.request, "Response was created successfully.")
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('responses-list', kwargs={'pk': self.object.chatbot.pk})

    def get_context_data(self, **kwargs):
        context = super(ResponsesCreateView, self).get_context_data(**kwargs)
        context['prim_key'] = self.kwargs['pk']
        return context


class ResponsesDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Responses

    def get_success_url(self):
        return reverse('responses-list', kwargs={'pk': self.object.chatbot.pk})

    success_message = "Responses was deleted successfully."

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, self.success_message)
        return super(ResponsesDeleteView, self).delete(request, *args, **kwargs)

    def test_func(self):
        response = self.get_object()
        if self.request.user == response.chatbot.user:
            return True
        return False

    def get_context_data(self, **kwargs):
        context = super(ResponsesDeleteView, self).get_context_data(**kwargs)
        response = get_object_or_404(Responses, pk=self.kwargs['pk'])
        chatbot = get_object_or_404(Chatbot, pk=response.chatbot.pk)
        context['prim_key'] = chatbot.pk
        return context


class ResponsesUpdateView(LoginRequiredMixin, ModelFormSetView):
    model = Responses
    template_name = 'creator/responses_update.html'
    fields = ['name', 'chatbot']

    def get_queryset(self):
        response = Responses.objects.filter(chatbot_id=self.kwargs['pk'])
        return response

    def get_context_data(self, **kwargs):
        context = super(ResponsesUpdateView, self).get_context_data(**kwargs)
        context['prim_key'] = self.kwargs['pk']
        return context


class UtterancesListView(LoginRequiredMixin, ListView):
    model = Utterances

    def get_queryset(self):
        return Utterances.objects.filter(response=self.kwargs['pk'])

    def get_context_data(self, **kwargs):
        context = super(UtterancesListView, self).get_context_data(**kwargs)
        response = get_object_or_404(Responses, pk=self.kwargs['pk'])
        chatbot = get_object_or_404(Chatbot, pk=response.chatbot.pk)
        context['prim_key'] = chatbot.pk
        context['url_key'] = self.kwargs['pk']
        return context


class UpdateUtterances(ModelFormSetView):
    model = Utterances
    template_name = 'creator/utterances_update.html'
    fields = ['text', 'image', 'response']

    def get_queryset(self):
        utterances = Utterances.objects.filter(response=self.kwargs['pk'])
        return utterances

    def get_context_data(self, **kwargs):
        context = super(UpdateUtterances, self).get_context_data(**kwargs)
        response = get_object_or_404(Responses, pk=self.kwargs['pk'])
        context['prim_key'] = response.pk
        return context


class UtterancesCreateView(LoginRequiredMixin, CreateView):
    model = Utterances
    fields = ['text', 'image', 'response']

    def form_valid(self, form):
        messages.success(self.request, "Utterance was created successfully.")
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_success_url(self, **kwargs):
        return reverse('utterances-list', kwargs={'pk': self.kwargs['pk']})

    def get_context_data(self, **kwargs):
        context = super(UtterancesCreateView, self).get_context_data(**kwargs)
        context['prim_key'] = self.kwargs['pk']
        return context


class UtterancesDeleteView(LoginRequiredMixin, DeleteView):
    model = Utterances

    def get_success_url(self):
        return reverse('utterances-list', kwargs={'pk': self.object.response.all()[0].pk})

    success_message = "Utterance was deleted successfully."

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, self.success_message)
        return super(UtterancesDeleteView, self).delete(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(UtterancesDeleteView, self).get_context_data(**kwargs)
        utterance = get_object_or_404(Utterances, pk=self.kwargs['pk'])
        response = get_object_or_404(Responses, pk=utterance.response.all()[0].pk)
        context['prim_key'] = response.pk
        context['url_key'] = utterance.pk
        return context


class StoryListView(LoginRequiredMixin, ListView):
    model = Story

    def get_queryset(self):
        return Story.objects.filter(chatbot_id=self.kwargs['pk'])

    def get_context_data(self, **kwargs):
        context = super(StoryListView, self).get_context_data(**kwargs)
        context['prim_key'] = self.kwargs['pk']
        return context


class StoryCreateView(LoginRequiredMixin, CreateView):
    model = Story
    fields = ['name', 'chatbot']

    def form_valid(self, form):
        messages.success(self.request, "Story was created successfully.")
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('story-list', kwargs={'pk': self.object.chatbot.pk})

    def get_context_data(self, **kwargs):
        context = super(StoryCreateView, self).get_context_data(**kwargs)
        context['prim_key'] = self.kwargs['pk']
        return context


class StoryDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Story

    def get_success_url(self):
        return reverse('story-list', kwargs={'pk': self.object.chatbot.pk})

    success_message = "Story was deleted successfully."

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, self.success_message)
        return super(StoryDeleteView, self).delete(request, *args, **kwargs)

    def test_func(self):
        story = self.get_object()
        if self.request.user == story.chatbot.user:
            return True
        return False

    def get_context_data(self, **kwargs):
        context = super(StoryDeleteView, self).get_context_data(**kwargs)
        story = get_object_or_404(Intent, pk=self.kwargs['pk'])
        chatbot = get_object_or_404(Chatbot, pk=story.chatbot.pk)
        context['prim_key'] = chatbot.pk
        return context


class StoryDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = Story

    def test_func(self):
        story = self.get_object()
        if self.request.user == story.chatbot.user:
            return True
        return False

    def get_queryset(self):
        story = get_object_or_404(Story, pk=self.kwargs['pk'])
        chatbot = get_object_or_404(Chatbot, pk=story.chatbot.pk)
        story = Story.objects.filter(chatbot_id=chatbot.pk)
        return story


class StoryUpdateView(LoginRequiredMixin, ModelFormSetView):
    model = Story
    template_name = 'creator/story_update.html'
    fields = ['name', 'chatbot']

    def get_queryset(self):
        story = Story.objects.filter(chatbot_id=self.kwargs['pk'])
        return story

    def get_context_data(self, **kwargs):
        context = super(StoryUpdateView, self).get_context_data(**kwargs)
        context['prim_key'] = self.kwargs['pk']
        return context


class StepsListView(LoginRequiredMixin, ListView):
    model = Steps

    def get_queryset(self):
        return Steps.objects.filter(story=self.kwargs['pk']).order_by('order')

    def get_context_data(self, **kwargs):
        context = super(StepsListView, self).get_context_data(**kwargs)
        story = get_object_or_404(Story, pk=self.kwargs['pk'])
        chatbot = get_object_or_404(Chatbot, pk=story.chatbot.pk)
        context['prim_key'] = chatbot.pk
        context['url_key'] = self.kwargs['pk']
        return context


class UpdateSteps(ModelFormSetView):
    model = Steps
    template_name = 'creator/steps_update.html'
    fields = ['intent', 'response', 'action', 'form', 'order', 'story']

    def get_queryset(self):
        steps = Steps.objects.filter(story=self.kwargs['pk']).order_by('order')
        return steps

    def get_context_data(self, **kwargs):
        context = super(UpdateSteps, self).get_context_data(**kwargs)
        story = get_object_or_404(Story, pk=self.kwargs['pk'])
        context['prim_key'] = story.pk
        return context


class StepsCreateView(LoginRequiredMixin, CreateView):
    model = Steps
    fields = ['intent', 'response', 'action', 'form', 'order', 'story']

    def form_valid(self, form):
        messages.success(self.request, "Step was created successfully.")
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_success_url(self, **kwargs):
        return reverse('steps-list', kwargs={'pk': self.kwargs['pk']})

    def get_context_data(self, **kwargs):
        context = super(StepsCreateView, self).get_context_data(**kwargs)
        context['prim_key'] = self.kwargs['pk']
        return context


class StepsDeleteView(LoginRequiredMixin, DeleteView):
    model = Steps

    def get_success_url(self):
        return reverse('steps-list', kwargs={'pk': self.object.story.all()[0].pk})

    success_message = "Step was deleted successfully."

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, self.success_message)
        return super(StepsDeleteView, self).delete(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(StepsDeleteView, self).get_context_data(**kwargs)
        step = get_object_or_404(Steps, pk=self.kwargs['pk'])
        story = get_object_or_404(Story, pk=step.story.all()[0].pk)
        context['prim_key'] = story.pk
        context['url_key'] = step.pk
        return context


class RulesListView(LoginRequiredMixin, ListView):
    model = Rule

    def get_queryset(self):
        return Rule.objects.filter(chatbot_id=self.kwargs['pk'])

    def get_context_data(self, **kwargs):
        context = super(RulesListView, self).get_context_data(**kwargs)
        context['prim_key'] = self.kwargs['pk']
        return context


class RuleCreateView(LoginRequiredMixin, CreateView):
    model = Rule
    fields = ['name', 'intent', 'action', 'chatbot']

    def form_valid(self, form):
        messages.success(self.request, "Rule was created successfully.")
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('rules-list', kwargs={'pk': self.object.chatbot.pk})

    def get_context_data(self, **kwargs):
        context = super(RuleCreateView, self).get_context_data(**kwargs)
        context['prim_key'] = self.kwargs['pk']
        return context


class RulesDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Rule

    def get_success_url(self):
        return reverse('rules-list', kwargs={'pk': self.object.chatbot.pk})

    success_message = "Rule was deleted successfully."

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, self.success_message)
        return super(RulesDeleteView, self).delete(request, *args, **kwargs)

    def test_func(self):
        rule = self.get_object()
        if self.request.user == rule.chatbot.user:
            return True
        return False

    def get_context_data(self, **kwargs):
        context = super(RulesDeleteView, self).get_context_data(**kwargs)
        rule = get_object_or_404(Rule, pk=self.kwargs['pk'])
        chatbot = get_object_or_404(Chatbot, pk=rule.chatbot.pk)
        context['prim_key'] = chatbot.pk
        return context


class RulesUpdateView(LoginRequiredMixin, ModelFormSetView):
    model = Rule
    template_name = 'creator/rule_update.html'
    fields = ['name', 'intent', 'action', 'chatbot']

    def get_queryset(self):
        rule = Rule.objects.filter(chatbot_id=self.kwargs['pk'])
        return rule

    def get_context_data(self, **kwargs):
        context = super(RulesUpdateView, self).get_context_data(**kwargs)
        context['prim_key'] = self.kwargs['pk']
        return context


class ActionsListView(LoginRequiredMixin, ListView):
    model = Action

    def get_queryset(self):
        return Action.objects.filter(chatbot_id=self.kwargs['pk'])

    def get_context_data(self, **kwargs):
        context = super(ActionsListView, self).get_context_data(**kwargs)
        context['prim_key'] = self.kwargs['pk']
        return context


class ActionCreateView(LoginRequiredMixin, CreateView):
    model = Action
    fields = ['name', 'run_contents', 'chatbot']

    def form_valid(self, form):
        messages.success(self.request, "Action was created successfully.")
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('actions-list', kwargs={'pk': self.object.chatbot.pk})

    def get_context_data(self, **kwargs):
        context = super(ActionCreateView, self).get_context_data(**kwargs)
        context['prim_key'] = self.kwargs['pk']
        return context


class ActionsDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Action

    def get_success_url(self):
        return reverse('actions-list', kwargs={'pk': self.object.chatbot.pk})

    success_message = "Action was deleted successfully."

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, self.success_message)
        return super(ActionsDeleteView, self).delete(request, *args, **kwargs)

    def test_func(self):
        action = self.get_object()
        if self.request.user == action.chatbot.user:
            return True
        return False

    def get_context_data(self, **kwargs):
        context = super(ActionsDeleteView, self).get_context_data(**kwargs)
        action = get_object_or_404(Action, pk=self.kwargs['pk'])
        chatbot = get_object_or_404(Chatbot, pk=action.chatbot.pk)
        context['prim_key'] = chatbot.pk
        return context


class ActionsUpdateView(LoginRequiredMixin, ModelFormSetView):
    model = Action
    template_name = 'creator/action_update.html'
    fields = ['name', 'run_contents', 'chatbot']

    def get_queryset(self):
        action = Action.objects.filter(chatbot_id=self.kwargs['pk'])
        return action

    def get_context_data(self, **kwargs):
        context = super(ActionsUpdateView, self).get_context_data(**kwargs)
        context['prim_key'] = self.kwargs['pk']
        return context


class SlotsListView(LoginRequiredMixin, ListView):
    model = Slot

    def get_queryset(self):
        return Slot.objects.filter(chatbot_id=self.kwargs['pk'])

    def get_context_data(self, **kwargs):
        context = super(SlotsListView, self).get_context_data(**kwargs)
        context['prim_key'] = self.kwargs['pk']
        return context


class SlotCreateView(LoginRequiredMixin, CreateView):
    model = Slot
    fields = ['name', 'type', 'influence_conversation', 'value', 'form', 'chatbot']

    def form_valid(self, form):
        messages.success(self.request, "Slot was created successfully.")
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('slots-list', kwargs={'pk': self.object.chatbot.pk})

    def get_context_data(self, **kwargs):
        context = super(SlotCreateView, self).get_context_data(**kwargs)
        context['prim_key'] = self.kwargs['pk']
        return context


class SlotsDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Slot

    def get_success_url(self):
        return reverse('slots-list', kwargs={'pk': self.object.chatbot.pk})

    success_message = "Slot was deleted successfully."

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, self.success_message)
        return super(SlotsDeleteView, self).delete(request, *args, **kwargs)

    def test_func(self):
        slot = self.get_object()
        if self.request.user == slot.chatbot.user:
            return True
        return False

    def get_context_data(self, **kwargs):
        context = super(SlotsDeleteView, self).get_context_data(**kwargs)
        slot = get_object_or_404(Slot, pk=self.kwargs['pk'])
        chatbot = get_object_or_404(Chatbot, pk=slot.chatbot.pk)
        context['prim_key'] = chatbot.pk
        return context


class SlotsUpdateView(LoginRequiredMixin, ModelFormSetView):
    model = Slot
    template_name = 'creator/slot_update.html'
    fields = ['name', 'type', 'influence_conversation', 'value', 'form', 'chatbot']

    def get_queryset(self):
        slot = Slot.objects.filter(chatbot_id=self.kwargs['pk'])
        return slot

    def get_context_data(self, **kwargs):
        context = super(SlotsUpdateView, self).get_context_data(**kwargs)
        context['prim_key'] = self.kwargs['pk']
        return context


class FormsListView(LoginRequiredMixin, ListView):
    model = Form

    def get_queryset(self):
        return Form.objects.filter(chatbot_id=self.kwargs['pk'])

    def get_context_data(self, **kwargs):
        context = super(FormsListView, self).get_context_data(**kwargs)
        context['prim_key'] = self.kwargs['pk']
        return context


class FormCreateView(LoginRequiredMixin, CreateView):
    model = Form
    fields = ['name', 'intent', 'chatbot']

    def form_valid(self, form):
        messages.success(self.request, "Form was created successfully.")
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('forms-list', kwargs={'pk': self.object.chatbot.pk})

    def get_context_data(self, **kwargs):
        context = super(FormCreateView, self).get_context_data(**kwargs)
        context['prim_key'] = self.kwargs['pk']
        return context


class FormsDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Form

    def get_success_url(self):
        return reverse('forms-list', kwargs={'pk': self.object.chatbot.pk})

    success_message = "Form was deleted successfully."

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, self.success_message)
        return super(FormsDeleteView, self).delete(request, *args, **kwargs)

    def test_func(self):
        form = self.get_object()
        if self.request.user == form.chatbot.user:
            return True
        return False

    def get_context_data(self, **kwargs):
        context = super(FormsDeleteView, self).get_context_data(**kwargs)
        form = get_object_or_404(Slot, pk=self.kwargs['pk'])
        chatbot = get_object_or_404(Chatbot, pk=form.chatbot.pk)
        context['prim_key'] = chatbot.pk
        return context


class FormsUpdateView(LoginRequiredMixin, ModelFormSetView):
    model = Form
    template_name = 'creator/form_update.html'
    fields = ['name', 'intent', 'chatbot']

    def get_queryset(self):
        form = Form.objects.filter(chatbot_id=self.kwargs['pk'])
        return form

    def get_context_data(self, **kwargs):
        context = super(FormsUpdateView, self).get_context_data(**kwargs)
        context['prim_key'] = self.kwargs['pk']
        return context


def training(request, pk):
    chatbot = get_object_or_404(Chatbot, pk=pk)
    intents = Intent.objects.filter(chatbot=pk).values_list('id', 'name')
    examples = Examples.objects.filter(intent__chatbot=pk).values_list('intent', 'example')
    responses = Responses.objects.filter(chatbot=pk).values_list('id', 'name')
    utterances = Utterances.objects.filter(response__chatbot=pk).values_list('response', 'text', 'image')
    stories = Story.objects.filter(chatbot=pk).values_list('id', 'name')
    steps = Steps.objects.filter(story__chatbot=pk).values_list('intent__name', 'response__name', 'action__name', 'form__name','order', 'story').order_by('order')
    rules = Rule.objects.filter(chatbot=pk).values_list('name', 'intent__name', 'action__name')
    actions = Action.objects.filter(chatbot=pk).values_list('name', 'run_contents', 'chatbot')
    forms = Form.objects.filter(chatbot=pk).values_list('id', 'name', 'intent__name')
    slots = Slot.objects.filter(form__chatbot=pk).values_list('name', 'type', 'influence_conversation', 'value', 'form')

    chatbot_train(chatbot, intents, examples, responses, utterances, stories, steps, rules, actions, forms, slots)
    messages.success(request, 'Your chatbot is being trained, please wait some minutes to let it finish')
    return redirect(chatbot)


def testing(request, pk):
    chatbot = get_object_or_404(Chatbot, pk=pk)
    actions = Action.objects.filter(chatbot=pk).values_list('name', 'run_contents', 'chatbot')
    chatbot_start(chatbot, actions)
    context = {'chatbot': chatbot}
    return render(request, 'chatbot-widget/index.html', context)


def downloading(request, pk):
    chatbot = get_object_or_404(Chatbot, pk=pk)
    shutil.make_archive("chatbots/"+chatbot.name, 'zip', "chatbots/"+chatbot.name)

    path = "chatbots/" + chatbot.name + ".zip"

    zipfile = open(path, 'rb')
    response = FileResponse(zipfile)

    os.remove(path)
    return response

