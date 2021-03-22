import random
from datetime import datetime
from django.conf import settings

import pytz
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver
from django_otp.oath import TOTP
from sendsms import api

@receiver(post_save, sender=get_user_model())
def send_otp(sender, instance, created, **kwargs):
    '''
    Send OTP to user for verification
    '''


    # create otp device
    totp = TOTP(key=bytes(settings.SECRET_KEY, encoding='utf-8'), digits=5, step=300)
    # t0 = (int(datetime.now(tz=pytz.UTC).timestamp()) - random.randint(10000, 100000)),

    totp.time = datetime.now().second
    # totp.t()

    # generate and send token via sms
    token = totp.token()
    if created:
        api.send_sms(
            body=f'\nPlease active your account with this OTP: {token}\n',
            from_phone=settings.CALLER_ID,
            to=[instance.phone_number]
        )

    if not created:
        print(f'\nUpdate User: SENT OTP {token} --- RECIEVED OTP {instance.otp}\n')

    # print(f'\nNEW USER: {instance}\n')
    
    # if not created:
    #     print(f'\nUSER UPDATE: {instance}\n')

    # # verify user's token from request
    # sms_otp = int(validated_data.get('verify_otp', 0))

    # # if otp valid, activate user's account
    # if totp.verify(sms_otp):
    #     instance.is_active = True
    #     instance.save()
    


    # # if created:
    # #     token = instance.handle_otp().token()
    # #     print(f'sending otp {token} to {instance}')

    # #     instance.generated_otp = token
    # #     instance.save()
    # api.send_sms(
    #     body='test sms',
    #     from_phone='123',
    #     to=['456']
    # )

    # print(f'\nDEBUG USER SIGNAL: {instance}\n')
    # pass
    

# pre_save.connect(validate_phone_number, sen)
