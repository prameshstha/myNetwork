# Generated by Django 2.2.1 on 2019-05-05 02:07

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import homePage.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='UserDetails',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_DOB', models.DateField(null=True)),
                ('user_gender', models.CharField(max_length=1, null=True)),
                ('user_profile_pic', models.ImageField(blank=True, null=True, upload_to=homePage.models.upload_propic_image_path)),
                ('user_cover_pic', models.ImageField(blank=True, null=True, upload_to=homePage.models.upload_coverpic_image_path)),
                ('user_Id', models.OneToOneField(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('post_title', models.CharField(max_length=100)),
                ('post_body', models.CharField(max_length=250)),
                ('post_image', models.ImageField(blank=True, null=True, upload_to='images/')),
                ('post_created_at', models.DateTimeField(auto_now_add=True)),
                ('post_updated_at', models.DateTimeField(auto_now=True)),
                ('post_likes', models.ManyToManyField(blank=True, related_name='post_likes', to=settings.AUTH_USER_MODEL)),
                ('post_user', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='FriendshipRequest',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(default=datetime.datetime(2019, 5, 5, 12, 7, 5, 933183))),
                ('rejected', models.DateTimeField(blank=True, null=True)),
                ('viewed', models.DateTimeField(blank=True, null=True)),
                ('added', models.BooleanField(blank=True, null=True)),
                ('friend_created_at', models.DateTimeField(auto_now_add=True)),
                ('from_user', models.ManyToManyField(blank=True, default=0, related_name='request_sender', to=settings.AUTH_USER_MODEL)),
                ('to_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='requests_receiver', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Friendship Request',
                'verbose_name_plural': 'Friendship Requests',
            },
        ),
        migrations.CreateModel(
            name='Friends',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(default=datetime.datetime(2019, 5, 5, 12, 7, 5, 933183))),
                ('current_user', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='owner', to=settings.AUTH_USER_MODEL)),
                ('friends_friend', models.ManyToManyField(blank=True, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Follower',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(default=datetime.datetime(2019, 5, 5, 12, 7, 5, 933183))),
                ('current_user', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='follower', to=settings.AUTH_USER_MODEL)),
                ('following_user', models.ManyToManyField(blank=True, related_name='followingThem', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Comments',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comment_content', models.TextField(max_length=255)),
                ('comment_created_at', models.DateTimeField(auto_now_add=True)),
                ('comment_updated_at', models.DateTimeField(auto_now=True)),
                ('post_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='homePage.Post')),
                ('user_id', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
