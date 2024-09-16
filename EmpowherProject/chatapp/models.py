from django.db import models
from django.utils import timezone
from django.conf import settings

class Chat(models.Model):
    mentor = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='mentor_chats', on_delete=models.CASCADE, limit_choices_to={'user_type': 'mentor'})
    mentee = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='mentee_chats', on_delete=models.CASCADE, limit_choices_to={'user_type': 'mentee'})
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f'Chat between {self.mentor.email} and {self.mentee.email}'

class Message(models.Model):
    chat = models.ForeignKey(Chat, related_name='messages', on_delete=models.CASCADE)
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='sent_messages', on_delete=models.CASCADE)
    message_text = models.TextField(blank=True)
    message_type = models.CharField(max_length=10, choices=[('text', 'Text'), ('file', 'File')], default='text')
    attachment_url = models.URLField(blank=True, null=True)  # URL to the attachment if message_type is 'file'
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f'Message from {self.sender.email} at {self.created_at}'

class Attachment(models.Model):
    message = models.OneToOneField(Message, related_name='attachment', on_delete=models.CASCADE)
    file_url = models.URLField()  # URL to the file
    file_type = models.CharField(max_length=50)  # MIME type of the file
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f'Attachment for message {self.message.id}'