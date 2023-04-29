import json
from base64 import b64encode
from hashlib import sha256
from time import time
import jsonwebtoken as jwt
import httpx


class Data:
    def __init__(self, parameter: object):
        config = open('config.json')
        data = json.load(config)
        self.__base_url = data['base_url']
        self.__app_id = data['application_id'] or ''
        self.__api_key = data['api_key'] or ''
        self.__product_agent_api_path = data['product_agent_api_path'] or ''
        self.headers = parameter.get('headers', '')
        self.query = parameter.get('query', '')
        self.body = parameter.get('body', '')
        self.http_method = parameter.get('http_method', 'GET')

    @property
    def raw_url(self):
        return self.__product_agent_api_path + self.query

    @property
    def url(self):
        return self.__base_url + self.raw_url

    def __create_checksum(self, http_method: str):
        string_to_hash = f"{http_method.upper()}|{self.raw_url.lower()}|{self.headers}|{self.body}"
        hash_object = sha256(str.encode(string_to_hash))
        base64_string = b64encode(hash_object.digest()).decode('utf-8')
        return base64_string

    def __create_jwt_token(self, http_method: str,
                           iat=time(), algorithm='HS256', version='V1'):
        checksum = self.__create_checksum(http_method)
        payload = {
            'appid': self.__app_id,
            'iat': iat,
            'version': version,
            'checksum': checksum
        }
        token = jwt.encode(payload, self.__api_key, algorithm=algorithm)
        return token

    def fetch_data(self):
        jwt_token = self.__create_jwt_token(http_method=self.http_method)
        headers = {'Authorization': f"Bearer {jwt_token}"}
        client = httpx.Client(headers=headers, verify=False)
        res = client.get(self.url)
        content = res.json()['result_content']
        return content

    def fetch_data_from_host_name(self, host):
        data = self.fetch_data()
        if isinstance(data, list):
            matching_data = [
                d for d in data if d['host_name'].casefold() == host.casefold()]
            if matching_data:
                return matching_data[0]