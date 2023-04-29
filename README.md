# OneSignal orqali Notification jo'natish
## Kirish
Birinchi o'rinda bizga OneSingaldan **APP_ID** va avtorizatsiya uchun **AUTH TOKEN** kerak bo'ladi. Buni bizga mobile team berishadi. Keyin esa **requests** module kerak bo'ladi

    pip install requests

Push notification jo'natish uchun biz kerakli ma'lumotlarni to'ldirib, Onesignalga request jo'natamiz, keyin onesignal mobilega websocket orqali biz jo'natgan notificationni yuboradi
![enter image description here](https://telegra.ph/file/7010751cbb7c7bcec06dd.jpg)
## Notification jo'natish
Umumiy qilib olganda, notificationni quyidagi funksiya orqali jo'natamiz:

    def send_push_notification(large_icon=None, big_picture=None, url=None,  
                               title_en="None", title_uz="None", title_ru="None",  
                               content_en="None", content_uz="None", content_ru="None",  
                               object_id=None, user_id=None):  
        
        header = {"Content-Type": "application/json; charset=utf-8",  
                 "Authorization": f"Basic {settings.ONE_SIGNAL_AUTH_API_KEY}"}  
      
	    if not user_id:
	        payload = {  
	             "app_id": settings.ONE_SIGNAL_APP_ID,  
                 "included_segments": ["Subscribed Users"],  
                 "contents": {"en": content_en, "uz": content_uz, "ru": content_ru},  
                 "headings": {"en": title_en, "uz": title_uz, "ru": title_ru},  
                 "data": {"id": object_id}, # additional data  
                 "large_icon": large_icon,  
                 "big_picture": big_picture,  
                 "url": url  
	        }
	    
	    else:
		    device_ids = list(  
                      UserDeviceId.objects.filter(user_id=user_id, is_active=True)
                          .values_list('device_id', flat=True))  
	        payload = {  
	              "app_id": settings.ONE_SIGNAL_APP_ID,  
                  "include_player_ids": device_ids,  
                  "channel_for_external_user_ids": "push",  
                  "contents": {"en": content_en, "uz": content_uz, "ru": content_ru},  
                  "headings": {"en": title_en, "uz": title_uz, "ru": title_ru},  
                  "data": {"user_id": user_id, "id": object_id}, # additional data    
                  "large_icon": large_icon,
                  "big_picture": big_picture,  
                  "url": url  
	        }  
        
        req = requests.post("https://onesignal.com/api/v1/notifications", headers=header, 
					        data=json.dumps(payload))  
        if req.status_code == 200:  
            print("Success")  
        else:  
            print("Error")  
          
        return req

Bu yerda notification jo'natish 2 xil usulda bo'ladi: hamma userlarga va faqat maxsus userlarga (ya'ni hammaga emas)
**1: Barchaga notification jo'natish**
Bir vaqtni o'zida hammaga jo'natish uchun **payload** da "**included_segments**" joyida "**[Subscrided Users]**" bo'lishi kerak

        payload = {  
             ...
             "included_segments": ["Subscribed Users"],
             ... }

**2: Faqatgina maxsus userlarni o'ziga jo'natish**
Bu holatda biz device idlarni bir model ochib, shu yerda userga bo'g'lab saqlab ketishimiz kerak:

    class UserDeviceId(models.Model):  
        user = models.ForeignKey(User, verbose_name="User", on_delete=models.CASCADE)  
        device_id = models.CharField(verbose_name="Device id", max_length=255)  
        status = models.BooleanField(verbose_name="Status", default=False)
Bizga device_idlarni mobilechilar berishadi, va bizning api orqali shu modelimizga ma'lumot qo'shib borishadi.
Faqatgina maxsus devicega jo'natish uchun **payload**da "**include_player_ids**" va "**channel_for_external_user_ids**"ga kerakli qiymatlar berib ketishimiz kerak.
		  

     device_ids = list(  
                    UserDeviceId.objects.filter(user_id=user_id, is_active=True)
                    .values_list('device_id', flat=True)
                         )  
     payload = {  
	     ... 
	     "include_player_ids": device_ids,  
	     "channel_for_external_user_ids": "push",
	     ...
	  } 
device_ids - jo'natilishi kerak bo'lgan device idlar ro'yhati (mobilechilardan olinadi)

Umuman olganda biz **payload** da quyidagi narsalarni OneSignalga jo'natamiz:

    ...
    "contents": {"en": content_en, "uz": content_uz, "ru": content_ru},  
    "headings": {"en": title_en, "uz": title_uz, "ru": title_ru},  
    "data": {"user_id": user_id, "id": object_id}, # additional data  
    "large_icon": "https://www.7pace.com/wp-content/uploads/2020/08/bugs.png",
    "big_picture": "https://www.7pace.com/wp-content/uploads/2020/08/bugs.png"  
    "url": url
    ...
en, uz, ru - tillar.
data - qo'shimcha data berib yuborishimiz mumkin bu yerda (optional)
url - ustiga bosganda qayerga o'tish kerakligi (optional)
large_icon va big_picture ga rasm url beriladi.
![enter image description here](https://i.ibb.co/NFGGTCj/image-1.png)![enter image description here](https://i.ibb.co/mH32ydq/image-3.png)

To'liq dokumentatsiya:
https://documentation.onesignal.com/reference/push-channel-properties
