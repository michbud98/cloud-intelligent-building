from django.shortcuts import render

from . import queries

# Create your views here.
def home_view(request):
    avg_tmp_indoors, avg_pres_indoors, avg_hum_indoors = queries.query_avg_values_from_location("indoors")
    avg_tmp_out, avg_pres_out, avg_hum_out = queries.query_avg_values_from_location("outdoors")
    tmp_in, tmp_out, dwh_tmp, dwh_coil_tmp = queries.get_boiler_values()
    
    my_context = {
        "avg_tmp_indoors": avg_tmp_indoors, "avg_pres_indoors": avg_pres_indoors, "avg_hum_indoors": avg_hum_indoors,
        "avg_tmp_out": avg_tmp_out, "avg_pres_out" : avg_pres_out, "avg_hum_out": avg_hum_out,
        "tmp_in": tmp_in, "tmp_out": tmp_out, "dwh_tmp": dwh_tmp, "dwh_coil_tmp": dwh_coil_tmp
    }

    return render(request, "home.html", my_context)