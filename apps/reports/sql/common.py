import abc
from dataclasses import dataclass

from django.http.request import HttpRequest

from contrib.django.db_connection import raw_sql


@dataclass
class ReportSqlBase:
    request: HttpRequest
    date_field: str = "jd.date"

    def __post_init__(self):
        self.start, self.end = map(self.request.GET.get, ("start" ,"end"))
        self.before_start = f"""{self.date_field} < '{self.start or "1900-01-01"}'"""
        self.before_end = f"""{self.date_field} <= '{self.end or "2100-01-01"}'"""

    @abc.abstractproperty
    def sql_statement(self):
        ...

    def execute(self):
        return raw_sql(self.sql_statement)
