
import secrets

from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DetailView, ListView, View

from users.email_messages import send_welcome_email
from users.forms import UserRegisterForm, CustomLoginForm, UserProfileForm, PasswordResetForm
from users.models import User


class RegisterView(CreateView):
    '''Форма регистрации с отправкой сообщения на почту'''
    model = User
    form_class = UserRegisterForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('users:login')

    def form_valid(self, form):
        user = form.save()
        user.is_active = False
        token = secrets.token_hex(16)
        user.token = token
        user.save()
        host = self.request.get_host()
        url = f'http://{host}/account/email-confirm/{token}'
        send_welcome_email(user, url)
        return super().form_valid(form)



class CustomLoginView(LoginView):
    '''Кастомный логинвью уже со стилями'''
    form_class = CustomLoginForm
    template_name = 'users/login.html'


class ProfileView(LoginRequiredMixin, DetailView):
    '''Контроллер для просмотра профиля'''
    model = User
    template_name = 'users/profile.html'

    def get_object(self, queryset=None):
        return self.request.user


class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    '''Контроллер для обновления профиля'''
    model = User
    form_class = UserProfileForm
    success_url = reverse_lazy('users:profile')

    def get_object(self, queryset=None):
        return self.request.user


class UserListView(LoginRequiredMixin, ListView):
    model = User
    permission_required = 'users.can_change_user_status'

    def get_queryset(self):
        return User.objects.all().order_by('-date_joined')


class UserDetailView(LoginRequiredMixin, DetailView):
    model = User
    context_object_name = 'user'




