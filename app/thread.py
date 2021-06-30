import threading
from collections import defaultdict

_data_by_thread_name = defaultdict(dict)


def _data():
    return _data_by_thread_name[threading.current_thread().name]


def get_cached_primary_lsn():
    return _data()['cached_primary_lsn']


def set_cached_primary_lsn(lsn):
    _data()['cached_primary_lsn'] = lsn


def did_write_happen():
    return _data().get('write_happened', False)


def set_write_happened():
    _data()['write_happened'] = True


def cleanup():
    del _data_by_thread_name[threading.current_thread().name]
