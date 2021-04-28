# Generated by Django 2.2.19 on 2021-04-25 23:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
        ('lists', '0001_initial'),
        ('cards', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='card',
            name='list_id',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='Card', to='lists.List'),
        ),
        migrations.AddField(
            model_name='card',
            name='members',
            field=models.ManyToManyField(blank=True, related_name='Cards', to='users.User'),
        ),
        migrations.AddField(
            model_name='card',
            name='owner',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='Card', to='users.User'),
        ),
    ]