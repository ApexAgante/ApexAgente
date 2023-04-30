from json import dumps
from ..classes.DataManager import Data

data = None


def write_config(api, app, url):
    config = {
        "base_url": url,
        "application_id": app,
        "api_key": api,
        "product_agent_api_path": "/WebApp/API/AgentResource/ProductAgents"
    }
    with open('config.json', 'w') as file:
        data_json = dumps(config, indent=2)
        file.write(data_json)


def create_data():
    global data
    if data is None:
        data = Data({
            'headers': '',
            'query': '?hostname',
            'body': '',
            'http_method': 'GET'
        })


def get_data():
    global data
    return data
