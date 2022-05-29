import os
from sys import maxsize
from django import forms
from django.forms import ModelForm, Textarea
from django.db import models
import datetime


GENDER_CHOICES = (('m','m'),('f','f'),('Other','Other'),)

def filepath(request, filename):
    old_filename = filename
    timeNow = datetime.datetime.now().strftime('%Y%m%d%H:%M:%S')
    filename = "%s%s" % (timeNow, old_filename)
    return os.path.join('media/', filename)

# Create your models here.
class Criminal_Face(models.Model):
    name=models.CharField(max_length=60)
    fathers_name=models.CharField(max_length=60)
    gender=models.CharField(choices=GENDER_CHOICES,max_length=5)
    age=models.IntegerField()
    crime=models.CharField(max_length=300)
    crime_image=models.ImageField(upload_to=filepath)



