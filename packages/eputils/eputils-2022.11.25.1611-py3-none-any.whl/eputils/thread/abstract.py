from logging import Logger
from typing import Callable, Tuple
from pika.connection import Connection
from pika.channel import Channel
from .settings import ConnectionSettings
import threading
import sys

class AbstractThread(threading.Thread):
    def __init__(self, 
                 host: str, 
                 creds_provider: Callable[[], Tuple[str, str]], 
                 logger: Logger,
                 app_id: str,
                 settings: ConnectionSettings) -> None:
        super().__init__()
        self._host = host
        self._creds_provider = creds_provider
        self._connection: Connection = None
        self._channel: Channel = None
        self._connected_event = threading.Event()
        self._stop_event = threading.Event()    # Requests thread to stop
        self._stopped_event = threading.Event() # Fires when thread is actually stopped
        self._app_id = app_id
        self._ident = threading.get_ident()
        self._settings = settings
        self.__logger = logger

    def connect(self) -> None:
        """Connect to the host"""
        raise NotImplementedError
    
    def is_connected(self) -> bool:
        return self._channel is not None and self._channel.is_open

    def run(self) -> None:
        """Run function for Thread"""
        self.connect()
        self._start_io_loop()
    
    def stop(self, blocking: bool = False) -> None:
        """Request thread stop"""
        self._print("Requested thread stopping..")
        self._stop_event.set()
        if blocking:
            self._stopped_event.wait()
    
    def _retry_connection(self) -> None:
        if self._stop_event.is_set():
            self._print("Stop event set, not retrying connection.")
            self._stopped()
            return

        self._print("Retrying to connect with message broker..")
        self.connect()
        self._start_io_loop()
    
    def _start_io_loop(self):
        self._print("Starting io loop..")
        self._connection.ioloop.start()

    def _stopped(self) -> None:
        self._stopped_event.set()
        self._kill_me()
    
    def _kill_me(self):
        raise Exception("Thread killed")

    def _close(self) -> None:
        self._print_warning(f"Closing thread!")
        self._connection.close()
    
    def _print(self, message: str):
        self.__print_func(message, self.__logger.info)

    def _print_warning(self, message: str):
        self.__print_func(message, self.__logger.warning)
    
    def _print_error(self, message: str):
        self.__print_func(message, self.__logger.error)

    def __print_func(self, message: str, func: Callable[[str], None]):
        func(f"{message} [thread {self._ident}-{self._app_id}]")
    
    def _call_later(self, func: Callable[[], None], after: float | int):
        self._connection.ioloop.call_later(
            after, 
            func)

    def __enter__(self):
        self.start()
        connected = self._connected_event.wait(8)
        if not connected:
            raise Exception("Could not connect to host..")
        return self
    
    def __exit__(self, type, value, tb):
        if tb is None:
            self.stop(blocking=True)
        else:
            self._print_error("Exception occured")
            self._print(str(tb))