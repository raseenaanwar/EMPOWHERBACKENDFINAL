from django.db import models
from accounts.models import MentorProfile,CustomUser

class Availability(models.Model):
    mentor = models.ForeignKey(MentorProfile, on_delete=models.CASCADE, related_name='availabilities', to_field='user')
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    duration = models.PositiveIntegerField()  # duration in minutes
    status = models.BooleanField(default=False)   

    def __str__(self):
        return f"{self.mentor.user.email} - {self.date} {self.start_time}-{self.end_time} ({self.duration} mins)"

class Booking_session(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    description = models.TextField()
    available = models.ForeignKey(Availability, on_delete = models.CASCADE)
    booked_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20)