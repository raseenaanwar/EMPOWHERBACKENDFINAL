from django.shortcuts import redirect, render
from rest_framework.generics import GenericAPIView
from rest_framework.views import APIView
from mentors.serializers import CustomUserSerializer
from .serializers import UserRegisterSerializer,LoginSerializer,PasswordResetRequestSerializer,SetNewPasswordSerializer,LogoutUserSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .utils import send_code_to_user
from .models import OneTimePassword
from rest_framework.decorators import api_view
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import smart_str,DjangoUnicodeDecodeError
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from .models import CustomUser

class RegisteruserView(GenericAPIView):
    serializer_class=UserRegisterSerializer

    def post(self,request):
        user_data=request.data
        serializer=self.serializer_class(data=user_data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            user=serializer.data
            # send email function
            send_code_to_user(user_data['email'])
            return Response({
                'data':user,
                'message':f"hi{user_data.get('first_name','user')} Check your mail for otp"
            },status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

class VerifyUserEmail(GenericAPIView):
    def post(self,request):
        otecode=request.data.get('otp')
        print(otecode)
        try:
            user_code_obj=OneTimePassword.objects.get(code=otecode)
            user=user_code_obj.user
            if not user.is_verified:
                user.is_verified=True
                user.save()
                
                return Response({
                    "message":"Account Email Verified successfully"
                },status=status.HTTP_200_OK)
            return Response({
                'message':"Code is invalid as the user is already verified"
                },status=status.HTTP_204_NO_CONTENT)
        except OneTimePassword.DoesNotExist:
            return Response({"message":'Passcode Not Provided'},status=status.HTTP_400_BAD_REQUEST)

class LoginUserView(GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
       
        return Response(serializer.data, status=status.HTTP_200_OK)

class PasswordResetRequestView(GenericAPIView):
    serializer_class=PasswordResetRequestSerializer
    def post(self,request):
        serializer=self.serializer_class(data=request.data,context={'request':request})
        serializer.is_valid(raise_exception=True)
        return Response({"message":"A link has been sent to your email to reset your passwprd"},status=status.HTTP_200_OK)
    
class PasswordResetConfirm(GenericAPIView):
    def get(self,request,uidb64,token):
        try:
            user_id=smart_str(urlsafe_base64_decode(uidb64))
            user=CustomUser.objects.get(id=user_id)
            if not PasswordResetTokenGenerator().check_token(user,token):
                return Response({'message':"Token is invalid or has expired"},status=status.HTTP_401_UNAUTHORIZED)
            return Response({'success':True,"message":"Credentials are valid","uidb64":uidb64,"token":token},status=status.HTTP_200_OK)
        except DjangoUnicodeDecodeError:
            return Response({"message":"token is invalid or has expired"},status=status.HTTP_401_UNAUTHORIZED) 
               
class SetNewPassword(GenericAPIView):
    serializer_class=SetNewPasswordSerializer
    def patch(self,request):
        serializer=self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response({"message":"Password reset successful"},status=status.HTTP_200_OK)
    
class LogoutUserView(GenericAPIView):
    serializer_class=LogoutUserSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer=self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return redirect('/')
    
class TestAuthenticationView(GenericAPIView):
    permission_classes=[IsAuthenticated]
    def get(self,request):
        data={
            "msg":"working"
        }
        return Response(data,status=status.HTTP_200_OK)
    



@api_view(['GET'])
def get_user_details(request):
    email = request.query_params.get('email')
    try:
        user = CustomUser.objects.get(email=email)
        user_serializer = CustomUserSerializer(user)
        return Response(user_serializer.data, status=status.HTTP_200_OK)
    except CustomUser.DoesNotExist:
        return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)