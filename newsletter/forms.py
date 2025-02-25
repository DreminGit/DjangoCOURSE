from django import forms
from .models import Newsletter, Client, Message


class StyleFormMixin:

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'


from django import forms
from .models import Newsletter, Client


class NewsletterForm(forms.ModelForm):
    class Meta:
        model = Newsletter
        fields = ['message', 'scheduled_at', 'periodicity', 'clients','status']
        widgets = {
            'scheduled_at': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'clients': forms.CheckboxSelectMultiple(),  # Используем чекбоксы для клиентов
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)  # Получаем текущего пользователя
        super(NewsletterForm, self).__init__(*args, **kwargs)
        if user is not None:
            # Фильтруем клиентов по текущему пользователю
            self.fields['clients'].queryset = Client.objects.filter(user=user)
            # Фильтруем сообщения по текущему пользователю
            self.fields['message'].queryset = Message.objects.filter(user=user)


class NewsletterManagerForm(forms.ModelForm):
    class Meta:
        model = Newsletter
        fields = ['status']

    def __init__(self, *args, **kwargs):
        super(NewsletterForm, self).__init__(*args, **kwargs)
        # Применяем класс к полям, кроме clients
        for field_name in self.fields:
            if field_name != 'clients':
                self.fields[field_name].widget.attrs.update({'class': 'form-control'})


class ClientForm(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = Client
        fields = ('last_name', 'first_name', 'middle_name', 'email',)