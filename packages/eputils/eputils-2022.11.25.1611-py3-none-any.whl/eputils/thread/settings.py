from dataclasses import dataclass

@dataclass
class ConnectionSettings:
    loop_interval: float | int
    retry_connection_interval: float | int

    @staticmethod
    def default():
        return ConnectionSettings(1, 3)