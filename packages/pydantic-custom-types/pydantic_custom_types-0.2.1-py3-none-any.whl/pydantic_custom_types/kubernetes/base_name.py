from string import ascii_lowercase


class BaseName(str):
    """
    Base validation of kubernetes/host names. All other types may inherit for this one
    to get base validation.
    The following is required:
    - type string
    - not empty string
    - only a-z, 0-9, and dash
    - cannot start with number
    - cannot start/end with dash
    """
    NUMBERS = "0123456789"
    LEGAL_CHARS = ascii_lowercase + "-" + NUMBERS

    @classmethod
    def __get_validators__(cls):
        yield cls.base_name_validate

    @classmethod
    def base_name_validate(cls, name: str):
        cls.is_string(name)
        cls.is_empty_string(name)
        cls.has_upper_case(name)
        cls.starts_with_number(name)
        cls.starts_end_with_dash(name)

        return name

    @staticmethod
    def is_string(name):
        if not isinstance(name, str):
            raise TypeError('string required')
        return name

    @staticmethod
    def is_empty_string(name):
        if name == "":
            raise ValueError("String cannot be empty")
        return name

    @classmethod
    def has_upper_case(cls, name: str):
        if not all(char in cls.LEGAL_CHARS for char in name):
            raise ValueError(f'Value maybe only container lowe case ascii characters, and dash: "{name}"')
        return name

    @classmethod
    def starts_with_number(cls, name):
        if name[0] in cls.NUMBERS:
            raise ValueError(f'Value cannot start with a number: "{name}"')
        return name

    @staticmethod
    def starts_end_with_dash(name):
        if name.startswith("-") or name.endswith("-"):
            raise ValueError(f'Value cannot start/end with a dash: "{name}"')
        return name
