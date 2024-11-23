from django.db import models
from django.contrib.auth.models import User

class Event(models.Model ) :
    title = models.CharField(max_length=100)
    start = models.DateTimeField(blank = False , null = False)
    end = models.DateTimeField(blank = False , null = False ) 
    user = models.ForeignKey(User , on_delete= models.CASCADE)

    def __str__(self) :
        return self.title