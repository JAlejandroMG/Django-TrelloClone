

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('cards', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('message', models.CharField(max_length=250)),
                ('creation_date', models.DateTimeField(auto_now_add=True)),
                ('card_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='cards.card')),

            ],
        ),
    ]
