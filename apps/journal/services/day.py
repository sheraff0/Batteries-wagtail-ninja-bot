from contrib.wagtail.pages import get_or_create_page
from ..models import Journal, Year, Month, Day


class NewDay:
    def __init__(self, date_: str):
        self._date = date_
        self.set_journal()
        self.set_date_parts()
        self.set_pages()

    def set_journal(self):
        self._journal = Journal.objects.live().first()

    def set_date_parts(self):
        self._year, self._month, self._day = str(self._date).split("-")

    def set_pages(self):
        self._year_page = get_or_create_page(Year, self._year, self._journal)
        self._month_page = get_or_create_page(Month, self._month, self._year_page)
        self._day_page = get_or_create_page(Day, self._day, self._month_page, date=self._date)

    @property
    def day_page(self):
        return self._day_page
