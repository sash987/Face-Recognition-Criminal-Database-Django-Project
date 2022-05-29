from django.contrib import admin
from .models import *

@admin.register(Criminal_Face)

class Criminal_Face_Admin(admin.ModelAdmin):
    list_display = ('id','name','fathers_name','gender','age','crime','crime_image')





