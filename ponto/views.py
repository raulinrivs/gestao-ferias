from django.shortcuts import redirect, render
from django.contrib import messages
from datetime import datetime, time, timedelta, date
from config import settings
from ponto.forms import RegisterForm, LoginForm, SolicitacaoForm
from django.views.generic.edit import FormView
from django.views.generic import TemplateView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from ponto.models import CustomUser, Solicitacao
from django.contrib.auth import authenticate
from django.core.mail import send_mail


class RegisterView(FormView):
    template_name = 'registration/register.html'
    form_class = RegisterForm
    success_url = '/login/'

    def form_valid(self, form):
        print(form.cleaned_data)
        CustomUser.objects.create_user(
            username = form.cleaned_data['matricula'],
            password = '12345678',
            matricula = form.cleaned_data['matricula'],
            email = form.cleaned_data['email'],
        )
        form.send_email()
        return super().form_valid(form)

class DashboardView(LoginRequiredMixin, TemplateView):
    login_url = '/login/'
    redirect_field_name = 'redirect_to'
    template_name = 'dashboard.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        context['groups'] = user.groups.all()
        #Solicitações organizadas com prioridade as que foram aprovadas pelo Gestor
        if user.groups.filter(name='Recursos Humanos').exists():
            context['rh_dashboard'] = \
                Solicitacao.objects.all()
        #Solicitações que são do Setor de responsabilidade do Gestor
        elif user.gestor:
            for group in user.groups.all():
                solicitacoes = Solicitacao.objects.filter(solicitante__groups=group)
            context['gestor_dashboard'] = solicitacoes
        else:
            #Solicitações que estão no nome do colaborador
            context['colaborador_dashboard'] = \
                Solicitacao.objects.filter(solicitante=user)
        return context
    
class SolicitacaoView(LoginRequiredMixin, FormView):
    template_name = 'nova_solicitacao.html'
    form_class = SolicitacaoForm
    success_url = '/dashboard'

    def form_valid(self, form):
        tempo_servico = datetime.combine(date.today(), time(0,0)) - datetime.combine(self.request.user.data_admissao, time(0,0))
        print(tempo_servico)
        # 12 Meses de serviço (Precisa do User -> views.py)
        if tempo_servico.days < 365:
            pass
        # Impedir criação se tiver menos de 30 dias para vencimento de ferias(Precisa do User -> views.py)
        elif tempo_servico.days > 700:
            pass 
        # Contingente (Pensar futuramente)
        # Construção intervalo
        # intervalos = {
        #     'data_inicial_1': form.cleaned_data['data_inicial_1'].strftime('%d/%m/%Y'),
        #     'data_final_1':  form.cleaned_data['data_final_1'].strftime('%d/%m/%Y'),
        #     'data_inicial_2': form.cleaned_data['data_inicial_2'],
        #     'data_final_2': form.cleaned_data['data_final_2'],
        #     'data_inicial_3': form.cleaned_data['data_inicial_3'],
        #     'data_final_3': form.cleaned_data['data_final_3'],
        #     'data_inicial_venda': form.cleaned_data['data_inicial_venda'],
        #     'data_final_venda': form.cleaned_data['data_final_venda'],
        # }
        intervalos = {
            'data_inicial_1': form.cleaned_data['data_inicial_1'].strftime('%d/%m/%Y'),
            'data_final_1':  form.cleaned_data['data_final_1'].strftime('%d/%m/%Y'),
        }
        if form.cleaned_data['data_inicial_2'] and form.cleaned_data['data_final_2']:
            intervalos['data_inicial_2'] = form.cleaned_data['data_inicial_2'].strftime('%d/%m/%Y')
            intervalos['data_final_2'] = form.cleaned_data['data_final_2'].strftime('%d/%m/%Y')
        if form.cleaned_data['data_inicial_3'] and form.cleaned_data['data_final_3']:
            intervalos['data_inicial_3'] = form.cleaned_data['data_inicial_3'].strftime('%d/%m/%Y')
            intervalos['data_final_3'] = form.cleaned_data['data_final_3'].strftime('%d/%m/%Y')
        if form.cleaned_data['data_inicial_venda'] and form.cleaned_data['data_final_venda']:
            intervalos['data_inicial_venda'] = form.cleaned_data['data_inicial_venda'].strftime('%d/%m/%Y')
            intervalos['data_final_venda'] = form.cleaned_data['data_final_venda'].strftime('%d/%m/%Y')
        Solicitacao.objects.create(
            status='CRI',
            tipo_ferias=form.cleaned_data['tipo_ferias'],
            intervalos=intervalos,
            solicitante=self.request.user,
        )
        return super().form_valid(form)
    
    def send_email(self):
        subject = 'Senha Ponto'
        message = f'Senha: 12345678'
        email_from = settings.EMAIL_HOST_USER
        recipient_list = ['pipecy@getnada.com',]
        send_mail(subject, message, email_from, recipient_list)
        

class SolicitacaoDetailView(LoginRequiredMixin, DetailView):
    model = Solicitacao
    template_name = 'detalhe_solicitacao.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    