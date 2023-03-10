# Generated by Django 4.1.7 on 2023-03-07 23:31

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ponto', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='data_admissao',
            field=models.DateField(default=datetime.date(2023, 3, 7), verbose_name='Data de admissão'),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='matricula',
            field=models.CharField(max_length=15, unique=True, verbose_name='Matricula'),
        ),
        migrations.CreateModel(
            name='Solicitacao',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tipo_ferias', models.CharField(choices=[('INT', 'Integral'), ('VEN', 'Venda'), ('PAR', 'Parcial')], max_length=3)),
                ('intervalos', models.TextField()),
                ('solicitante', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
