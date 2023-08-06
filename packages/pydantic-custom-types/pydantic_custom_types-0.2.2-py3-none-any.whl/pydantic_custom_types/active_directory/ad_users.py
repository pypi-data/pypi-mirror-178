from pydantic_custom_types.active_directory.util import load_local_file


class RealAdUser(str):
    """
    This class requires env var "USERS_FILE".
    Value must be path to a json file containing a list of AD UPN names(str) to
    validate against
    """
    @staticmethod
    def users() -> list[str]:
        return [x.lower() for x in load_local_file("USERS_FILE")]

    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, name: str):
        for user in cls.users():
            if user.lower() == name.lower():
                return name
        else:
            raise ValueError(f'User "{name}" does not exist')

