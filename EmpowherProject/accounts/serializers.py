from django.utils.encoding import smart_str,smart_bytes,force_str
from django.conf import settings
from django.core.mail import send_mail
from rest_framework import serializers
from django.contrib.auth import authenticate
from rest_framework.exceptions import AuthenticationFailed
from accounts.models import CustomUser
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.http import urlsafe_base64_decode,urlsafe_base64_encode
from django.utils.encoding import smart_str,smart_bytes,force_str
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from .utils import send_normal_email
from rest_framework_simplejwt.tokens import RefreshToken,TokenError

class UserRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(min_length=6, write_only=True)
    password2 = serializers.CharField(min_length=6, write_only=True)

    class Meta:
        model = CustomUser
        fields = ("first_name", "last_name", "role", "email", "password", "password2")

    def validate(self, attrs):
        password = attrs.get('password', '')
        password2 = attrs.get('password2', '')
        if password != password2:
            raise serializers.ValidationError("Passwords do not match")
        # Add email validation
        if CustomUser.objects.filter(email=attrs['email']).exists():
            raise serializers.ValidationError("User with this email already exists.")
        return attrs

    def create(self, validated_data):
        user = CustomUser.objects.create(
            email=validated_data["email"],
            first_name=validated_data["first_name"],
            last_name=validated_data["last_name"],
            role=validated_data["role"],
        )
        user.set_password(validated_data["password"])
        user.save()
        return user

class LoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=255, min_length=6)
    password = serializers.CharField(max_length=68, write_only=True)
    first_name = serializers.CharField(max_length=255, read_only=True)
    access_token = serializers.CharField(max_length=255, read_only=True)
    refresh_token = serializers.CharField(max_length=255, read_only=True)
    role = serializers.CharField(max_length=50, read_only=True)  # Add role field

    class Meta:
        model = CustomUser
        fields = ['email', 'password', 'first_name', 'access_token', 'refresh_token', 'role']

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')
        request = self.context.get('request')
        user = authenticate(request, email=email, password=password)
        if not user:
            raise AuthenticationFailed("Invalid credentials. Please try again.")
        if not user.is_verified:
            raise AuthenticationFailed("Email is not verified.")
        print("inside seriloazer")
        user_tokens = user.tokens()
        print(user_tokens)
        return {
            'email': user.email,
            'first_name': user.first_name,
            'access_token': str(user_tokens.get('access')),
            'refresh_token': str(user_tokens.get('refresh')),
            'role': user.role  # Return the user's role
        }

class PasswordResetRequestSerializer(serializers.Serializer):
    email=serializers.EmailField(max_length=255)

    class Meta:
        fields=['email']

    def validate(self,attrs):
        email=attrs.get('email')
        frontend_url = settings.FRONTEND_URL  # Retrieve frontend URL from settings
        abslink = f"{frontend_url}{relative_link}"  # Construct absolute link
        if  CustomUser.objects.filter(email=email).exists():
            user=CustomUser.objects.get(email=email)
            uidb64=urlsafe_base64_encode(smart_bytes(user.id))
            token=PasswordResetTokenGenerator().make_token(user)
            request=self.context.get('request')
            site_domain=get_current_site(request).domain
            relative_link=reverse('password-reset-confirm',kwargs={"uidb64":uidb64,"token":token})
            abslink=f"http://{site_domain}{relative_link}"
            email_body=f"Hi Use the following link to reset your password\n {abslink}"
            # data={
            #         'email_body':email_body,
            #         'email_subject':"Reset Your Password",
            #         'to_email':user.email
            # }
            # send_normal_email(data)
            send_mail(
                subject="Reset Your Password",
                message=email_body,
                from_email="your_email@example.com",
                recipient_list=[user.email],  # Ensure user.email is in a list or tuple
                fail_silently=False,
            )
        return super().validate(attrs)

class SetNewPasswordSerializer(serializers.Serializer):
    password=serializers.CharField(max_length=100,min_length=6,write_only=True)
    confirm_password=serializers.CharField(max_length=100,min_length=6,write_only=True)
    uidb64=serializers.CharField(write_only=True)
    token=serializers.CharField(write_only=True)

    class Meta:
        fields=['password','confirm_password','uidb64','token']
    def validate(self, attrs):
        try:
            password = attrs.get("password")
            token = attrs.get("token")
            uidb64 = attrs.get("uidb64")
            confirm_password=attrs.get('confirm_password')
            user_id=force_str(urlsafe_base64_decode(uidb64))
            user=CustomUser.objects.get(id=user_id)
            if not PasswordResetTokenGenerator().check_token(user,token):
                raise AuthenticationFailed("reset link is invalid or has expired",401)
            if password !=confirm_password:
                raise AuthenticationFailed("Passwords do not match")
            user.set_password(password)
            user.save()
            return user     
        except Exception as e:
            return AuthenticationFailed("Link is invalid or has expired")   
            
        
class LogoutUserSerializer(serializers.Serializer):
    refresh_token=serializers.CharField()

    default_error_message = {
        'bad_token': ('Token is expired or invalid')
    }

    def validate(self, attrs):
        self.token = attrs.get('refresh_token')
        return attrs

    def save(self, **kwargs):
        try:
            token=RefreshToken(self.token)
            token.blacklist()
        except TokenError:
            return self.fail('bad_token')
 
        return self.fail("bad_token")