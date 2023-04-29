from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

from apps.notification.utils import send_push_notification


class NotificationTypeChoices(models.TextChoices):
    all_users = 'all_users', 'All users'
    one_user = 'one_user', 'One user'


class Notification(models.Model):
    title = models.CharField(verbose_name="Title", max_length=255)
    sub_title = models.TextField(verbose_name="Subtitle")
    img_url = models.URLField(null=True, blank=True)
    link = models.URLField(null=True, blank=True)
    auditory_type = models.CharField(verbose_name="Type", max_length=255, choices=NotificationTypeChoices.choices)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class NotificationTemplate(models.Model):
    title = models.CharField(verbose_name="Title", max_length=255)
    sub_title = models.TextField(verbose_name="Subtitle")
    img_url = models.URLField(null=True, blank=True)
    link = models.URLField(null=True, blank=True)

    def __str__(self):
        return self.title


class NotificationSchedule(models.Model):
    notification = models.ForeignKey(NotificationTemplate, on_delete=models.CASCADE)
    auditory_type = models.CharField(verbose_name="Type", max_length=255, choices=NotificationTypeChoices.choices)
    users = models.ManyToManyField(User, blank=True)

    def __str__(self):
        return self.notification.title


@receiver([post_save], sender=NotificationSchedule)
def send_notification(sender, instance, created, **kwargs):
    if created:
        notification_template = instance.notification
        if instance.auditory_type == NotificationTypeChoices.all_users:
            response = send_push_notification(large_icon=notification_template.img_url,
                                              big_picture=notification_template.img_url,
                                              title_uz=notification_template.title,
                                              title_en=notification_template.title,
                                              title_ru=notification_template.title,
                                              content_uz=notification_template.sub_title,
                                              content_en=notification_template.sub_title,
                                              content_ru=notification_template.sub_title,
                                              url=notification_template.link,
                                              user_id=None)
            if response.status_code == 200:
                Notification.objects.create(title=notification_template.title,
                                            sub_title=notification_template.sub_title,
                                            img_url=notification_template.img_url, link=notification_template.link,
                                            auditory_type=instance.auditory_type)
            else:
                print('Error')
                # error case logic here

        elif instance.auditory_type == NotificationTypeChoices.one_user:
            users = instance.users.all()

            for user in users:
                response = send_push_notification(large_icon=notification_template.img_url,
                                                  big_picture=notification_template.img_url,
                                                  title_uz=notification_template.title,
                                                  title_en=notification_template.title,
                                                  title_ru=notification_template.title,
                                                  content_uz=notification_template.sub_title,
                                                  content_en=notification_template.sub_title,
                                                  content_ru=notification_template.sub_title,
                                                  url=notification_template.link,
                                                  user_id=user.id)
                if response.status_code == 200:
                    Notification.objects.create(title=notification_template.title,
                                                sub_title=notification_template.sub_title,
                                                img_url=notification_template.img_url, link=notification_template.link,
                                                auditory_type=instance.auditory_type, user_id=user.id)
                else:
                    print('Error')
                    # error case logic here
