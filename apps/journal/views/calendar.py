from django.contrib.admin.utils import quote
from django.shortcuts import render
from django.utils import timezone

from contrib.utils.calendar import WEEKDAYS, MONTHS, Calendar
from contrib.wagtail.pages import get_page_edit_url
from ..models import Day


def index(request):
    _journal_map = {x["date"]: get_page_edit_url(x["id"])
        for x in Day.objects.values("id", "date")}
    _calendar = Calendar(_journal_map)
    return render(request, "journal/calendar.html", {
        "WEEKDAYS": WEEKDAYS,
        "calendar": _calendar
    })
