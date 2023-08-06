from pydantic_custom_types.active_directory.util import load_local_file


class RealAdGroup(str):
    """
    This class requires env var "GROUPS_FILE".
    Value must be path to a json file containing a list of AD groups(str) to
    validate against
    """
    @staticmethod
    def groups() -> list[str]:
        return load_local_file("GROUPS_FILE")

    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def find_group_not_case_sensitive(cls, name: str):
        for g in cls.groups():
            if g.lower() == name.lower():
                return g


    @classmethod
    def validate(cls, name: str):
        if name in cls.groups():
            return name
        else:
            hint = cls.find_group_not_case_sensitive(name)
            if hint:
                raise ValueError(f'Group "{name}" does not exist, did you mean "{hint}"?')
            raise ValueError(f'Group "{name}" does not exist.')
