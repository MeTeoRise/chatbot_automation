from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.http import HttpResponse
from .models import Chatbot


def home(request):
    context = {
        'chatbots': Chatbot.objects.all()
    }
    return render(request, 'creator/home.html', context)


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

    def test_func(self):
        chatbot = self.get_object()
        if self.request.user == chatbot.user:
            return True
        return False


def about(request):
    return render(request, 'creator/about.html')


