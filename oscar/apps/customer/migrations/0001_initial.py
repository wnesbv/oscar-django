# Generated by Django 3.2.4 on 2021-11-28 07:26

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('catalogue', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='ProductAlert',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(blank=True, db_index=True, max_length=254, verbose_name='Email')),
                ('key', models.CharField(blank=True, db_index=True, max_length=128, verbose_name='Key')),
                ('status', models.CharField(choices=[('Unconfirmed', 'Not yet confirmed'), ('Active', 'Active'), ('Cancelled', 'Cancelled'), ('Closed', 'Closed')], default='Active', max_length=20, verbose_name='Status')),
                ('date_created', models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='Date created')),
                ('date_confirmed', models.DateTimeField(blank=True, null=True, verbose_name='Date confirmed')),
                ('date_cancelled', models.DateTimeField(blank=True, null=True, verbose_name='Date cancelled')),
                ('date_closed', models.DateTimeField(blank=True, null=True, verbose_name='Date closed')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='catalogue.product')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='alerts', to=settings.AUTH_USER_MODEL, verbose_name='User')),
            ],
            options={
                'verbose_name': 'Product alert',
                'verbose_name_plural': 'Product alerts',
                'ordering': ['-date_created'],
                'abstract': False,
            },
        ),
    ]
