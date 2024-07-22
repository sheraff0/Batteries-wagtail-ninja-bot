from django.templatetags.static import static
from django.utils.safestring import mark_safe

from wagtail import hooks


@hooks.register("insert_editor_js")
def editor_stimulus_totals_js():
    return mark_safe(
        f'<script src="{static("js/stimulus/totals.js")}"></script>'
    )
