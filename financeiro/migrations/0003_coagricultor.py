# Generated by Django 2.1.3 on 2019-04-02 22:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('financeiro', '0002_registro_hash'),
    ]

    operations = [
        migrations.CreateModel(
            name='Coagricultor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=60)),
                ('identificador', models.CharField(max_length=20)),
            ],
        ),
    ]
