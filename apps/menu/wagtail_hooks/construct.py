from wagtail import hooks

HIDDEN_MENU_ITEMS = [
    "images",
    "documents",
    "reports",
    #"settings",
    "help",
]

ORDERING = {
    "Журнал": 1001,
    "Списки": 1002,
    "Операции": 1003,
    "Отчёты": 1004,
}


@hooks.register("construct_main_menu")
def construct(request, menu_items):
    menu_items[:] = [x for x in menu_items if x.name not in HIDDEN_MENU_ITEMS]
    for item in menu_items:
        if _order := ORDERING.get(item.label):
            item.order = _order
