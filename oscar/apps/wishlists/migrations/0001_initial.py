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
            name='WishList',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='Default', max_length=255, verbose_name='Name')),
                ('key', models.CharField(db_index=True, editable=False, max_length=6, unique=True, verbose_name='Key')),
                ('visibility', models.CharField(choices=[('Private', 'Private - Only the owner can see the wish list'), ('Shared', 'Shared - Only the owner and people with access to the obfuscated link can see the wish list'), ('Public', 'Public - Everybody can see the wish list')], default='Private', max_length=20, verbose_name='Visibility')),
                ('date_created', models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='Date created')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='wishlists', to=settings.AUTH_USER_MODEL, verbose_name='Owner')),
            ],
            options={
                'verbose_name': 'Wish List',
                'ordering': ('owner', 'date_created'),
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Line',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.PositiveIntegerField(default=1, verbose_name='Quantity')),
                ('title', models.CharField(max_length=255, verbose_name='Title')),
                ('product', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='wishlists_lines', to='catalogue.product', verbose_name='Product')),
                ('wishlist', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='lines', to='wishlists.wishlist', verbose_name='Wish List')),
            ],
            options={
                'verbose_name': 'Wish list line',
                'ordering': ['pk'],
                'abstract': False,
                'unique_together': {('wishlist', 'product')},
            },
        ),
    ]
