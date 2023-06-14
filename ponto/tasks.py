from datetime import datetime
import json
from celery import shared_task
from ponto.models import Solicitacao

@shared_task
def solicitacoesDeferidas():
    solicitacoes = Solicitacao.objects.filter(status__in=('DEF', 'USU'))
    for solicitacao in solicitacoes:
        if solicitacao.tipo_ferias == 'INT':
            intervalos = json.loads(solicitacao.intervalos)
            for chave, valor in intervalos.items():
                intervalos[chave] = datetime.strptime(valor, '%d/%m/%Y')
            if solicitacao.status == 'USU' and intervalos.get('data_final_1') <= datetime.today():
                solicitacao.status = 'CON'
                print(f'Solicitação INTEGRAL - {solicitacao.id} de USU para CON') 
            elif solicitacao.status == 'DEF' and intervalos.get('data_inicial_1') <= datetime.today():
                solicitacao.status = 'USU'
                print(f'Solicitação INTEGRAL - {solicitacao.id} de DEF para USU')
            solicitacao.save()
        elif solicitacao.tipo_ferias == 'VEN':
            intervalos = json.loads(solicitacao.intervalos)
            for chave, valor in intervalos.items():
                intervalos[chave] = datetime.strptime(valor, '%d/%m/%Y')
            if solicitacao.status == 'USU' and intervalos.get('data_final_1') <= datetime.today():
                solicitacao.status = 'CON'
                print(f'Solicitação VENDA - {solicitacao.id} de USU para CON')
            elif solicitacao.status == 'DEF' and intervalos.get('data_inicial_1') <= datetime.today():
                solicitacao.status = 'USU'
                print(f'Solicitação VENDA - {solicitacao.id} de DEF para USU')
            solicitacao.save()
        elif solicitacao.tipo_ferias == 'PAR':
            intervalos = json.loads(solicitacao.intervalos)
            for chave, valor in intervalos.items():
                intervalos[chave] = datetime.strptime(valor, '%d/%m/%Y')
            intervalos = intervalos.values()
            data_final = max(intervalos)
            data_inicial = min(intervalos)
            if solicitacao.status == 'USU' and data_final <= datetime.today():
                solicitacao.status = 'CON'
                print(f'Solicitação PARCIAL - {solicitacao.id} de USU para CON')
            elif solicitacao.status == 'DEF' and data_inicial <= datetime.today():
                solicitacao.status = 'USU'
                print(f'Solicitação PARCIAL - {solicitacao.id} de DEF para USU')
            solicitacao.save()
