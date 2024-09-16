from django.utils.timezone import make_aware
from datetime import datetime, timedelta
from .serializers import MentorProfileSerializer
from datetime import datetime
from django.http import JsonResponse
from rest_framework import generics
from accounts.models import CustomUser
from rest_framework.response import Response
from rest_framework import status
import json
from rest_framework.decorators import api_view
from .serializers import UserGeneralProfileSerializer,CustomUserSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from accounts.models import CustomUser,MentorProfile
from mentors.models import Availability, Booking_session
from django.shortcuts import get_object_or_404
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError
# from .models import Availability
from .serializers import AvailabilitySerializer
from datetime import date
from django.utils import timezone
from django.db.models import Q
from .tasks import send_confirmation_email, send_reminder_email
@api_view(['POST'])
def get_user_profile(request):
   
    try:
        email = request.data.get('email')
        
        user = CustomUser.objects.get(email=email)
        serializer = CustomUserSerializer(user)
        return Response(serializer.data, status=200)
    except CustomUser.DoesNotExist:
        return Response({'error': 'User not found'}, status=404)
    
@api_view(['POST'])
def get_mentor_profile(request):
   
    try:
        
        email=request.data.get('email')
        user = CustomUser.objects.get(email=email)
        # if not user.is_authenticated:
        #     return Response({"error": "User is not authenticated"}, status=status.HTTP_401_UNAUTHORIZED)
        profile = MentorProfile.objects.get(user=user)
        serializer = MentorProfileSerializer(profile)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except (CustomUser.DoesNotExist, MentorProfile.DoesNotExist):
        return Response({"error": "Profile not found"}, status=status.HTTP_404_NOT_FOUND)


class MentorListView(generics.ListAPIView):
    serializer_class = CustomUserSerializer
    
    def get_queryset(self):
        try:
            # Filter queryset to include only users with the role of "mentor"
            queryset = CustomUser.objects.filter(role='MENTOR')
            
            return queryset
        except:
            print("An error occurred while retrieving data.")
            return JsonResponse("Data retrieval failed", safe=False)
class MentorBlockView(generics.UpdateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.is_blocked = not instance.is_blocked
        instance.save()

        serializer = self.get_serializer(instance)  # Use the same serializer instance
        return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['POST'])
def create_mentor_profile(request):
    try:
        email = request.data.get('email')
        user = CustomUser.objects.get(email=email)
        
        # Update or create mentor profile
        profile, created = MentorProfile.objects.update_or_create(
            user=user,
            defaults={
                'intro_as_mentor': request.data.get('intro_as_mentor', ''),
                'mentoring_topics': request.data.get('mentoring_topics', ''),
                'area_of_expertise': request.data.get('area_of_expertise', []),
                'linkedin': request.data.get('linkedin', '')
            }
        )
        
        serializer = MentorProfileSerializer(profile)
        return Response(serializer.data, status=status.HTTP_200_OK if not created else status.HTTP_201_CREATED)
    except CustomUser.DoesNotExist:
        return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
@api_view(['POST','PUT'])
def create_general_user_profile(request):
   
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
def get_general_user_profile(request):
    
    user = request.user
    try:
        profile = CustomUser.objects.get(id=user.id)
        serializer = UserGeneralProfileSerializer(profile)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except CustomUser.DoesNotExist:
        return Response({"error": "Profile not found"}, status=status.HTTP_404_NOT_FOUND)
    
class MentorDetailView(APIView):
    print("inside mentor detail")
    def get(self, request, pk):
        print(pk)
        mentor = get_object_or_404(MentorProfile, pk=pk)
        serializer = MentorProfileSerializer(mentor)
        print(serializer.data)
        return Response(serializer.data)


class RecentlyJoinedMentorsView(generics.ListAPIView):
    serializer_class = MentorProfileSerializer
    print('inside recent mentors')

    def get_queryset(self):
        # return CustomUser.objects.filter(role='MENTOR').order_by('-date_joined')[:10]
         return CustomUser.objects.filter(role='MENTOR')

class UserCountAPIView(APIView):
    # permission_classes = [IsAuthenticated]
    print('inside user count')
    def get(self, request):
        print("insideget")
        mentors_count = CustomUser.objects.filter(role='MENTOR').count()
        mentees_count = CustomUser.objects.filter(role='MENTEE').count()
        wellwishers_count = CustomUser.objects.filter(role='WELLWISHER').count()
        print(mentors_count)
        return Response({
            'mentors_count': mentors_count,
            'mentees_count': mentees_count,
            'wellwishers_count': wellwishers_count,
        })
    

# @api_view(['POST'])
# def book_session(request):
#     data = request.data
#     print(data)
#     user = CustomUser.objects.get(email = data['email'])
#     available = Availability.objects.get(mentor = data['mentor_id'],date = data['date'], start_time = data['time'].split(' - ')[0],  end_time = data['time'].split(' - ')[1])
#     print(available.id)
#     available.status = True
#     available.save()
#     book = Booking_session.objects.create(user = user, description = data['reason'], available = available, status = 'booked')
#     book.save()
#     return Response({'message':'ok'})

@api_view(['POST'])
def book_session(request):
    data = request.data
    try:
        # Fetch the user (mentee) and availability
        user = CustomUser.objects.get(email=data['email'])
        available = Availability.objects.get(
            mentor=data['mentor_id'],
            date=data['date'],
            start_time=data['time'].split(' - ')[0],
            end_time=data['time'].split(' - ')[1]
        )
        
        # Update availability status
        available.status = True
        available.save()
        
        # Create a booking session
        book = Booking_session.objects.create(
            user=user,
            description=data['reason'],
            available=available,
            status='booked'
        )
        
        # Fetch the mentor's profile and email
        mentor = CustomUser.objects.get(id=data['mentor_id'])
        mentor_profile = MentorProfile.objects.get(user=mentor)
        mentor_email = mentor.email
        mentor_first_name = mentor.first_name
        mentor_profile_link = mentor_profile.linkedin
        video_call_url = mentor_profile.video_call_url
        
        # Fetch mentee details
        mentee_email = data['email']
        mentee_first_name = user.first_name
        
        # Define the meeting details
        meeting_details = f"Date: {data['date']}\nTime: {data['time']}\nReason: {data['reason']}"
        
        # Call the Celery task to send confirmation emails
        send_confirmation_email.delay(
            mentor_email, 
            mentee_email, 
            meeting_details, 
            video_call_url, 
            mentor_profile_link,
            mentee_first_name,
            data.get('message', 'No message from mentee')  # Ensure `mentee_message` is provided
        )
        
        # Calculate reminder times
        meeting_datetime = datetime.strptime(data['date'] + ' ' + data['time'].split(' - ')[0], '%Y-%m-%d %H:%M:%S')
        reminder_time_1_hour_before = make_aware(meeting_datetime - timedelta(hours=1))
        reminder_time_1_day_before = make_aware(meeting_datetime - timedelta(days=1))
        
        # Schedule reminders using apply_async
        send_reminder_email.apply_async(
            args=[mentor_email, mentee_email, mentor_first_name, mentee_first_name, meeting_details, video_call_url, mentor_profile_link],
            eta=reminder_time_1_hour_before
        )

        send_reminder_email.apply_async(
            args=[mentor_email, mentee_email, mentor_first_name, mentee_first_name, meeting_details, video_call_url, mentor_profile_link],
            eta=reminder_time_1_day_before
        )

        return Response({'message': 'ok'})
    
    except CustomUser.DoesNotExist:
        return Response({'message': 'User not found'}, status=404)
    except Availability.DoesNotExist:
        return Response({'message': 'Availability not found'}, status=404)
    except Exception as e:
        print(f"Error during booking or sending emails: {e}")
        return Response({'message': 'An error occurred'}, status=500)

@api_view(['POST'])
def save_mentor_availability(request):
    email = request.data.get('email')
    data = request.data
    
    availability_data = request.data.get('availability', [])
       
    try:
        user = CustomUser.objects.get(email=email)       
        mentor_profile = MentorProfile.objects.get(user=user)       
        mentor_profile.video_call_url = data.get('video_call_url')
        mentor_profile.save()        
        for entry in availability_data:          
            # Convert time to HH:MM:SS format if necessary
            try:
                start_time = datetime.strptime(entry['start_time'], '%H:%M').time()
                end_time = datetime.strptime(entry['end_time'], '%H:%M').time()
            except ValueError:
                return Response({'error': 'Time format must be HH:MM'}, status=status.HTTP_400_BAD_REQUEST)
            
            # Ensure times are in HH:MM:SS format
            start_time_str = start_time.strftime('%H:%M:%S')
            end_time_str = end_time.strftime('%H:%M:%S')
            
            
            # Create a dictionary with the data to pass to the serializer
            serializer_data = {
                'mentor': mentor_profile.pk,
                'date': entry['date'],
                'start_time': start_time_str,
                'end_time': end_time_str,
                'duration': entry['duration'],
            }
                      
            serializer = AvailabilitySerializer(data=serializer_data)
            
            if serializer.is_valid():
                serializer.save()
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        return Response({'message': 'Availability saved successfully!'}, status=status.HTTP_201_CREATED)

    except MentorProfile.DoesNotExist:
        return Response({'error': 'Mentor profile not found.'}, status=status.HTTP_404_NOT_FOUND)

    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def delete_mentor_availability(request):
    email = request.data.get('email')
    date = request.data.get('date')
    start = request.data.get('start')
    end = request.data.get('end')
    print("inside delete availability",email, date, start, end)
    if not (email and date and start and end):
        return Response({'error': 'Missing required parameters'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        
        availability = Availability.objects.get(
            mentor__user__email=email,
            date=date,
            start_time=start,
            end_time=end
        )
        
        availability.delete()
        return Response({'message': 'Availability deleted successfully'})
    except Availability.DoesNotExist:
        return Response({'error': 'Availability not found'}, status=status.HTTP_404_NOT_FOUND)

@api_view(['POST'])
def get_mentor_availability(request):
    email = request.data.get('uemail')
    mentor_id = request.data.get('myParam')
    print(mentor_id)
    try:
        
        mentor_profile = MentorProfile.objects.get(user_id=mentor_id)
        
        mentor_profile_serializer = MentorProfileSerializer(mentor_profile)
        now = timezone.now()

        availabilities = mentor_profile.availabilities.filter(
            Q(date__gt=now.date()) |
            (Q(date=now.date()) & Q(start_time__gte=now.time()))
        )
        
        availability_serializer = AvailabilitySerializer(availabilities, many=True)
        return Response({
            'mentor_profile': mentor_profile_serializer.data,
            'availabilities': availability_serializer.data
        })
    except MentorProfile.DoesNotExist:
        return Response({'error': 'Mentor profile not found'}, status=404)

@api_view(['POST'])
def get_mentor_availability2(request):
    email = request.data.get('email')  
    mentor = CustomUser.objects.get( email = email)
    try:
        
        mentor_profile = MentorProfile.objects.get(user_id=mentor)
        
        mentor_profile_serializer = MentorProfileSerializer(mentor_profile)
        now = timezone.now()

        availabilities = mentor_profile.availabilities.filter(
            Q(date__gt=now.date()) |
            (Q(date=now.date()) & Q(start_time__gte=now.time()))
        )
        
        availability_serializer = AvailabilitySerializer(availabilities, many=True)
        return Response({
            'mentor_profile': mentor_profile_serializer.data,
            'availabilities': availability_serializer.data
        })
    except MentorProfile.DoesNotExist:
        return Response({'error': 'Mentor profile not found'}, status=404)
    
class Availabletimeslots(generics.ListAPIView):
    serializer_class = AvailabilitySerializer

    def get_queryset(self):
        mentor_id = self.kwargs.get('mentor_id')
        return Availability.objects.filter(id=mentor_id)

    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        print(queryset)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)



@api_view(['POST'])
def get_mentor_date(request):
    print('entered into mentor date')
    data = request.data
    try:
        mentor_profile = MentorProfile.objects.get(user=data['id'])
        availabilities = Availability.objects.filter(mentor_profile=mentor_profile)
        serializer = AvailabilitySerializer(availabilities, many=True)
        
        return Response(serializer.data, status=status.HTTP_200_OK)
    except MentorProfile.DoesNotExist:
        return Response({'error': 'Mentor not found'}, status=status.HTTP_404_NOT_FOUND)

class RecentlyJoinedMentorsView(generics.ListAPIView):
    serializer_class = CustomUserSerializer
    print(serializer_class.data)
    
    def get_queryset(self):
        return CustomUser.objects.filter(user_type=CustomUser.MENTOR).order_by('-date_joined')[:5]  # Limit to 5 most recent mentors

class RecentlyJoinedMenteesView(generics.ListAPIView):
    serializer_class = CustomUserSerializer
    
    def get_queryset(self):
        return CustomUser.objects.filter(user_type=CustomUser.MENTEE).order_by('-date_joined')[:5]  # Limit to 5 most recent mentees

class RecentlyJoinedWellWishersView(generics.ListAPIView):
    serializer_class = CustomUserSerializer
    
    def get_queryset(self):
        return CustomUser.objects.filter(user_type=CustomUser.WELLWISHER).order_by('-date_joined')[:5]  # Limit to 5 most recent well-wishers

class UserCountsView(generics.GenericAPIView):
    def get(self, request, *args, **kwargs):
        counts = {
            'mentors': CustomUser.objects.filter(user_type=CustomUser.MENTOR).count(),
            'mentees': CustomUser.objects.filter(user_type=CustomUser.MENTEE).count(),
            'wellWishers': CustomUser.objects.filter(user_type=CustomUser.WELLWISHER).count()
        }
        return Response(counts)
    


@api_view(['POST'])
def get_slot_on_date(request):
    email = request.data.get('email')
    mentor_id = request.data.get('myParam')
    date = request.data.get('date')
    print(email,mentor_id,date)
    # Fetch availabilities for the given mentor and date
    availabilities = Availability.objects.filter(mentor_id=mentor_id, date=date)
    
    # Serialize the data
    serializer = AvailabilitySerializer(availabilities, many=True)
    print("inside get slot",serializer.data)
    return Response({'time_slots': serializer.data})


def schedule_meeting(request):
    # Your code to handle scheduling

    mentor_email = 'mentor@example.com'
    mentee_email = 'mentee@example.com'
    meeting_details = '2024-08-15 10:00 AM'

    # Call the Celery task
    send_confirmation_email.delay(mentor_email, mentee_email, meeting_details)
    return HttpResponse("Meeting scheduled and confirmation email sent.")