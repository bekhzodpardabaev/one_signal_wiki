import json

import requests
from django.conf import settings

from apps.common.models import UserDeviceId


def send_push_notification(large_icon=None, big_picture=None, url=None,
                           title_en="None", title_uz="None", title_ru="None",
                           content_en="None", content_uz="None", content_ru="None",
                           user_id=None, object_id=None):
    header = {"Content-Type": "application/json; charset=utf-8",
              "Authorization": f"Basic {settings.ONE_SIGNAL_AUTH_API_KEY}"}

    if user_id is None:
        payload = {
            "app_id": settings.ONE_SIGNAL_APP_ID,
            "included_segments": ["Subscribed Users"],
            "contents": {"en": content_en, "uz": content_uz, "ru": content_ru},
            "headings": {"en": title_en, "uz": title_uz, "ru": title_ru},
            "data": {"id": object_id},  # additional data
            "large_icon": large_icon,
            "big_picture": big_picture,
            "url": url
        }
    else:
        device_ids = list(
            UserDeviceId.objects.filter(user_id=user_id, is_active=True).values_list('device_id', flat=True))

        payload = {
            "app_id": settings.ONE_SIGNAL_APP_ID,
            "include_player_ids": device_ids,
            "channel_for_external_user_ids": "push",
            "contents": {"en": content_en, "uz": content_uz, "ru": content_ru},
            "headings": {"en": title_en, "uz": title_uz, "ru": title_ru},
            "data": {"user_id": user_id, "id": object_id},  # additional data
            "large_icon": large_icon,
            "url": url
        }
    print('paylod: ', payload)
    req = requests.post("https://onesignal.com/api/v1/notifications", headers=header, data=json.dumps(payload))
    print('req text ', req.json())
    if req.status_code == 200:
        print("Success")
    else:
        print("Error")

    return req
