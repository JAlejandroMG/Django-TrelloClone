

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('lists', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Card',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('description', models.CharField(max_length=200)),
                ('creation_date', models.DateTimeField(auto_now_add=True)),
                ('expiration_date', models.DateField()),
                ('position', models.IntegerField()),
                ('list_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Card', to='lists.List')),
            ],
        ),
    ]
