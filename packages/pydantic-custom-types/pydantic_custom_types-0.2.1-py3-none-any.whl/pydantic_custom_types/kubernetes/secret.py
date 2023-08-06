from pydantic_custom_types.kubernetes.base_name import BaseName


class SecretName(BaseName):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate_secret_name

    @classmethod
    def validate_secret_name(cls, name: str) -> str:
        cls.base_name_validate(name)
        cls.has_to_many_characters(name)
        return name

    @classmethod
    def has_to_many_characters(cls, name: str):
        max_length = 254
        if len(name) >= max_length:
            raise ValueError(f"Name cannot be longer than {max_length} characters")
        return name
