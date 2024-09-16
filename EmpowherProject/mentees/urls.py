# mentors/urls.py

from django.urls import path
from .views import *
from . import views

urlpatterns = [
    

    path('mentee-list/', MenteeListView.as_view(), name='mentee-list'),
    path('<int:pk>/block/', MenteeBlockView.as_view(), name='mentee-block'),
    path('create-mentee-general-user-profile/', views.create_mentee_general_user_profile),
    path('create-mentee-profile/', create_mentee_profile, name='create_mentee_profile'),
    path('get-mentee-profile/', views.get_mentee_profile,name='get-mentee-profile'),
    path('get-mentee-user-profile/', get_mentee_user_profile, name='get_mentee_user_profile'   ),
    
]
