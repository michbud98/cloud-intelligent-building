from django import forms

from .models import Device, Thermo_head, Sunblind

class Device_form(forms.ModelForm):
    class Meta:
        model = Device
        fields = [
            "device_type",
            "device_id",
            "room"
        ]
        labels = {
            'device_type': "Device type T-Thermostatic head / S - sunblind"
        }

    def clean_device_id(self):
        device_id = self.cleaned_data.get("device_id")
        device_type = self.cleaned_data.get("device_type")
        final_device_id = ""

        if device_type == "sunblind":
            final_device_id = f"B{device_id}"
        elif device_type == "thermo_head":
            final_device_id = f"T{device_id}"
        else:
            raise forms.ValidationError(f"Cant add device type {device_type}")
        
        return final_device_id


class Thermo_head_form(Device_form):
    device_id = forms.CharField(label='Device_id_number', widget=forms.NumberInput)
    class Meta(Device_form.Meta):
        model = Thermo_head

class Sunblind_form(Device_form):
    device_id = forms.CharField(label='Device_id_number', widget=forms.NumberInput)
    class Meta(Device_form.Meta):
        model = Sunblind
        
class Thermo_head_values_form(Device_form):
    class Meta(Device_form.Meta):
        model = Thermo_head
        fields = [
            "set_heat_value",
        ]
        labels = {
            'set_heat_value': "Heat value"
        }

class Sunblind_values_form(Device_form):
    class Meta(Device_form.Meta):
        model = Sunblind
        fields = [
            "set_open_value",
        ]