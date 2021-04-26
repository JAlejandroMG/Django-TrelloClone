# Generated by Django 2.2.19 on 2021-04-25 23:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('boards', '0001_initial'),
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='board',
            name='members',
            field=models.ManyToManyField(blank=True, related_name='members_board', to='users.User'),
        ),
        migrations.AddField(
            model_name='board',
            name='owner',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='creator_board', to='users.User'),
        ),
    ]
