# Generated by Django 5.0.4 on 2024-05-10 04:47

import django.contrib.auth.models
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Feature',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='Banner',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.JSONField(default=dict)),
                ('is_active', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('feature', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='banners.feature')),
            ],
        ),
        migrations.CreateModel(
            name='BannerTagFeature',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('banner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='banners.banner')),
                ('feature', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='banners.feature')),
                ('tag', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='banners.tag')),
            ],
        ),
        migrations.AddField(
            model_name='banner',
            name='tags',
            field=models.ManyToManyField(through='banners.BannerTagFeature', to='banners.tag'),
        ),
        migrations.CreateModel(
            name='UserBanner',
            fields=[
                ('user_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('use_last_revision', models.BooleanField(default=False)),
                ('user_tag', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='banners.tag', verbose_name='tag_id')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            bases=('auth.user',),
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.AddConstraint(
            model_name='bannertagfeature',
            constraint=models.UniqueConstraint(fields=('tag', 'banner', 'feature'), name='unique_banner', violation_error_message='A banner must have a unique tag and feature'),
        ),
    ]
