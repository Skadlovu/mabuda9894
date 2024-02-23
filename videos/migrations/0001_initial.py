# Generated by Django 5.0 on 2024-02-22 21:01

import django.db.models.deletion
import taggit.managers
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('taggit', '0006_rename_taggeditem_content_type_object_id_taggit_tagg_content_8fc721_idx'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField(default='videos', max_length=100)),
                ('slug', models.SlugField(default='', max_length=100)),
                ('number_of_videos', models.IntegerField(blank=True, default=0)),
                ('status', models.BooleanField(default=False, help_text='0=default, 1=hidden')),
            ],
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField(blank=True, max_length=250, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='VidStream',
            fields=[
                ('title', models.CharField(max_length=300)),
                ('description', models.TextField(max_length=600)),
                ('upload_date', models.DateTimeField(auto_now_add=True)),
                ('video', models.FileField(upload_to='videos', verbose_name='Video')),
                ('thumb', models.ImageField(blank=True, default='', upload_to='thumbs')),
                ('views', models.PositiveBigIntegerField(blank=True, default=0)),
                ('slug', models.SlugField(default='', max_length=100)),
                ('status', models.BooleanField(default=False, help_text='0=default, 1=hidden')),
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('duration', models.CharField(blank=True, default='', max_length=20, null=True)),
                ('size', models.CharField(default=0, max_length=20)),
                ('preview', models.FileField(blank=True, default='', null=True, upload_to='preview')),
                ('timestamp', models.DateTimeField(auto_now_add=True, null=True)),
                ('last_viewed', models.DateTimeField(auto_now=True)),
                ('category', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='videos.category', verbose_name='Category')),
                ('comments', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='event_comments', to='videos.comment')),
                ('likes', models.ManyToManyField(blank=True, related_name='video_likes', to=settings.AUTH_USER_MODEL)),
                ('tags', taggit.managers.TaggableManager(help_text='A comma-separated list of tags.', through='taggit.TaggedItem', to='taggit.Tag', verbose_name='Tags')),
                ('uploader', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='User')),
            ],
            options={
                'ordering': ['-upload_date'],
            },
        ),
        migrations.AddField(
            model_name='comment',
            name='video',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='videos.vidstream'),
        ),
    ]
