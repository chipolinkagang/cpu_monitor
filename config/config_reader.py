import json


def get_config() -> dict:
    try:
        with open('config/config.json') as json_file:
            data = json.load(json_file)
            return data
    except Exception as e:
        return {"Error": "Cant read config." + str(e)}