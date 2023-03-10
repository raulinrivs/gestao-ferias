from django.forms import ValidationError
from django import forms
from django.core.mail import send_mail
from config import settings
from datetime import datetime, timedelta, date, time

class RegisterForm(forms.Form):
    matricula = forms.CharField(
        label= 'Matricula',
        widget=forms.TextInput(attrs={
            'placeholder': 'Matricula'
    }))
    email = forms.EmailField(
        label= 'E-mail',
        widget=forms.TextInput(attrs={
            'placeholder': 'E-mail'
    }))

    def send_email(self):
        subject = 'Senha Ponto'
        message = f'Senha: 12345678'
        email_from = settings.EMAIL_HOST_USER
        recipient_list = ['pipecy@getnada.com',]
        send_mail(subject, message, email_from, recipient_list)
        

class LoginForm(forms.Form):
    login = forms.CharField(label='Usuário')
    senha = forms.CharField(widget=forms.PasswordInput)
    
    
class SolicitacaoForm(forms.Form):
    TIPO_FERIAS = [
                ('INT', 'Integral'), 
                ('VEN', 'Venda'), 
                ('PAR', 'Parcial'),
        ]
    tipo_ferias = forms.ChoiceField(choices=TIPO_FERIAS)
    data_inicial_1 = forms.DateField(label='Data inicial 1', widget=forms.TextInput(attrs={
            'type': 'date'
    }))
    data_final_1 = forms.DateField(label='Data final 1', widget=forms.TextInput(attrs={
            'type': 'date'
    }))
    data_inicial_2 = forms.DateField(required=False, label='Data inicial 2', widget=forms.TextInput(attrs={
            'type': 'date'
    }))
    data_final_2 = forms.DateField(required=False, label='Data final 2', widget=forms.TextInput(attrs={
            'type': 'date'
    }))
    data_inicial_3 = forms.DateField(required=False, label='Data inicial 3', widget=forms.TextInput(attrs={
            'type': 'date'
    }))
    data_final_3 = forms.DateField(required=False, label='Data final 3', widget=forms.TextInput(attrs={
            'type': 'date'
    }))
    data_inicial_venda = forms.DateField(required=False, label='Data inicial venda', widget=forms.TextInput(attrs={
            'type': 'date'
    }))
    data_final_venda = forms.DateField(required=False, label='Data final venda', widget=forms.TextInput(attrs={
            'type': 'date'
    }))
    
    
    def clean(self):
        cleaned_data = super().clean()
        data_hoje = datetime.combine(date.today(), time(0,0))
        data_inicial = datetime.combine(cleaned_data.get('data_inicial_1'), time(0,0))
        data_final = datetime.combine(cleaned_data.get('data_final_1'), time(0,0))
        # Critérios gerais
        # Solicitação com no mínimo 30 dias de prazo (forms.py)
        if data_inicial - data_hoje < timedelta(days=30):
            raise ValidationError('Só é possivel solicitar férias com data inicial daqui 30 dias')
        print(f'Data inicial: {data_inicial}\nData final: {data_final}\nData Hoje: {data_hoje}')
        