# Generated by Django 2.2.19 on 2021-05-01 15:34

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Board',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('description', models.CharField(max_length=200)),
                ('date_creation', models.DateTimeField(auto_now_add=True)),
                ('visibility', models.CharField(choices=[('PRIVATE', 'PRIVATE'), ('PUBLIC', 'PUBLIC')], default='PRIVATE', max_length=7)),
            ],
        ),
    ]
