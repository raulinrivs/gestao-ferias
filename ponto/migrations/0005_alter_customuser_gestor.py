# Generated by Django 4.1.7 on 2023-03-08 17:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        ('ponto', '0004_customuser_gestor_alter_customuser_data_admissao'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='gestor',
            field=models.ManyToManyField(blank=True, to='auth.group'),
        ),
    ]