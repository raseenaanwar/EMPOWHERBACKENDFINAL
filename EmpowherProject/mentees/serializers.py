from rest_framework import serializers
from accounts.models import CustomUser,MenteeProfile
from mentors.serializers import CustomUserSerializer
class MenteeSerializer(serializers.ModelSerializer):
    user=CustomUserSerializer(read_only=True)
    class Meta:
        model = MenteeProfile
        fields =['user', 'intro_as_mentee','development_goal', 'linkedin']


class MenteeGeneralProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = [ 'profession', 'country', 'timezone', 'language', 'profile_image','is_verified','is_blocked']