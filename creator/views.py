from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.utils.encoding import smart_str
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.http import HttpResponse, FileResponse
from .models import Chatbot, Intent, Examples, Responses, Story, Steps
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
    fields = ['name', 'response', 'chatbot']

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
    fields = ['name', 'response', 'chatbot']

    def get_queryset(self):
        response = Responses.objects.filter(chatbot_id=self.kwargs['pk'])
        return response

    def get_context_data(self, **kwargs):
        context = super(ResponsesUpdateView, self).get_context_data(**kwargs)
        context['prim_key'] = self.kwargs['pk']
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
    fields = ['intent', 'action', 'order', 'story']

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
    fields = ['intent', 'action', 'order', 'story']

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


def training(request, pk):
    chatbot = get_object_or_404(Chatbot, pk=pk)
    intents = Intent.objects.filter(chatbot=pk).values_list('id', 'name')
    examples = Examples.objects.filter(intent__chatbot=pk).values_list('intent', 'example')
    responses = Responses.objects.filter(chatbot=pk).values_list('name', 'response')
    stories = Story.objects.filter(chatbot=pk).values_list('id', 'name')
    steps = Steps.objects.filter(story__chatbot=pk).values_list('intent__name', 'action__name', 'order', 'story').order_by('order')

    chatbot_train(chatbot, intents, examples, responses, stories, steps)
    messages.success(request, 'Your chatbot is being trained, please wait some minutes to let it finish')
    return redirect(chatbot)


def testing(request, pk):
    chatbot = get_object_or_404(Chatbot, pk=pk)
    chatbot_start(chatbot)
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

