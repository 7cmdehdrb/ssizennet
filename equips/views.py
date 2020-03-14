from django.shortcuts import render
from django.core.paginator import Paginator
from django.views.generic import ListView, DetailView
from . import models

# Create your views here.


class EquipView(ListView):
    def get(self, request):
        qs = models.Equip.objects.all()
        paginator = Paginator(qs, 4)
        page = request.GET.get("page", 1)
        equips = paginator.get_page(page)
        get_copy = request.GET.copy()
        address = get_copy.pop("page", True) and get_copy.urlencode()
        return render(
            request, "equips/list.html", {"equips": equips, "address": address}
        )


class EquipDetail(DetailView):

    model = models.Equip
    context_object_name = "equip_obj"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context
