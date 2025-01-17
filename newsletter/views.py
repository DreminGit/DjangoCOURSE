from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.urls import reverse_lazy

from django.views.generic import CreateView, ListView, DetailView, UpdateView, DeleteView, TemplateView

from newsletter.forms import NewsletterForm, ClientForm
from newsletter.models import Client, Message, Newsletter


def index_view(request):
    '''Базовый приветственный шаблон сайта'''
    return render(request, 'newsletter/base_welcome.html')


class PersonalAccountOverviewView(TemplateView):
    '''Шаблон персонального аккаунта пользователя'''
    template_name = 'newsletter/personal_account_overview.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['client_list'] = Client.objects.all()  # Список клиентов
        context['newsletter_list'] = Newsletter.objects.all()  # Список рассылок
        context['message_list'] = Message.objects.all()  # Список рассылок
        return context


# CLIENT

class ClientListView(LoginRequiredMixin,ListView):
    '''Контроллер вывода списка клиентов'''
    model = Client

    def get_queryset(self):
        '''Сортирует пользователей по дате добавления в базу'''
        return Client.objects.all().order_by('-created_at')

class ClientDetailView(LoginRequiredMixin, DetailView):
    '''Контроллер просмотра клиента'''
    model = Client

class ClientCreateView(LoginRequiredMixin, CreateView):
    '''Контроллер создания клиента'''
    model = Client
    form_class = ClientForm
    success_url = reverse_lazy('newsletter:client_list')


class ClientUpdateView(LoginRequiredMixin, UpdateView):
    '''Контроллер обновления информации о клиенте'''
    model = Client
    form_class = ClientForm
    success_url = reverse_lazy('newsletter:client_list')


class ClientDeleteView(LoginRequiredMixin, DeleteView):
    '''Контроллер удаления клиента'''
    model = Client
    success_url = reverse_lazy('newsletter:client_list')


# NEWSLETTER


class NewsletterListView(LoginRequiredMixin, ListView):
    '''Контроллер просмотра рассылок'''
    model = Newsletter


class NewsletterCreateView(LoginRequiredMixin, CreateView):
    '''Контроллер создания рассылок'''
    model = Newsletter
    form_class = NewsletterForm
    success_url = reverse_lazy('newsletter:newsletter_list')


class NewsletterUpdateView(LoginRequiredMixin, UpdateView):
    '''Контроллер обновления информации о рассылке'''
    model = Newsletter
    form_class = NewsletterForm
    success_url = reverse_lazy('newsletter:newsletter_list')


class NewsletterDeleteView(LoginRequiredMixin, DeleteView):
    '''Контроллер удаления рассылок'''
    model = Newsletter
    success_url = reverse_lazy('newsletter:newsletter_list')


class NewsletterDetailView(LoginRequiredMixin, DetailView):
    '''Контроллер просмотра информации о рассылке'''
    model = Newsletter


# MESSAGE

class MessageListView(LoginRequiredMixin, ListView):
    '''Контроллер просмотра сообщений'''
    model = Message

class MessageDetailView(LoginRequiredMixin, DetailView):
    '''Контроллер просмотра информации о сообщении'''
    model = Message


class MessageCreateView(LoginRequiredMixin, CreateView):
    '''Контроллер создания сообщения'''
    model = Message
    fields = ('title', 'message')
    success_url = reverse_lazy('newsletter:message_list')


class MessageUpdateView(LoginRequiredMixin, UpdateView):
    '''Контроллер обновления сообщения'''
    model = Message
    fields = ('title', 'message',)
    success_url = reverse_lazy('newsletter:message_list')


class MessageDeleteView(LoginRequiredMixin, DeleteView):
    '''Контроллер удаления сообщения'''
    model = Message
    success_url = reverse_lazy('newsletter:message_list')