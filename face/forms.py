from tkinter import Widget
from django import forms
from face.models import *
from django.forms import ModelForm

class Criminal_form(forms.ModelForm):
    class Meta:
        model = Criminal_Face
        fields = ['name','fathers_name','gender','age','crime','crime_image',]
        widgets = {
            'name':forms.TextInput(attrs={'class':'form-control'}),
            'fathers_name':forms.TextInput(attrs={'class':'form-control'}),
            'gender':forms.TextInput(attrs={'class':'form-control'}),
            'age':forms.TextInput(attrs={'class':'form-control'}),
            'crime':forms.TextInput(attrs={'class':'form-control'}),
            'crime_image':forms.FileInput(attrs={'class':'form-control'}),
        }
