from enum import StrEnum, auto
import calendar

from datetime import date, datetime


WEEKDAYS = ("Пн", "Вт", "Ср", "Чт", "Пт", "Сб", "Вс")
MONTHS = ("Январь", "Февраль", "Март", "Апрель", "Май", "Июнь",
    "Июль", "Август", "Сентябрь", "Октябрь", "Ноябрь", "Декабрь")


class Calendar:
    def __init__(self, journal_map=None):
        self._journal_map = journal_map
        self._now = datetime.now()
        self._year = self._now.year
        self._month = self._now.month
        self._calendar = calendar.Calendar()

    def get_month(self, ym):
        _month = []
        for week in self._calendar.monthdays2calendar(*ym):
            _week = []
            for day, weekday in week:
                _date = date(*ym, day) if day > 0 else None
                _journal_page = self._journal_map and self._journal_map.get(_date)
                _week.append((_journal_page, str(_date), day, weekday))
            _month.append(_week)
        return [day for week in _month for day in week]

    @property
    def previous_ym(self):
        return (self._year, self._month - 1) if self._month > 1 else (
            self._year - 1, 12)

    @property
    def current_ym(self):
        return self._year, self._month

    @property
    def next_ym(self):
        return (self._year, self._month + 1) if self._month < 12 else (
            self._year + 1, 1)

    @property
    def three_months(self):
        _months = self.previous_ym, self.current_ym, self.next_ym
        _title = [f"{MONTHS[m-1]} {y}" for y, m in _months]
        _days = [*map(self.get_month, _months)]
        return zip(_title, _days)
