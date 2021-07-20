from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Patient(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    pic = models.URLField()
    address = models.CharField(max_length=250)
    city = models.CharField(max_length=250)
    state = models.CharField(max_length=250)
    zip = models.CharField(max_length=250)

    def __str__(self):
        return self.user.username
    
class Doctor(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    pic = models.URLField()
    address = models.CharField(max_length=250)
    city = models.CharField(max_length=250)
    state = models.CharField(max_length=250)
    zip = models.CharField(max_length=250)
    
    def __str__(self):
        return self.user.username