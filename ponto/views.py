# from base64 import urlsafe_b64encode
# from django.utils.encoding import force_bytes
# from django.shortcuts import redirect, render
# from datetime import datetime, time, timedelta, date
# from config import settings
# from ponto.forms import RegisterForm, LoginForm, SolicitacaoForm
# from django.views.generic.edit import FormView
# from django.views.generic import TemplateView, DetailView
# from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin

# from ponto.models import CustomUser as User, Solicitacao, Group as Setor
# from random import choice
# import string

# class RegisterView(FormView):
#     template_name = 'registration/register.html'
#     form_class = RegisterForm
#     success_url = '/login/'

#     def form_valid(self, form):
#         senha = ''
#         for i in range(8):
#             senha += choice(string.ascii_letters + string.digits)
#         # User.objects.create_user(
#         #     username = form.cleaned_data['matricula'],
#         #     password = senha,
#         #     matricula = form.cleaned_data['matricula'],
#         #     email = form.cleaned_data['email'],
#         # )
#         form.send_email(senha)
#         return super().form_valid(form)

# class DashboardView(LoginRequiredMixin, TemplateView):
#     login_url = '/login/'
#     redirect_field_name = 'redirect_to'
#     template_name = 'dashboard.html'
            
    
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         user = self.request.user
#         #Intervalo desde a ultuma troca de senha
#         if user.is_authenticated:
#             context['intervalo_senha'] = date.today() - user.data_senha
#         context['groups'] = user.groups.all()
#         gestor = user.gestor.all()
        
#         #Solicitações organizadas com prioridade as que foram aprovadas pelo Gestor
#         if user.groups.filter(name='Recursos Humanos').exists():
#             context['rh_dashboard'] = \
#                 Solicitacao.objects.all()
                
#         #Solicitações que são do Setor de responsabilidade do Gestor
#         if gestor:
#             for group in user.groups.all():
#                 solicitacoes = Solicitacao.objects.filter(solicitante__groups=group)
#             context['gestor_dashboard'] = solicitacoes
            
#         #Solicitações que estão no nome do colaborador
#         context['colaborador_dashboard'] = \
#             Solicitacao.objects.filter(solicitante=user)
#         return context
    
# class SolicitacaoView(LoginRequiredMixin, FormView):
#     template_name = 'nova_solicitacao.html'
#     form_class = SolicitacaoForm
#     success_url = '/dashboard'

#     def form_valid(self, form):
#         tempo_servico = datetime.combine(date.today(), time(0,0)) - datetime.combine(self.request.user.data_admissao, time(0,0))
#         print(tempo_servico)
#         # 12 Meses de serviço (Precisa do User -> views.py)
#         if tempo_servico.days < 365:
#             pass
        
#         # Impedir criação se tiver menos de 30 dias para vencimento de ferias(Precisa do User -> views.py)
#         if tempo_servico.days > 700:
#             pass 
            
#         intervalos = {
#             'data_inicial_1': form.cleaned_data['data_inicial_1'].strftime('%d/%m/%Y'),
#             'data_final_1':  form.cleaned_data['data_final_1'].strftime('%d/%m/%Y'),
#         }
#         if form.cleaned_data['data_inicial_2'] and form.cleaned_data['data_final_2']:
#             intervalos['data_inicial_2'] = form.cleaned_data['data_inicial_2'].strftime('%d/%m/%Y')
#             intervalos['data_final_2'] = form.cleaned_data['data_final_2'].strftime('%d/%m/%Y')
#         if form.cleaned_data['data_inicial_3'] and form.cleaned_data['data_final_3']:
#             intervalos['data_inicial_3'] = form.cleaned_data['data_inicial_3'].strftime('%d/%m/%Y')
#             intervalos['data_final_3'] = form.cleaned_data['data_final_3'].strftime('%d/%m/%Y')
#         if form.cleaned_data['data_inicial_venda'] and form.cleaned_data['data_final_venda']:
#             intervalos['data_inicial_venda'] = form.cleaned_data['data_inicial_venda'].strftime('%d/%m/%Y')
#             intervalos['data_final_venda'] = form.cleaned_data['data_final_venda'].strftime('%d/%m/%Y')
#         Solicitacao.objects.create(
#             status='CRI',
#             tipo_ferias=form.cleaned_data['tipo_ferias'],
#             intervalos=intervalos,
#             solicitante=self.request.user,
#         )
#         form.send_email(self.request.user)
#         return super().form_valid(form)
        

# class SolicitacaoDetailView(LoginRequiredMixin, DetailView):
#     model = Solicitacao
#     template_name = 'detalhe_solicitacao.html'
    
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         return context

    