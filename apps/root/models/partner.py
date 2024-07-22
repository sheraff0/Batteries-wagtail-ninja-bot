from .common import SimpleModel


class Partner(SimpleModel):
    class Meta:
        ordering = ["name"]
        verbose_name = "Партнёр"
        verbose_name_plural = "Партнёры"
