from django.http import JsonResponse
from rest_framework import generics
from accounts.models import CustomUser,MenteeProfile
from .serializers import MenteeSerializer,MenteeGeneralProfileSerializer
from mentors.serializers import UserGeneralProfileSerializer,CustomUserSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view

class MenteeListView(generics.ListAPIView):
    serializer_class = MenteeSerializer
    
    def get_queryset(self):
        try:
            # Filter queryset to include only users with the role of "mentor"
            queryset = CustomUser.objects.filter(role='MENTEE')
            return queryset
        except:
            print("An error occurred while retrieving data.")
            return JsonResponse("Data retrieval failed", safe=False)

class MenteeBlockView(generics.UpdateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    
    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        
        # Invert the current value of is_blocked
        instance.is_blocked = not instance.is_blocked
        
        instance.save()
        
        serializer = CustomUserSerializer(instance)  # Instantiate the serializer with the updated instance
        return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
def get_mentee_user_profile(request):
   
    try:
        email = request.data.get('email')
        
        user = CustomUser.objects.get(email=email)
        serializer = CustomUserSerializer(user)
        return Response(serializer.data, status=200)
    except CustomUser.DoesNotExist:
        return Response({'error': 'User not found'}, status=404)
    
@api_view(['POST'])
def get_mentee_profile(request):
   
    try:
        
        email=request.data.get('email')
        user = CustomUser.objects.get(email=email)
        # if not user.is_authenticated:
        #     return Response({"error": "User is not authenticated"}, status=status.HTTP_401_UNAUTHORIZED)
        profile = MenteeProfile.objects.get(user=user)
        serializer = MenteeSerializer(profile)
        print(serializer)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except (CustomUser.DoesNotExist, MenteeProfile.DoesNotExist):
        return Response({"error": "Profile not found"}, status=status.HTTP_404_NOT_FOUND)


@api_view(['POST'])
def create_mentee_profile(request):
    try:
        email = request.data.get('email')
        user = CustomUser.objects.get(email=email)
        
        # Update or create mentor profile
        profile, created = MenteeProfile.objects.update_or_create(
            user=user,
            defaults={
                'intro_as_mentee': request.data.get('intro_as_mentee', ''),
                'development_goal': request.data.get('development_goal', ''),
                'linkedin': request.data.get('linkedin', '')
            }
        )
        
        serializer = MenteeSerializer(profile)
        return Response(serializer.data, status=status.HTTP_200_OK if not created else status.HTTP_201_CREATED)
    except CustomUser.DoesNotExist:
        return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
@api_view(['POST','PUT'])
def create_mentee_general_user_profile(request):
   
    if request.method in ['POST','PUT']:
        # Access form data and make a mutable copy
        form_data = request.POST.copy()
        # Access files data
        files_data = request.FILES
        # Get user by email
        try:
            user = CustomUser.objects.get(email=form_data['email'])
            
        except CustomUser.DoesNotExist:
            return Response('User not found', status=status.HTTP_404_NOT_FOUND)

        # Remove the email field from the form data
        if 'email' in form_data:
            del form_data['email']

        # Update fields of the user object
        user.first_name = form_data.get('first_name', user.first_name)
        user.last_name = form_data.get('last_name', user.last_name)
        user.profession = form_data.get('profession', user.profession)
        user.country = form_data.get('country', user.country)
        user.timezone = form_data.get('timezone', user.timezone)
        user.language = form_data.get('language', user.language)

      
        if 'profile_image' in files_data:
            user.profile_image = files_data['profile_image']

        # Save the updated user object
        user.save()

        # Serialize the updated user data
        serializer = UserGeneralProfileSerializer(user)

        # Return a success response with the updated user data
        return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
def get_mentee_general_user_profile(request):
    
    user = request.user
    try:
        profile = CustomUser.objects.get(id=user.id)
        serializer = UserGeneralProfileSerializer(profile)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except CustomUser.DoesNotExist:
        return Response({"error": "Profile not found"}, status=status.HTTP_404_NOT_FOUND)
    
# class MentorDetailView(APIView):
#     print("inside mentor detail")
#     def get(self, request, pk):
#         print(pk)
#         mentor = get_object_or_404(MentorProfile, pk=pk)
#         serializer = MentorProfileSerializer(mentor)
#         print(serializer.data)
#         return Response(serializer.data)

class MenteeListView(generics.ListAPIView):
    serializer_class = CustomUserSerializer
    
    def get_queryset(self):
        try:
            # Filter queryset to include only users with the role of "mentor"
            queryset = CustomUser.objects.filter(role='MENTEE')
            
            return queryset
        except:
            print("An error occurred while retrieving data.")
            return JsonResponse("Data retrieval failed", safe=False)