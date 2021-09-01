
import threading

class RedisWatcherExtended(object):
    """Class that is used by casbin for tracking updates using redis subscriber.
    Update message is called by PyCasbin and Casbin rules are updated on all instances of application."""

    stop_reader_thread = False
    redis_pubsub_connection = None
    logger = None

    def __init__(
        self, logger: logger, redis_host: str = "redis", redis_port: int = 6379
    ):
        self.redis_url = redis_host
        self.redis_port = redis_port
        self.logger = logger
        self.reader_thread = threading.Thread(target=self.redis_connector_loop)
        self.reader_thread.start()

    def stop_watcher(self):
        """Stopping thread loop and closing redis connection"""
        self.stop_reader_thread = True
        self.reader_thread.join()

    def redis_connector_loop(self):
        """Main loop for redis subscription"""
        initial_delay = 0
        while not self.stop_reader_thread:
            self.redis_update_watch(delay=initial_delay)
            initial_delay = 10

    def set_update_callback(self, fn):
        """Setting callback method for enforcer model loading"""
        self.update_callback = fn

    def update_callback(self):
        self.logger.critical("Update callback is not overwritten.")

