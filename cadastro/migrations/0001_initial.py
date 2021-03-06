# Generated by Django 2.1.3 on 2019-04-05 15:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Coagricultor',
            fields=[
                ('identificador', models.IntegerField(primary_key=True, serialize=False)),
                ('nome', models.CharField(max_length=60)),
            ],
        ),
        migrations.CreateModel(
            name='PontoConvivencia',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=28)),
            ],
        ),
        migrations.AddField(
            model_name='coagricultor',
            name='ponto_de_convivencia',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cadastro.PontoConvivencia'),
        ),
    ]
