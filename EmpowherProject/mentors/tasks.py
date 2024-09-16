from celery import shared_task
from django.core.mail import send_mail
import logging
logger = logging.getLogger(__name__)
@shared_task
def send_confirmation_email(mentor_email, mentee_email, meeting_details, video_call_url, mentor_profile_link, mentee_first_name, mentee_message):
    subject = "Session Booking Confirmation"
    
    # Email body for the mentee
    mentee_message_body = (
        f"Dear {mentee_first_name},\n\n"
        f"Congratulations! You successfully booked a mentoring session with {mentor_profile_link}. For you to prepare well and to have a great session, we'd like to give you a few tips:\n\n"
        f"1. Take a moment to write down what you really want to achieve with this session. Do you have a specific goal in mind or at least a clear problem statement?\n"
        f"2. List your key questions that you would like to ask during the session.\n"
        f"3. Please make sure that you can show up and arrive on time for your appointment. Be aware that our mentors donate their time for you. If you don't show up without letting the mentor know before, it's like tearing through a bank note after someone gave it to you as a present.\n\n"
        f"On the day of the session, you can access the video call using this link: {video_call_url}\n\n"
        f"In case of a no-show without noticing the mentor at least 24 hours before the session, we might block your account for 30 days.\n\n"
        f"You can reach out to your mentor using our chat!\n\n"
        f"We wish you a great session and all the best in your development and career journey!\n\n"
        f"The Empowher Team"
    )
    
    # Email body for the mentor
    mentor_message_body = (
        f"Dear Mentor,\n\n"
        f"Congratulations! {mentee_email} booked a session with you as their mentor. We are pretty sure this session will be super helpful for your mentee and hopefully for you as well. "
        f"After the session, make sure to mark your session as 'Done' or - in case the mentee did not show up - as a 'No Show'. This allows us to keep the quality for you and your fellow mentors high.\n\n"
        f"{mentee_email} has left a message for you:\n"
        f"{mentee_message}\n\n"
        f"If you like to get in contact with your mentee before the session, you can write them an email: {mentee_email}\n\n"
        f"You can reach out to your mentee using our chat!\n\n"
        f"We wish you a great session. Thank you so much for being a member of our platform and donating your time.\n\n"
        f"All the Best,\n"
        f"The Empowher Team"
    )

    # Sending email to the mentor
    send_mail(
        subject,
        mentor_message_body,
        'noreply@example.com',  # From address
        [mentor_email],         # To address
    )
    
    # Sending email to the mentee
    send_mail(
        subject,
        mentee_message_body,
        'noreply@example.com',  # From address
        [mentee_email],         # To address
    )
@shared_task
def send_reminder_email(mentor_email, mentee_email, mentor_first_name, mentee_first_name, meeting_details, video_call_url, mentor_profile_link):
    try:
        subject = "Reminder: Upcoming Session"

        # Email body for the mentee
        mentee_message_body = (
            f"Dear Mentee {mentee_first_name},\n\n"
            f"This is a friendly reminder about your upcoming mentoring session with mentor {mentor_first_name}.\n\n"
            f"Session Details:\n"
            f"{meeting_details}\n\n"
            f"You can access the video call using this link: {video_call_url}\n\n"
            f"Please make sure you are prepared and arrive on time.\n\n"
            f"We look forward to a productive session!\n\n"
            f"Best Regards,\n"
            f"The Empowher Team"
        )
        
        # Email body for the mentor
        mentor_message_body = (
            f"Dear Mentor {mentor_first_name},\n\n"
            f"This is a friendly reminder about your upcoming session with mentee {mentee_first_name}.\n\n"
            f"Session Details:\n"
            f"{meeting_details}\n\n"
            f"You can access the video call using this link: {video_call_url}\n\n"
            f"Please ensure you are available and prepared for the session.\n\n"
            f"Thank you for your time and dedication!\n\n"
            f"Best Regards,\n"
            f"The Empowher Team"
        )

        # Sending reminder email to the mentor
        send_mail(
            subject,
            mentor_message_body,
            'noreply@example.com',  # From address
            [mentor_email],         # To address
        )
        
        # Sending reminder email to the mentee
        send_mail(
            subject,
            mentee_message_body,
            'noreply@example.com',  # From address
            [mentee_email],         # To address
        )
    except Exception as e:
        logger.error(f"Failed to send reminder email: {e}")
