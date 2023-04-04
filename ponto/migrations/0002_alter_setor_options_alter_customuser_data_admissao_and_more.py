# Generated by Django 4.1.7 on 2023-03-29 16:03

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ponto', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='setor',
            options={'verbose_name_plural': 'Setores'},
        ),
        migrations.AlterField(
            model_name='customuser',
            name='data_admissao',
            field=models.DateField(default=datetime.datetime(2023, 3, 29, 16, 3, 51, 772465, tzinfo=datetime.timezone.utc), verbose_name='Data de admissão'),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='data_senha',
            field=models.DateField(default=datetime.datetime(2023, 3, 29, 16, 3, 51, 772465, tzinfo=datetime.timezone.utc), verbose_name='Data da ultima troca de senha'),
        ),
        migrations.AlterField(
            model_name='setor',
            name='contingente',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='solicitacao',
            name='data_criacao',
            field=models.DateField(default=datetime.datetime(2023, 3, 29, 16, 3, 51, 772465, tzinfo=datetime.timezone.utc), verbose_name='Data de criação'),
        ),
    ]
