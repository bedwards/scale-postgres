import logging
import threading

logger = logging.getLogger(__name__)
data = threading.local()


class Router:
    def db_for_read(self, model, **hints):
        db = ('replica'
              if not getattr(data, 'write_happened', False)
              else 'default')
        logger.error('db_for_read %s, %r', db, threading.current_thread().name)
        return db

    def db_for_write(self, model, **hints):
        data.write_happened = True
        return 'default'
