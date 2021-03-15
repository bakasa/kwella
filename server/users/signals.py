from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model

@receiver(post_save, sender=get_user_model())
def send_otp(sender, instance, **kwargs):
    '''
    Send OTP to user for verification
    '''

    print(f'sending otp {instance.generate_otp()} to {instance}')
    # pass

# pre_save.connect(validate_phone_number, sen)
