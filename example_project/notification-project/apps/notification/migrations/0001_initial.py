# Generated by Django 4.1.6 on 2023-02-10 17:29

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="NotificationTemplate",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("title", models.CharField(max_length=255, verbose_name="Title")),
                ("sub_title", models.TextField(verbose_name="Subtitle")),
                ("img_url", models.URLField(blank=True, null=True)),
                ("link", models.URLField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name="NotificationSchedule",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "auditory_type",
                    models.CharField(
                        choices=[("all_users", "All users"), ("one_user", "One user")],
                        max_length=255,
                        verbose_name="Type",
                    ),
                ),
                (
                    "notification",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="notification.notificationtemplate",
                    ),
                ),
                (
                    "users",
                    models.ManyToManyField(blank=True, to=settings.AUTH_USER_MODEL),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Notification",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("title", models.CharField(max_length=255, verbose_name="Title")),
                ("sub_title", models.TextField(verbose_name="Subtitle")),
                ("img_url", models.URLField(blank=True, null=True)),
                ("link", models.URLField(blank=True, null=True)),
                (
                    "auditory_type",
                    models.CharField(
                        choices=[("all_users", "All users"), ("one_user", "One user")],
                        max_length=255,
                        verbose_name="Type",
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                (
                    "user",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
    ]
