import socket


class Ipv4Address(str):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, name: str) -> str:
        socket.inet_aton(name)
        return name
