from django.template.defaultfilters import date as date_filter
from django.utils.timezone import localdate

from contrib.django.styling import color_text, style_text


class DebtUrgencyMixin:
    @property
    def debt_urgency(self):
        try:
            assert self.total_debt > 0
            return int(100 - max(0, min(100, (
                self.payment_date - localdate()
            ).days / 14 * 100)))
        except:
            return 0

    @property
    def debt_urgency_color(self):
        H = 40 - self.debt_urgency * 40 / 100
        S = self.debt_urgency
        L = 50
        return f"hsl({H}, {S}%, {L}%)"

    def _payment_soon(self):
        try:
            _value = date_filter(self.payment_date, "d E Y")
            if (self.total_debt or 0) <= 0:
                return color_text(
                    style_text(_value, "text-decoration", "line-through"), "#aaa")
            return color_text(_value, self.debt_urgency_color)
        except: ...
    _payment_soon.short_description = "Срок оплаты"
    payment_soon = property(_payment_soon)

    def _debt(self):
        if (self.total_debt or 0) != 0:
            return color_text(self.total_debt, self.debt_urgency_color)
    _debt.short_description = "Мы должны"
    debt = property(_debt)
