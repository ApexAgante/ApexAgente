import jsonwebtoken as jwt
import json
import httpx
from time import time
from hashlib import sha256
from base64 import b64encode
from prettytable import PrettyTable
from typing import List


class Data():
    def __init__(self, parameter: object):
        config = open('config.json')
        data = json.load(config)
        self.__base_url = data['base_url']
        self.__app_id = data['application_id']
        self.__api_key = data['api_key']
        self.__product_agent_api_path = data['product_agent_api_path']
        self.headers = parameter['headers'] if 'headers' in parameter else ''
        self.query = parameter['query'] if 'query' in parameter else ''
        self.body = parameter['body'] if 'body' in parameter else ''
        self.http_method = parameter['http_method'] if 'http_method' in parameter else ''

    @property
    def raw_url(self):
        return self.__product_agent_api_path + self.query

    @property
    def url(self):
        return self.__base_url + self.raw_url

    def __create_checksum(self):
        string_to_hash = f"{self.http_method.upper()}|{self.raw_url.lower()}|{self.headers}|{self.body}"
        hash_object = sha256(str.encode(string_to_hash))
        base64_string = b64encode(hash_object.digest()).decode('utf-8')
        return base64_string

    def __create_jwt_token(self, iat=time(), algorithm='HS256', version='V1'):
        checksum = self.__create_checksum()
        payload = {
            "appid": self.__app_id,
            "iat": iat,
            "version": version,
            "checksum": checksum
        }
        token = jwt.encode(payload, self.__api_key, algorithm=algorithm)
        return token

    def fetch_data(self) -> List:
        jwt_token = self.__create_jwt_token()
        headers = {"Authorization": f"Bearer {jwt_token}"}
        client = httpx.Client(headers=headers, verify=False)
        res = client.get(self.url)
        content = res.json()['result_content']
        return content

    def get_all_data(self):
        res = self.fetch_data()
        if isinstance(res, list):
            table = PrettyTable(
                ['Index', 'Entity ID', 'Host Name', 'IP Address',
                 'Registration Time', 'Status'])
            index = 0
            for data in res:
                index += 1
                entity_id = data['entity_id']
                host = data['host_name']
                ip = data['ip_address_list']
                registration_time = data['last_registration_time']
                status = data['connection_status']
                table.add_row([index, entity_id,
                               host, ip, registration_time, status.upper()])
            tbl = table.get_string(title="All Data")
            print(tbl)
        else:
            print("""     ____        _          _   _       _     _____                     _ 
    |  _ \  __ _| |_ __ _  | \ | | ___ | |_  |  ___|__  _   _ _ __   __| |
    | | | |/ _` | __/ _` | |  \| |/ _ \| __| | |_ / _ \| | | | '_ \ / _` |
    | |_| | (_| | || (_| | | |\  | (_) | |_  |  _| (_) | |_| | | | | (_| |
    |____/ \__,_|\__\__,_| |_| \_|\___/ \__| |_|  \___/ \__,_|_| |_|\__,_|""")

    def get_all_host(self):
        res = self.fetch_data()
        if res and isinstance(res, list):
            hosts = []
            for data in res:
                hosts.append(data['host_name'])

            return hosts

    def get_data_by_host(self, host: str):
        res = self.fetch_data()
        if res and isinstance(res, list):
            data_found = next(
                (data for data in res if
                    data['host_name'].casefold() == host.casefold()), None
            )

            if data_found is not None:
                table = PrettyTable(["Type", "Result"])
                for key, value in data_found.items():
                    if key == 'ip_address_list':
                        table.add_row(['IP Address', value])
                    elif key == 'connection_status':
                        table.add_row(['Connection Status', value])
                    elif key == 'entity_id':
                        table.add_row(['Entity ID', value])
                    elif key == 'last_registration_time':
                        table.add_row(['Last Registration Time', value])

                tbl = table.get_string(title=data_found['host_name'])
                print(tbl)
            else:
                print("""     ____        _          _   _       _     _____                     _ 
    |  _ \  __ _| |_ __ _  | \ | | ___ | |_  |  ___|__  _   _ _ __   __| |
    | | | |/ _` | __/ _` | |  \| |/ _ \| __| | |_ / _ \| | | | '_ \ / _` |
    | |_| | (_| | || (_| | | |\  | (_) | |_  |  _| (_) | |_| | | | | (_| |
    |____/ \__,_|\__\__,_| |_| \_|\___/ \__| |_|  \___/ \__,_|_| |_|\__,_|""")
