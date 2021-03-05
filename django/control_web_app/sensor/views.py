from django.shortcuts import render, get_object_or_404
from django.template.defaulttags import register
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required

from . import queries
from .models import Sensor
from .forms import Sensor_form
from room.models import Room


@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)

# Create your views here.
@login_required
def sensor_list_view(request):
    unset_list, set_list, boiler_list = queries.sort_sensor_ids(queries.query_all_tag_values("sensor_id"))
    hostname_dict = queries.create_hostname_dict(queries.query_all_tag_values("sensor_id"))
    sensor_type_dict = queries.create_sensor_type_dict(queries.query_all_tag_values("sensor_id"))
    
    my_context = {
        "hostname_dict" : hostname_dict,
        "sensor_type_dict" : sensor_type_dict,
        "sensor_id_list_nonset": unset_list,
        "sensor_id_list_set": set_list,
        "boiler_list": boiler_list
    }
    return render(request, "sensor_list.html", my_context)

@login_required
def sensor_create_view(request, sensor_id, hostname, sensor_type):
    # TODO Might be a good idea to add some try catch or something like that
    initial_data = { "sensor_id": sensor_id, "hostname": hostname, "sensor_type": sensor_type}
    my_context = {}
    if request.method == "POST":
        form = Sensor_form(request.POST, initial=initial_data)
        if form.is_valid():
            form.save()
            return redirect(sensor_list_view)
        else:
            form = Sensor_form(request.POST, initial=initial_data)
            my_context ={
                'form':form,
            }
    else:
        form = Sensor_form(initial=initial_data)
        my_context ={
            'form':form,
        }
    
    return render(request, "sensor_create.html", my_context)

@login_required
def sensor_update_view(request, sensor_id):
    obj = get_object_or_404(Sensor, sensor_id=sensor_id)
    form = Sensor_form(request.POST or None, instance=obj)
    if request.method == "POST":
        if form.is_valid():
            form.save()
            return redirect(sensor_list_view)
    if form.is_valid():
        form.save()
    context = {
        'form': form
    }
    return render(request, "sensor_create.html", context)

@login_required
def sensor_remove_view(request, sensor_id):
    obj = get_object_or_404(Sensor, sensor_id=sensor_id)
    if request.method == "POST":
        obj.delete()
        return redirect(sensor_list_view)

    my_context = {
        "obj": obj,
    }
    return render(request, "sensor_delete.html", my_context)

@login_required
def sensor_detail_view(request, sensor_id):
    obj, temperature, pressure, humidity  = None, None, None, None
    tmp_in, tmp_out, dwh_tmp, dhw_coil_temp = None, None, None, None
    boiler_bool = None
    try:
        obj = Sensor.objects.get(sensor_id=sensor_id)
        if obj.location != "boiler":
            temperature, pressure, humidity = queries.get_sensor_values(obj.sensor_id)
            boiler_bool = False
        elif obj.location == "boiler":
            tmp_in, tmp_out, dwh_tmp, dhw_coil_temp = queries.get_boiler_values(obj.sensor_id)
            boiler_bool = True
    except Sensor.DoesNotExist:
        sensor_fields = queries.query_sensor_fields(sensor_id)
        if ['dhw_coil_temp', 'dhw_tmp', 'tmp_in', 'tmp_out'] != sensor_fields:
            temperature, pressure, humidity = queries.get_sensor_values(sensor_id)
            boiler_bool = False
        elif ['dhw_coil_temp', 'dhw_tmp', 'tmp_in', 'tmp_out'] == sensor_fields:
            tmp_in, tmp_out, dwh_tmp, dhw_coil_temp = queries.get_boiler_values(sensor_id)
            boiler_bool = True
        else:
            print(sensor_fields)
            raise Except(sensor_fields)
    
    my_context = {
            "sensor_id": sensor_id, "obj" : obj,
            "temperature": temperature, "pressure": pressure, "humidity": humidity,
            "tmp_in": tmp_in, "tmp_out": tmp_out, "dhw_tmp": dwh_tmp, "dhw_coil_temp": dhw_coil_temp,
            "boiler_bool": boiler_bool
        }
    return render(request, "sensor_detail.html", my_context)
