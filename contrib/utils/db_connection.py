from django.db import connection


def raw_sql(sql, fetch: bool = True):
    with connection.cursor() as cursor:
        cursor.execute(sql)
        if fetch:
            keys = [x.name for x in cursor.description]
            data = cursor.fetchall()
            return [dict(zip(keys, x)) for x in data]
