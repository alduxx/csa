# Generated by Django 2.1.3 on 2019-04-15 18:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('financeiro', '0004_delete_coagricultor'),
    ]

    operations = [
        migrations.AlterField(
            model_name='registro',
            name='hash',
            field=models.CharField(editable=False, max_length=32),
        ),
    ]