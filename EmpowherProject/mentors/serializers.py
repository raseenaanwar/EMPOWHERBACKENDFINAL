

from accounts.models import CustomUser
from accounts.models import MentorProfile
from rest_framework import serializers
from .models import  Availability,Booking_session

class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id','first_name', 'last_name', 'profile_image', 'profession','email', 'country', 'timezone', 'language','date_joined','is_verified','is_blocked']
        
class MentorProfileSerializer(serializers.ModelSerializer):
    user = CustomUserSerializer(read_only=True)

    class Meta:
        model = MentorProfile
        fields = ['user', 'intro_as_mentor', 'mentoring_topics', 'area_of_expertise', 'linkedin', 'video_call_url']

    
class UserGeneralProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = [ 'profession', 'country', 'timezone', 'language', 'profile_image']

class AvailabilitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Availability
        fields = ['id', 'mentor', 'date', 'start_time', 'end_time', 'duration', 'status']

class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking_session
        fields = '__all__'