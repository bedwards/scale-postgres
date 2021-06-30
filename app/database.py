from django.db import connections


def _to_tuple(pg_lsn):
    # printed as two hexadecimal numbers of up to 8 digits each, separated by
    # a slash; for example, 16/B374D848
    return tuple([int(x, 16) for x in pg_lsn.split('/')]) + (pg_lsn,)


def get_current_wal_lsn():
    with connections['default'].cursor() as cursor:
        cursor.execute('select pg_current_wal_lsn()')
        current_wal_lsn = cursor.fetchone()[0]
    return _to_tuple(current_wal_lsn)


def get_last_wal_receive_lsn():
    with connections['replica'].cursor() as cursor:
        cursor.execute('select pg_last_wal_receive_lsn()')
        last_wal_receive_lsn = cursor.fetchone()[0]
    return _to_tuple(last_wal_receive_lsn)
