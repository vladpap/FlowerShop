# Generated by Django 4.2.4 on 2023-08-16 19:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('bot', '0003_alter_event_options_catalog'),
    ]

    operations = [
        migrations.CreateModel(
            name='Consultation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='client_consultation_set', to='bot.client', verbose_name='Клиент')),
                ('florist', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='florist_consultation_set', to='bot.client', verbose_name='Флорист')),
            ],
            options={
                'verbose_name': 'Консультация',
                'verbose_name_plural': 'Консультации',
            },
        ),
    ]