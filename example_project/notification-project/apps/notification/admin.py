from django.contrib import admin

from apps.notification.models import Notification, NotificationSchedule, NotificationTemplate

admin.site.register(Notification)

admin.site.register(NotificationTemplate)

admin.site.register(NotificationSchedule)