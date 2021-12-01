# Generated by Django 3.2.4 on 2021-11-28 07:26

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('catalogue', '0001_initial'),
        ('basket', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('partner', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='lineattribute',
            name='option',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='catalogue.option', verbose_name='Option'),
        ),
        migrations.AddField(
            model_name='line',
            name='basket',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='lines', to='basket.basket', verbose_name='Basket'),
        ),
        migrations.AddField(
            model_name='line',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='basket_lines', to='catalogue.product', verbose_name='Product'),
        ),
        migrations.AddField(
            model_name='line',
            name='stockrecord',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='basket_lines', to='partner.stockrecord'),
        ),
        migrations.AddField(
            model_name='basket',
            name='owner',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='baskets', to=settings.AUTH_USER_MODEL, verbose_name='Owner'),
        ),
    ]
