# mentors/urls.py

from django.urls import path
from .views import MentorBlockView, MentorListView
from . import views
from .views import RecentlyJoinedMentorsView
from .views import UserCountAPIView
from .views import *
urlpatterns = [
    path('mentor-list/', MentorListView.as_view(), name='mentor-list'),
    path('<int:pk>/block/', MentorBlockView.as_view(), name='mentor-block'),
    path('user-count/', UserCountAPIView.as_view(), name='user-count'),
    path('recently-joined-mentors/', RecentlyJoinedMentorsView.as_view(), name='recently_joined_mentors'),
    path('recently-joined-mentees/', RecentlyJoinedMenteesView.as_view(), name='recently_joined_mentees'),
    path('recently-joined-wellwishers/', RecentlyJoinedWellWishersView.as_view(), name='recently_joined_wellwishers'),
    path('user-counts/', UserCountsView.as_view(), name='user_counts'),

    path('create-general-user-profile/', views.create_general_user_profile),
    path('create-mentor-profile/', create_mentor_profile, name='create_mentor_profile'),
    path('get-mentor-profile/', views.get_mentor_profile,name='get-mentor-profile'),
    path('get_user_profile/', get_user_profile, name='get_user_profile'),
    path('mentor-detail/<int:pk>/', MentorDetailView.as_view(), name='mentor-detail'),
    path('mentor-availability/', views.save_mentor_availability, name='save_mentor_availability'),
    path('<int:mentor_id>/availability/', Availabletimeslots.as_view(), name='available-time-slots'),
    path('get-mentor-availability/', get_mentor_availability, name='get-mentor-availability'),
    path('get-mentor-availability2/', get_mentor_availability2, name='get-mentor-availability2'),
    path('get-slot-on-date/', get_slot_on_date, name='get-slot-on-date'),
    path('fetchdate/',views.get_mentor_date, name = 'fetchdate'),
    path('delete-mentor-availability/',delete_mentor_availability, name='delete-mentor-availability'),
    path('book_session/',book_session,name='book_session')


   
    

   
]

