from decouple import config, UndefinedValueError
import json


def load_local_file(env_var):
    try:
        usr = config(env_var)
    except UndefinedValueError as e:
        raise UndefinedValueError(f"Env var not set '{env_var}'\npath to json file of list[str] must be specified to use class\n{e}")

    with open(usr, "r") as uf:
        return json.load(uf)
