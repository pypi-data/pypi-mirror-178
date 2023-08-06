from string import ascii_lowercase


class Hostname(str):
    NUMBERS = "0123456789"
    LEGAL_CHARS = ascii_lowercase + "-" + "_" + NUMBERS

    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, name: str) -> str:
        cls.has_valid_characters(name)
        cls.has_to_many_characters(name)
        cls.start_end_with_dot(name)

        return name

    @classmethod
    def has_valid_characters(cls, name: str):
        if not all(char in cls.LEGAL_CHARS for char in name):
            raise ValueError(f'Value "{name}" maybe only contain [-_0-9a-z]')
        return name

    @classmethod
    def has_to_many_characters(cls, name: str):
        max_length = 64
        if len(name) >= max_length:
            raise ValueError(f"Name must be less than {max_length} characters")
        return name

    @classmethod
    def start_end_with_dot(cls, name: str):
        if name.startswith(".") or name.endswith("."):
            raise ValueError("Name cannot start/end with a dot")
        return name

    @classmethod
    def start_end_with_dash(cls, name: str):
        if name.startswith("-") or name.endswith("-"):
            raise ValueError("Name cannot start/end with a dot")
        return name
