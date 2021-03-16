from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model

@receiver(post_save, sender=get_user_model())
def send_otp(sender, instance, created, **kwargs):
    '''
    Send OTP to user for verification
    '''
    if created:
        token = instance.handle_otp().token()
        print(f'sending otp {token} to {instance}')

        instance.generated_otp = token
        instance.save()


# pre_save.connect(validate_phone_number, sen)
