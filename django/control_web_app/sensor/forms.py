from django import forms

from .models import Sensor
from room.models import Room
from . import queries

class Sensor_form(forms.ModelForm):
    LOCATION_CHOICES = [("indoors", "Indoors"), ("outdoors", "Outdoors"),("boiler", "Boiler")]
    
    # [("value saved", "Text seen in select"), ("same", "same")]
    room_choices = [(None, "----")]
    # rooms_set = Room.objects.all()
    # for room in rooms_set:
    #     room_choices.append((room.id, room.room_name))
    sensor_id = forms.CharField(disabled = True)
    hostname = forms.CharField(disabled = True) 
    sensor_type = forms.CharField(disabled = True) 
    location = forms.CharField(label='Choose where sensor is located:', widget=forms.RadioSelect(choices=LOCATION_CHOICES))
    description = forms.CharField(required=False, widget=forms.Textarea(attrs={ "rows": 5 }))
    class Meta:
        model = Sensor
        fields = "__all__"

    # def clean_sensor_id

    def clean_location(self):
        sensor_id = self.cleaned_data.get("sensor_id")
        location = self.cleaned_data.get("location")

        sensor_fields = queries.query_sensor_fields(sensor_id)
        if ['dhw_coil_temp', 'dhw_tmp', 'tmp_in', 'tmp_out'] == sensor_fields and location != "boiler":
            raise forms.ValidationError("This sensor collects data boiler data and because of that location must be set to boiler")
        elif ['humidity', 'pressure', 'temperature'] == sensor_fields and location == "boiler":
            raise forms.ValidationError("This sensor collects data weather data and because of that location must be set to indoors/outdors")
        else:
            return location
        
    def clean_room(self):
        location = self.cleaned_data.get("location")
        room = self.cleaned_data.get("room")
        
        if location == "outdoors" and room is not None:
            raise forms.ValidationError("Location outdoors can't have set room")
        if location == "boiler" and room is not None:
            raise forms.ValidationError("Boiler can't have set room")
        else:
            return room
        
