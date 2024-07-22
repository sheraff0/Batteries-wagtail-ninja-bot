from django.urls import path, reverse

from wagtail import hooks
from wagtail.admin.menu import Menu, MenuItem, SubmenuMenuItem

from apps.journal.views import index


@hooks.register("register_admin_urls")
def register_calendar_index():
    return [
        path("calendar/", index, name="calendar"),
    ]


@hooks.register("register_admin_menu_item")
def register_calendar_menu_item():
    return MenuItem("Журнал", reverse("calendar"), icon_name="date")


#@hooks.register("register_admin_menu_item")
def register_calendar_menu_item():
    submenu = Menu(items=[
        MenuItem("Текущий месяц", reverse("calendar-alt"), icon_name="date"),
    ])
    return SubmenuMenuItem("Журнал", submenu, icon_name="date")
