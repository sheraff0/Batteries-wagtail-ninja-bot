from django.db import connection


def raw_sql(sql, fetch: bool = True):
    with connection.cursor() as cursor:
        cursor.execute(sql)
        _keys = [x[0] for x in cursor.description]
        if fetch:
            return [
                dict(zip(_keys, x))
                for x in cursor.fetchall()
            ]
