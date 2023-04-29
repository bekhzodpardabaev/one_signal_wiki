from django.conf import settings
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

from apps.notification.models import Notification
from apps.notification.utils import send_push_notification


class Post(models.Model):
    title = models.CharField(max_length=255)
    body = models.TextField()
    image = models.ImageField(upload_to='post_images', null=True, blank=True)
    notification = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


@receiver([post_save], sender=Post)
def send_notification(sender, instance, created, **kwargs):
    if created and instance.notification:
        response = send_push_notification(
            large_icon=settings.HOST + instance.image.url,
            big_picture=settings.HOST + instance.image.url,
            title_uz=instance.title,
            title_en=instance.title,
            title_ru=instance.title,
            content_uz=instance.body,
            content_en=instance.body,
            content_ru=instance.body,
            url=None,
            user_id=None
        )
        if response.status_code == 200:
            Notification.objects.create(
                title=instance.title, sub_title=instance.body,
                img_url=settings.HOST + instance.image.url,
                auditory_type='all_users'
            )
