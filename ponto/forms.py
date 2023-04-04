# from django.forms import ValidationError
# from django import forms
# from django.core.mail import send_mail
# from config import settings
# from datetime import datetime, timedelta, date, time
# from .models import CustomUser

# class RegisterForm(forms.Form):
#     matricula = forms.CharField(
#         label= 'Matricula',
#         widget=forms.TextInput(attrs={
#             'placeholder': 'Matricula'
#     }))
#     email = forms.EmailField(
#         label= 'E-mail',
#         widget=forms.TextInput(attrs={
#             'placeholder': 'E-mail'
#     }))

#     def send_email(self, senha):
#         subject = 'Senha Ponto'
#         message = f'Senha: {senha}'
#         email_from = settings.EMAIL_HOST_USER
#         recipient_list = [self.cleaned_data['email']]
#         send_mail(subject, message, email_from, recipient_list)
        

# class LoginForm(forms.Form):
#     login = forms.CharField(label='Usuário')
#     senha = forms.CharField(widget=forms.PasswordInput)
    
    
# class SolicitacaoForm(forms.Form):
#     TIPO_FERIAS = [
#                 ('INT', 'Integral'), 
#                 ('VEN', 'Venda'), 
#                 ('PAR', 'Parcial'),
#         ]
#     tipo_ferias = forms.ChoiceField(choices=TIPO_FERIAS)
#     data_inicial_1 = forms.DateField(label='Data inicial 1', widget=forms.TextInput(attrs={
#             'type': 'date'
#     }))
#     data_final_1 = forms.DateField(label='Data final 1', widget=forms.TextInput(attrs={
#             'type': 'date'
#     }))
#     data_inicial_2 = forms.DateField(required=False, label='Data inicial 2', widget=forms.TextInput(attrs={
#             'type': 'date'
#     }))
#     data_final_2 = forms.DateField(required=False, label='Data final 2', widget=forms.TextInput(attrs={
#             'type': 'date'
#     }))
#     data_inicial_3 = forms.DateField(required=False, label='Data inicial 3', widget=forms.TextInput(attrs={
#             'type': 'date'
#     }))
#     data_final_3 = forms.DateField(required=False, label='Data final 3', widget=forms.TextInput(attrs={
#             'type': 'date'
#     }))
#     data_inicial_venda = forms.DateField(required=False, label='Data inicial venda', widget=forms.TextInput(attrs={
#             'type': 'date'
#     }))
#     data_final_venda = forms.DateField(required=False, label='Data final venda', widget=forms.TextInput(attrs={
#             'type': 'date'
#     }))
    
#     def send_email(self, user):
#         groups = user.groups.all()
#         users = CustomUser.objects.all()
#         recipient_list = [user.email]
#         if user.gestor.all():
#             print('')
#         else:
#             for setor in groups:
#                 gestores = users.filter(gestor=setor) 
#                 for user in gestores:
#                     recipient_list.append(user.email)
#         subject = 'Solicitação de férias criado'
#         message = f''
#         email_from = settings.EMAIL_HOST_USER
#         send_mail(subject, message, email_from, recipient_list)
    
#     def clean(self):
#         cleaned_data = super().clean()
#         data_hoje = datetime.combine(date.today(), time(0,0))
#         data_inicial = datetime.combine(cleaned_data.get('data_inicial_1'), time(0,0))
#         data_final = datetime.combine(cleaned_data.get('data_final_1'), time(0,0))
    
#         if cleaned_data['tipo_ferias'] == 'INT':
#             validador_ferias_integral(data_inicial, data_final, data_hoje)
#         elif cleaned_data['tipo_ferias'] == 'VEN':
#             data_inicial_venda = datetime.combine(cleaned_data.get('data_inicial_venda'), time(0,0))
#             data_final_venda = datetime.combine(cleaned_data.get('data_final_venda'), time(0,0))
#             validador_ferias_venda(data_inicial, data_final, data_inicial_venda, data_final_venda)
#         elif cleaned_data['tipo_ferias'] == 'PAR':
#             data_inicial_2 = datetime.combine(cleaned_data.get('data_inicial_2'), time(0,0))
#             data_final_2 = datetime.combine(cleaned_data.get('data_final_2'), time(0,0))
#             data_inicial_3 = datetime.combine(cleaned_data.get('data_inicial_3'), time(0,0))
#             data_final_3 = datetime.combine(cleaned_data.get('data_final_3'), time(0,0))
#             validador_ferias_parcial(data_inicial, data_final, data_inicial_2, data_final_2, data_inicial_3, data_final_3)


# def validador_ferias_integral(inicial, final, hoje):
#     if final - inicial != timedelta(days=30):
#         raise ValidationError('O intervalo deve possuir 30 dias')
#     if inicial - hoje < timedelta(days=30):
#         raise ValidationError('Só é possivel solicitar férias com data inicial daqui 30 dias')
        

# def validador_ferias_venda(inicial, final, inicial_venda, final_venda):
#     print(final - inicial + final_venda - inicial_venda)
#     if final - inicial + final_venda - inicial_venda != timedelta(days=30):
#         raise ValidationError('O intervalo deve possuir 30 dias')
#     #Ferias -> Venda
#     if inicial_venda > inicial:
#         if inicial < final and inicial < inicial_venda and inicial < final_venda:
#             if final < inicial_venda and final < final_venda:
#                 if inicial_venda < final_venda:
#                     pass
#                 else:
#                     raise ValidationError('Intervalos incorretos')
#             else:
#                 raise ValidationError('Intervalos incorretos')
#         else:
#             raise ValidationError('Intervalos incorretos')
#     #Venda -> Ferias
#     elif inicial > inicial_venda:
#         if inicial_venda < final_venda and inicial_venda < inicial and inicial_venda < final:
#             if final_venda < inicial and final_venda < final:
#                 if inicial < final:
#                     pass
#                 else:
#                     raise ValidationError('Intervalos incorretos')
#             else:
#                 raise ValidationError('Intervalos incorretos')
#         else:
#             raise ValidationError('Intervalos incorretos')


# def validador_ferias_parcial(inicial_1, final_1, inicial_2, final_2, inicial_3, final_3):
#     if final_1 - inicial_1 + final_2 - inicial_2 + final_3 - inicial_3 != timedelta(days=30):
#         raise ValidationError('O intervalo deve possuir 30 dias')
#     if final_1 - inicial_1 >= timedelta(days=5) and \
#         final_2 - inicial_2 >= timedelta(days=5) and \
#         final_3 - inicial_3 >= timedelta(days=5):
#         raise ValidationError('Todos os intervalo devem ter ao menos 5 dias')
#     if final_1 - inicial_1 >= timedelta(days=14) or \
#         final_2 - inicial_2 >= timedelta(days=14) or \
#         final_3 - inicial_3 >= timedelta(days=14):
#         raise ValidationError('Um dos intervalos deve ter ao menos 14 dias')
        