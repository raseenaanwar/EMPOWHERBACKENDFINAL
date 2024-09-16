import random
from django.conf import settings
from django.core.mail import EmailMessage
from django.core.mail import send_mail
from accounts.models import CustomUser,OneTimePassword
def generateOtp():
    otp=""
    for i in range(6):
        otp+=str(random.randint(1,9))
    return otp

def send_code_to_user(email):
    subject="One time passcode for Email verification"
    otp_code=generateOtp()
    print(otp_code)
    user=CustomUser.objects.get(email=email)
    message=f"Hi {user.first_name} Thanks for signing up , Please verify your email with one time pass code {otp_code}"
    from_email=settings.EMAIL_HOST_USER
    OneTimePassword.objects.create(user=user,code=otp_code)
    # d_email=EmailMessage(subject=Subject,body=email_body,from_email=from_email,to=[email])
    # d_email.send(fail_silently=True)
    send_mail(subject, message, from_email, [email], fail_silently=True)

def send_normal_email(data):
    email=EmailMessage(
        subject=data['email_subject'],
        body=data['email_body'],
        from_email=settings.EMAIL_HOST_USER,
        to=data['to_email']


    )
    email.send()
