# Generated by Django 4.1.7 on 2023-03-21 19:13

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ponto', '0007_alter_customuser_data_admissao_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customuser',
            name='username',
        ),
        migrations.AlterField(
            model_name='customuser',
            name='data_admissao',
            field=models.DateField(default=datetime.date(2023, 3, 21), verbose_name='Data de admissão'),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='data_senha',
            field=models.DateField(default=datetime.date(2023, 3, 21), verbose_name='Data da ultima troca de senha'),
        ),
    ]
