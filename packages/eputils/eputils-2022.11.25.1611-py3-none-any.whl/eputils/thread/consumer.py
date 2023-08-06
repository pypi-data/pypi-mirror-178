from logging import Logger
from typing import Callable, Tuple
from pika.channel import Channel
from pika.spec import Basic, BasicProperties
from .settings import ConnectionSettings
from .abstract import AbstractThread
import pika
import threading

class ConsumerThread(AbstractThread):
    def __init__(self, 
                 host: str, 
                 queue_name: str, 
                 creds_provider: Callable[[], Tuple[str, str]], 
                 on_receive: Callable[[str], None], 
                 app_id: str,
                 logger: Logger, 
                 settings: ConnectionSettings = ConnectionSettings.default()):
        super().__init__(host, creds_provider, logger, app_id, settings)

        self._on_receive = on_receive
        self._queue_name = queue_name
        self._stop_event = threading.Event()

    def _check_stop(self):
        if self._stop_event.is_set():
            return self._stop()
        
        self._call_later(self._check_stop, self._settings.loop_interval)

    def _stop(self):
        self._print("Stopping consumer thread..")
        self._closing = True
        self._channel.stop_consuming()
        self._connection.close()
        self._connection.ioloop.close()
        self._print("Stopped")
    
    def stop_flag(self):
        self._closing = True
        self._stop_event.set()
        self._print("Requested thread stopping..")

    def connect(self):
        creds_user, creds_pass = self._creds_provider()
        credentials = pika.PlainCredentials(creds_user, creds_pass)

        self._connection = pika.SelectConnection(
            pika.ConnectionParameters(host=self._host,
                                      credentials=credentials),
            on_open_callback=self.on_connection_open,
            on_open_error_callback=self.on_connection_open_error,
            on_close_callback=self.on_connection_close
        )

        self._call_later(self._check_stop, self._settings.loop_interval)
    
    def on_connection_open(self, connection):
        self._print("Connection OPENED")
        self._print("Making channel..")
        self._connection.channel(
            on_open_callback=self.on_channel_open)
    
    def on_connection_close(self, connection, error):
        self._print(f"Connection CLOSED, error: {error}. Retrying..")
        self._call_later(self._retry_connection, 0.5) # retry immediately
    
    def on_connection_open_error(self, connection, error):
        self._print(f"Connection ERROR WHILE OPENING. Retrying in {self._settings.retry_connection_interval}..")
        self._call_later(self._retry_connection, self._settings.retry_connection_interval)

    def on_channel_open(self, channel: Channel):
        self._channel = channel
        self._channel.add_on_close_callback(self.on_channel_close)
        self._print("Channel opened")

        channel.queue_declare(self._queue_name, durable=True)
        channel.basic_consume(self._queue_name,
                              self.on_message)

    def on_channel_close(self, channel, reason: Exception):
        self._print(f"Channel closed with reason: {reason}")
    
    def on_message(self, channel: Channel, method: Basic.Deliver, props: BasicProperties, body: bytes):
        channel.basic_ack(method.delivery_tag)
        self._on_receive(body)
    
    def __enter__(self):
        return super().__enter__()
    
    def __exit__(self, type, value, tb):
        return super().__exit__(type, value, tb)