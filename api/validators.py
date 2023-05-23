from datetime import datetime, timedelta
from django.forms import ValidationError


def validador_ferias_integral(inicial: datetime, final: datetime):
    if final - inicial != timedelta(days=30):
        raise ValidationError('O intervalo deve possuir 30 dias')


def validador_ferias_venda(
    inicial: datetime, final: datetime, inicial_venda: datetime, final_venda: datetime):
    if final - inicial + final_venda - inicial_venda != timedelta(days=30):
        raise ValidationError('O intervalo deve possuir 30 dias')
    #Ferias -> Venda
    if inicial_venda > inicial:
        if not inicial < final and inicial < inicial_venda and inicial < final_venda:
            raise ValidationError('Intervalos incorretos')
        if not final < inicial_venda and final < final_venda:
            raise ValidationError('Intervalos incorretos')
        if not inicial_venda < final_venda:
            raise ValidationError('Intervalos incorretos')
    #Venda -> Ferias
    elif inicial > inicial_venda:
        if inicial_venda < final_venda and inicial_venda < inicial and inicial_venda < final:
            if final_venda < inicial and final_venda < final:
                if inicial < final:
                    pass
                else:
                    raise ValidationError('Intervalos incorretos')
            else:
                raise ValidationError('Intervalos incorretos')
        else:
            raise ValidationError('Intervalos incorretos')


def validador_ferias_parcial(inicial_1: datetime, final_1: datetime, 
    inicial_2: datetime, final_2: datetime, inicial_3: datetime, final_3: datetime):
    if final_1 - inicial_1 + final_2 - inicial_2 + final_3 - inicial_3 != timedelta(days=30):
        raise ValidationError('O intervalo deve possuir 30 dias')
    if not final_1 - inicial_1 >= timedelta(days=5) and \
        final_2 - inicial_2 >= timedelta(days=5) and \
        final_3 - inicial_3 >= timedelta(days=5):
        raise ValidationError('Todos os intervalo devem ter ao menos 5 dias')
    if not final_1 - inicial_1 >= timedelta(days=14) or \
        final_2 - inicial_2 >= timedelta(days=14) or \
        final_3 - inicial_3 >= timedelta(days=14):
        raise ValidationError('Um dos intervalos deve ter ao menos 14 dias')