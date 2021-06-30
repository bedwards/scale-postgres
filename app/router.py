import logging
import threading
from . import database
from . import thread

logger = logging.getLogger(__name__)


class Router:
    def db_for_read(self, model, **hints):
        extra = ''
        if thread.did_write_happen():
            # if a write already occurred in this request, always use primary
            db = 'default'

        else:
            current_wal_lsn = thread.get_cached_primary_lsn()

            if current_wal_lsn is None:
                db = 'replica'

            else:
                last_wal_receive_lsn = database.get_last_wal_receive_lsn()

                extra = 'primary %s, replica %s' % (
                            current_wal_lsn, last_wal_receive_lsn)

                db = ('replica'
                      if (current_wal_lsn[0] < last_wal_receive_lsn[0] or
                          current_wal_lsn[1] <= last_wal_receive_lsn[1])
                      else 'default')

        logger.error('db_for_read %s, %s, %s',
                     db, threading.current_thread().name, extra)
        return db

    def db_for_write(self, model, **hints):
        thread.set_write_happened()
        return 'default'
