# Generated by Django 3.2.4 on 2021-11-28 07:26

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import oscar.models.fields
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Country',
            fields=[
                ('iso_3166_1_a2', models.CharField(max_length=2, primary_key=True, serialize=False, verbose_name='ISO 3166-1 alpha-2')),
                ('iso_3166_1_a3', models.CharField(blank=True, max_length=3, verbose_name='ISO 3166-1 alpha-3')),
                ('iso_3166_1_numeric', models.CharField(blank=True, max_length=3, verbose_name='ISO 3166-1 numeric')),
                ('printable_name', models.CharField(db_index=True, max_length=128, verbose_name='Country name')),
                ('name', models.CharField(max_length=128, verbose_name='Official name')),
                ('display_order', models.PositiveSmallIntegerField(db_index=True, default=0, help_text='Higher the number, higher the country in the list.', verbose_name='Display order')),
                ('is_shipping_country', models.BooleanField(db_index=True, default=False, verbose_name='Is shipping country')),
            ],
            options={
                'verbose_name': 'Country',
                'verbose_name_plural': 'Countries',
                'ordering': ('-display_order', 'printable_name'),
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='UserAddress',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, choices=[('Mr', 'Mr'), ('Miss', 'Miss'), ('Mrs', 'Mrs'), ('Ms', 'Ms'), ('Dr', 'Dr')], max_length=64, verbose_name='Title')),
                ('first_name', models.CharField(blank=True, max_length=255, verbose_name='First name')),
                ('last_name', models.CharField(blank=True, max_length=255, verbose_name='Last name')),
                ('line1', models.CharField(max_length=255, verbose_name='First line of address')),
                ('line2', models.CharField(blank=True, max_length=255, verbose_name='Second line of address')),
                ('line3', models.CharField(blank=True, max_length=255, verbose_name='Third line of address')),
                ('line4', models.CharField(blank=True, max_length=255, verbose_name='City')),
                ('state', models.CharField(blank=True, max_length=255, verbose_name='State/County')),
                ('postcode', oscar.models.fields.UppercaseCharField(blank=True, max_length=64, verbose_name='Post/Zip-code')),
                ('search_text', models.TextField(editable=False, verbose_name='Search text - used only for searching addresses')),
                ('phone_number', phonenumber_field.modelfields.PhoneNumberField(blank=True, help_text='In case we need to call you about your order', max_length=128, region=None, verbose_name='Phone number')),
                ('notes', models.TextField(blank=True, help_text='Tell us anything we should know when delivering your order.', verbose_name='Instructions')),
                ('is_default_for_shipping', models.BooleanField(default=False, verbose_name='Default shipping address?')),
                ('is_default_for_billing', models.BooleanField(default=False, verbose_name='Default billing address?')),
                ('num_orders_as_shipping_address', models.PositiveIntegerField(default=0, verbose_name='Number of Orders as Shipping Address')),
                ('num_orders_as_billing_address', models.PositiveIntegerField(default=0, verbose_name='Number of Orders as Billing Address')),
                ('hash', models.CharField(db_index=True, editable=False, max_length=255, verbose_name='Address Hash')),
                ('date_created', models.DateTimeField(auto_now_add=True, verbose_name='Date Created')),
                ('country', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='address.country', verbose_name='Country')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='addresses', to=settings.AUTH_USER_MODEL, verbose_name='User')),
            ],
            options={
                'verbose_name': 'User address',
                'verbose_name_plural': 'User addresses',
                'ordering': ['-num_orders_as_shipping_address'],
                'abstract': False,
                'unique_together': {('user', 'hash')},
            },
        ),
    ]
