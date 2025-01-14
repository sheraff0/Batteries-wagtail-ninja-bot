# Generated by Django 5.0.2 on 2024-02-20 20:33

import apps.root.models.mixins
import contrib.wagtail.models
import django.db.models.deletion
import modelcluster.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('wagtailcore', '0091_remove_revision_submitted_for_moderation'),
        ('wagtailimages', '0025_alter_image_file_alter_rendition_file'),
    ]

    operations = [
        migrations.CreateModel(
            name='Account',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64, verbose_name='Название')),
            ],
            options={
                'verbose_name': 'Счёт',
                'verbose_name_plural': 'Счета',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Contacts',
            fields=[
                ('page_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='wagtailcore.page')),
                ('name', models.CharField(blank=True, max_length=128, null=True, verbose_name='Наименование')),
                ('avito', models.CharField(blank=True, max_length=128, null=True, verbose_name='Avito')),
                ('whatsapp', models.CharField(blank=True, max_length=128, null=True, verbose_name='WhatsApp')),
                ('telegram', models.CharField(blank=True, max_length=128, null=True, verbose_name='Telegram')),
                ('email', models.CharField(blank=True, max_length=32, null=True, verbose_name='Email')),
                ('phone', models.CharField(blank=True, max_length=32, null=True, verbose_name='Телефон')),
                ('schedule', models.TextField(blank=True, null=True, verbose_name='Часы работы')),
                ('address', models.CharField(blank=True, max_length=64, null=True, verbose_name='Адрес')),
                ('maps_url', models.CharField(blank=True, max_length=64, null=True, verbose_name='Ссылка на карты')),
            ],
            options={
                'abstract': False,
            },
            bases=(apps.root.models.mixins.CommonPagesMixin, contrib.wagtail.models.UnidecodeMixin, 'wagtailcore.page'),
        ),
        migrations.CreateModel(
            name='Country',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64, verbose_name='Название')),
            ],
            options={
                'verbose_name': 'Страна',
                'verbose_name_plural': 'Страны',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Fellow',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64, verbose_name='Имя')),
                ('birth_day', models.DateField(blank=True, null=True, verbose_name='День рождения')),
            ],
            options={
                'verbose_name': 'Сотрудник',
                'verbose_name_plural': 'Сотрудники',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Home',
            fields=[
                ('page_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='wagtailcore.page')),
            ],
            options={
                'abstract': False,
            },
            bases=(apps.root.models.mixins.CommonPagesMixin, apps.root.models.mixins.CatalogSamplesMixin, contrib.wagtail.models.UnidecodeMixin, 'wagtailcore.page'),
        ),
        migrations.CreateModel(
            name='Partner',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64, verbose_name='Название')),
            ],
            options={
                'verbose_name': 'Партнёр',
                'verbose_name_plural': 'Партнёры',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='HomeCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sort_order', models.IntegerField(blank=True, editable=False, null=True)),
                ('catalog_filters', models.CharField(blank=True, max_length=128, null=True, verbose_name='Фильтры каталога')),
                ('title', models.CharField(blank=True, max_length=128, null=True, verbose_name='Заголовок')),
                ('description', models.TextField(blank=True, null=True, verbose_name='Описание')),
                ('image', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='wagtailimages.image', verbose_name='Изображение (PNG!)')),
                ('page', modelcluster.fields.ParentalKey(on_delete=django.db.models.deletion.CASCADE, related_name='categories', to='root.home')),
            ],
            options={
                'verbose_name': 'Категория',
                'verbose_name_plural': 'Категории',
                'ordering': ['sort_order'],
            },
            bases=(apps.root.models.mixins.ImageMixin, models.Model),
        ),
        migrations.CreateModel(
            name='HomeSlide',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sort_order', models.IntegerField(blank=True, editable=False, null=True)),
                ('subtitle', models.CharField(blank=True, max_length=128, null=True, verbose_name='Над заголовком (проблема)')),
                ('title', models.CharField(blank=True, max_length=128, null=True, verbose_name='Заголовок')),
                ('description', models.TextField(blank=True, null=True, verbose_name='Описание')),
                ('details_title', models.CharField(blank=True, max_length=128, null=True, verbose_name='Мотиватор')),
                ('details_subtitle', models.CharField(blank=True, max_length=128, null=True, verbose_name='Мотиватор, дополнение')),
                ('image', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='wagtailimages.image', verbose_name='Изображение (PNG!)')),
                ('page', modelcluster.fields.ParentalKey(on_delete=django.db.models.deletion.CASCADE, related_name='slides', to='root.home')),
            ],
            options={
                'verbose_name': 'Слайд',
                'verbose_name_plural': 'Слайды',
                'ordering': ['sort_order'],
            },
        ),
    ]
