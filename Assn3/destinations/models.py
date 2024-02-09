from django.db import models
from django.contrib.auth.models import User

class Destination(models.Model):
    name = models.CharField(max_length=100)
    review = models.TextField()
    rating = models.IntegerField()
    share_publicly = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)  # Provide the appropriate user ID here

    def __str__(self):
        return self.name