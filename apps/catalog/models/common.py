from django.db import models

from apps.root.models.common import PREMIUM_GTE

DELTA_SIMILAR = 0.1


class Polarity(models.IntegerChoices):
    STRAIGHT = (1, "Прямая")
    REVERSE = (2, "Обратная")


class PriceSegment(models.IntegerChoices):
    ECONOM = (1, "Эконом")
    ECONOM_PLUS = (2, "Эконом+")
    STANDARD = (3, "Стандарт")
    STANDARD_PLUS = (4, "Стандарт+")
    PREMIUM = (5, "Премиум")
    PREMIUM_PLUS = (6, "Премиум+")


class Terminal(models.IntegerChoices):
    STANDARD = (1, "Стандартные")
    THIN = (2, "Тонкие")
    UNIVERSAL = (3, "Универсальные")


class CaseFormat(models.IntegerChoices):
    EUROPE = (1, "Европа")
    ASIA = (2, "Азия")
    AMERICA = (3, "Америка")
    TRUCK = (4, "Грузовые")


class Sections(models.IntegerChoices):
    BATTERY = (1, "Аккумулятор автомобильный")
    ACCESSORY = (2, "Аксессуар")
    SERVICE = (3, "Услуга")
    MOTO_BATTERY = (4, "Аккумулятор для мотоцикла")


class StandardSize(models.TextChoices):
    # Европа
    L1 = ("L1", "L1")
    LB1 = ("LB1", "LB1")
    L2 = ("L2", "L2")
    LB2 = ("LB2", "LB2")
    L3 = ("L3", "L3")
    LB3 = ("LB3", "LB3")
    L4 = ("L4", "L4")
    LB4 = ("LB4", "LB4")
    L5 = ("L5", "L5")
    LB5 = ("LB5", "LB5")
    L6 = ("L6", "L6")
    # Азия
    B19 = ("B19", "B19")
    B24 = ("B24", "B24")
    D23 = ("D23", "D23")
    D26 = ("D26", "D26")
    D31 = ("D31", "D31")
    # Грузовые
    A = ("A", "A")
    B = ("B", "B")
    C = ("C", "C")
    D5 = ("D5", "D5")


SS = StandardSize
STANDARD_DIMENSIONS = {
    SS.L1: (207, 175, 190),
    SS.LB1: (207, 175, 175),
    SS.L2: (242, 175, 190),
    SS.LB2: (242, 175, 175),
    SS.L3: (276, 175, 190),
    SS.LB3: (276, 175, 175),
    SS.L4: (315, 175, 190),
    SS.LB4: (315, 175, 175),
    SS.L5: (353, 175, 190),
    SS.LB5: (353, 175, 175),
    SS.B19: (195, 129, 222),
    SS.B24: (237, 128, 222),
    SS.D23: (230, 173, 220),
    SS.D26: (260, 173, 220),
    SS.D31: (306, 173, 220),
    SS.A: (513, 189, 236),
    SS.B: (518, 228, 238),
    SS.C: (518, 274, 230),
    SS.D5: (513, 223, 223),
}
