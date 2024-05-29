from django.db import models
#from authentication.models import User
from django.conf import settings


class Event(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    date = models.DateTimeField()
    #organizer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='events')
    organizer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='events')

    def __str__(self):
        return self.title
    

class Registration(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    #user = models.ForeignKey(User, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.username} - {self.event.title}'