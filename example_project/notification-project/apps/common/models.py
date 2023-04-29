from django.contrib.auth.models import User
from django.db import models


class UserDeviceId(models.Model):
    user = models.ForeignKey(User, verbose_name="User", on_delete=models.CASCADE)
    device_id = models.CharField(verbose_name="Device id", max_length=255)
    status = models.BooleanField(verbose_name="Status", default=False)
