from .common import SimpleModel


class Country(SimpleModel):
    class Meta:
        ordering = ["name"]
        verbose_name = "Страна"
        verbose_name_plural = "Страны"
