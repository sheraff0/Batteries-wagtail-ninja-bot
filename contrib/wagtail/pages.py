from django.urls import reverse

from contrib.utils.objects import update_instance


def get_or_create_page(Model, title=None, parent=None, **kwargs):
    if _page := Model.objects.filter(title=title, path__startswith=parent.path).first():
        update_instance(_page, kwargs)
        _page.save()
    else:
        _page = Model(title=title)
        update_instance(_page, kwargs)
        parent.add_child(instance=_page)
    return _page


def get_page_edit_url(id, path='pages/{id}/edit/'): 
    return reverse("wagtailadmin_home") + path.format(id=id)
