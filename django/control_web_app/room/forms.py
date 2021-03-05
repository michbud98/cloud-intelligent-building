from django import forms

from .models import Room

class Room_form(forms.ModelForm):
    class Meta:
        model = Room
        fields = "__all__"
        