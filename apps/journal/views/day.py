from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import redirect
from django.urls import reverse

from ..services import NewDay


@staff_member_required
def new_day(request):
    _date = request.GET.get("date")
    pk = NewDay(_date).day_page.pk
    return redirect(reverse("wagtailadmin_home") + f'pages/{pk}/edit/')
