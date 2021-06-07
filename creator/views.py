from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.http import HttpResponse
from .models import Chatbot, Intent, Story
from .utils import chatbot_create, chatbot_delete, chatbot_train
from django.contrib import messages


def home(request):
    context = {
        'chatbots': Chatbot.objects.all()
    }
    return render(request, 'creator/home.html', context)


def about(request):
    return render(request, 'creator/about.html')


class ChatbotListView(ListView):
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


class ChatbotCreateView(LoginRequiredMixin, CreateView):
    model = Chatbot
    fields = ['name', 'description']

    def form_valid(self, form):
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


class IntentUpdateView(LoginRequiredMixin, UserPassesTestMixin, SuccessMessageMixin, UpdateView):
    model = Intent
    fields = ['yaml']
    success_message = 'Intents successfully saved!!'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def test_func(self):
        intent = self.get_object()
        if self.request.user == intent.chatbot.user:
            return True
        return False


class StoryUpdateView(LoginRequiredMixin, UserPassesTestMixin, SuccessMessageMixin, UpdateView):
    model = Story
    fields = ['yaml']
    success_message = 'Stories successfully saved!!'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def test_func(self):
        story = self.get_object()
        if self.request.user == story.chatbot.user:
            return True
        return False


def training(request, pk):
    chatbot = get_object_or_404(Chatbot, pk=pk)
    chatbot_train(chatbot)
    messages.success(request, 'Your chatbot is being trained, please wait some minutes to let it finish')
    return redirect(chatbot)


