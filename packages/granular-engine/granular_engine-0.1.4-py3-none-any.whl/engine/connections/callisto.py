import os 
import json 
import requests 
import click
import keyring
from appdirs import user_config_dir 


__all__ = ['Callisto']

class Callisto:
    def __init__(self, email=None, password=None,
                host=None):
        self.host = host
        self.email = email 
        self.password = password
        self.headers = {
            'accept': 'application/json',
            'Content-Type': 'application/json'
        }
        self.setup()

    def read_config(self):
        try:
            config_path = os.path.join(user_config_dir('engine'), "config.json")
            fin = open(config_path, 'r')
            config_data = json.load(fin)
            fin.close()

            if not self.host:
                self.host = config_data['host']
            if not self.email:
                self.email = config_data['email']
            if not self.password:
                # self.password = config_data['password']
                self.password = keyring.get_password("engine", self.email)
            self.headers['Cookie'] = keyring.get_password("engine-cookie", self.email)
        except:
            pass

    def update_config(self):
        config_path = os.path.join(user_config_dir('engine'), "config.json")
        fout = open(config_path, 'w')
        json.dump({'host': self.host,
                    'email': self.email, 
                    # 'password': self.password, 
                    # 'cookie': self.headers['Cookie']
                    }, fout)
        fout.close()
        keyring.set_password("engine", self.email, self.password)
        keyring.set_password("engine-cookie", self.email, self.headers['Cookie'])
    
    def is_token_valid(self):
        response = requests.get(f'{self.host}/callisto/api/v1/users/me', headers=self.headers)
        if response.status_code == 200:
            return True 
        return False

    def login(self):
        login_url = f'{self.host}/callisto/auth/v1/login'
        data = {"email": self.email, "password": self.password}
        if 'Cookie' in self.headers:
            del self.headers['Cookie']

        response = requests.post(login_url, headers=self.headers, data=json.dumps(data))
        if response.status_code == 200:
            resdata = response.json()
            self.user_id = resdata["user"]["id"]
            auth_cookie = response.cookies["callisto_auth"]
            self.headers["Cookie"] = f"callisto_auth={auth_cookie}"
            self.update_config()
            print(f"{self.email} successfully logged on {self.host}")
        else:
            print('failed to authenticate')
            print(f"authentication endpoint {self.host} returned with HTTP status code : {response.status_code}")
            print(f"please register at {f'{self.host}/register'} if you havent")

    def setup(self):
        self.read_config()
        if not self.email or not self.password:
            click.echo("Please login using email and password")
            exit()
        elif not self.is_token_valid():
            self.login()

    def get_org_id_from_slug(self, org_slug):
        url = f"{self.host}/callisto/api/v1/organizations/{org_slug}"
        response = requests.get(url, headers=self.headers)
        if response.status_code == 200:
            resdata = response.json()
            return resdata['id']
        else:
            click.echo('Organization slug {org_slug} not found')
            return None
            