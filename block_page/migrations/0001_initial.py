# Generated by Django 3.2.4 on 2021-11-23 05:27

import ckeditor_uploader.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        ('catalogue', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='SlidesFlatShow',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('slides_show_name', models.CharField(max_length=33, verbose_name='slides show name')),
                ('published', models.BooleanField(default=True, verbose_name='published')),
            ],
            options={
                'ordering': ('-published',),
            },
        ),
        migrations.CreateModel(
            name='SlidesFlatPage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30, verbose_name='name')),
                ('specific_explanation', models.CharField(max_length=200, verbose_name='specific explanation')),
                ('slide_photo', models.FileField(blank=True, null=True, upload_to='publisher_photo/', verbose_name='slide photo')),
                ('publications_slide', models.BooleanField(blank=True, default=False, null=True, verbose_name='publish slide photo')),
                ('paragraph', ckeditor_uploader.fields.RichTextUploadingField(verbose_name='paragraph')),
                ('object_id', models.PositiveIntegerField()),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Date of creation')),
                ('modified_at', models.DateTimeField(auto_now=True, verbose_name='Date of change')),
                ('to_publish', models.BooleanField(default=False, verbose_name='to publish slideshows')),
                ('content_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='contenttypes.contenttype')),
                ('product_link', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='catalogue.product')),
            ],
            options={
                'ordering': ('-modified_at',),
            },
        ),
    ]