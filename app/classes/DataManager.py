import jsonwebtoken as jwt
import json
import httpx
from time import time, sleep
from hashlib import sha256
from base64 import b64encode
from rich import box
from rich.table import Table
from rich.console import Console
from rich.progress import track, Progress
from os import path

from ..functions.File import write_pdf, write_excel

console = Console()


class Data():
    def __init__(self, parameter: object):
        file_path = ('config.json' if path.isfile('config.json')
                     else 'default_config.json')
        config = open(file_path)
        data = json.load(config)
        self.__base_url = data['base_url']
        self.__app_id = data['application_id']
        self.__api_key = data['api_key']
        self.__product_agent_api_path = data['product_agent_api_path']
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

    def fetch_data(self):
        jwt_token = self.__create_jwt_token()
        headers = {"Authorization": f"Bearer {jwt_token}"}
        client = httpx.Client(headers=headers, verify=False)
        res = client.get(self.url)
        content = res.json()['result_content']
        return content

    def get_all_data(self):
        res = self.fetch_data()
        if isinstance(res, list):
            table = Table(title="All Data", show_header=True,
                          header_style="bold white", box=box.ROUNDED)
            table_heading = [
                {
                    'header': "ID",
                    'max_width': 2,
                    'style': '#878787',
                },
                {
                    'header': 'Entity ID',
                    'max_width': 50,
                },
                {
                    'header': 'Host',
                    'max_width': 20
                },
                {
                    'header': 'IP Address',
                    'max_width': 20,
                    'style': '#3d8eff'
                },
                {
                    'header': 'Registration Time',
                    'max_width': 20
                },
                {
                    'header': 'Status',
                    'max_width': 12
                }
            ]
            for heading in table_heading:
                table.add_column(**heading)

            index = 0
            data_table = [
                ["ID", "Entity ID", "Host", "IP Address", "Registration Time", "Status"]
            ]

            data_excel = {
                "ID": [],
                "Entity ID": [],
                "Host": [],
                "IP Address": [],
                "Registration Time": [],
                "Status": []
            }

            for data in res:
                index += 1
                id = str(index)
                entity_id = data['entity_id']
                host = data['host_name']
                ip = data['ip_address_list']
                registration_time = data['last_registration_time']
                status = ('[green]ONLINE[/green]' if data['connection_status']
                          == 'Online' else '[red]OFFLINE[/red]')
                data_table.append([id, 
                                   entity_id,
                                   host, ip,
                                   registration_time,
                                   data['connection_status'].upper()])
                data_excel["ID"].append(id)
                data_excel["Entity ID"].append(entity_id)
                data_excel["Host"].append(host)
                data_excel["IP Address"].append(ip)
                data_excel['Registration Time'].append(registration_time)
                data_excel["Status"].append(data['connection_status'].upper())
                table.add_row(id, entity_id, host, ip,
                              registration_time, status)

            hosts = []
            for data in res:
                hosts.append(data['host_name'])

            with Progress(console=console, transient=True) as progress:
                tasks = []
                for host in hosts:
                    task = progress.add_task(
                        f"[red]Fetching {host}...", total=100)
                    tasks.append(task)

                while not progress.finished:
                    for task in tasks:
                        progress.update(task, advance=0.5)
                    sleep(0.02)

            console.print(table)

            write_pdf(data_table)
            write_excel(data_excel)
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
                table = Table(
                    title=data_found['host_name'], header_style="bold white",
                    box=box.ROUNDED)
                table.add_column("Type", max_width=30)
                table.add_column("Value", max_width=50)
                for i in track(range(100),
                               description=f"[red]Fetching {host}"):
                    sleep(0.02)

                for key, value in data_found.items():
                    if key == 'ip_address_list':
                        table.add_row('IP Address', value)
                    elif key == 'connection_status':
                        table.add_row('Connection Status', value)
                    elif key == 'entity_id':
                        table.add_row('Entity ID', value)
                    elif key == 'last_registration_time':
                        table.add_row('Last Registration Time', value)

                console.print(table)
            else:
                print("""     ____        _          _   _       _     _____                     _ 
    |  _ \  __ _| |_ __ _  | \ | | ___ | |_  |  ___|__  _   _ _ __   __| |
    | | | |/ _` | __/ _` | |  \| |/ _ \| __| | |_ / _ \| | | | '_ \ / _` |
    | |_| | (_| | || (_| | | |\  | (_) | |_  |  _| (_) | |_| | | | | (_| |
    |____/ \__,_|\__\__,_| |_| \_|\___/ \__| |_|  \___/ \__,_|_| |_|\__,_|""")
