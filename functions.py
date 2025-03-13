import requests

from test_data import *


class APIRequests:
    direction = 'IMPORT'
    payload_type = 'COMMODITY'
    callback_uri = 'https://someuri/'

    def __init__(self):
        self.bearer_token = self.create_bearer_token()
        self.headers = {
            "Authorization": "Bearer " + self.bearer_token,
            "Content-Type": "application/json"
        }
        self.connect_token = self.create_a_connect_token()

    def create_bearer_token(self):
        response_bearer = requests.request("GET", Login_Url, headers=auth_header)
        response_bearer.raise_for_status()
        bearer_token = response_bearer.json().get('bearer_token')

        return bearer_token

    def create_a_connect_token(self):
        payload = {
            "direction": self.direction,
            "type": self.payload_type,
            "callback_uri": self.callback_uri,
            "postal_address": {
                "country_code": "GB"
            }
        }
        response_connect_token = requests.request("POST", Connect_token_Url, json=payload, headers=self.headers)
        response_connect_token.raise_for_status()
        connect_token = response_connect_token.json().get('connect_token')
        return connect_token

    def session_start(self):
        headers = {
            "Content-Type": "application/json"
        }
        payload = {
            "connect_token": self.connect_token,
            "route": "session_restore"
        }
        response_session_start = requests.request("POST", url=Connect_Url, json=payload, headers=headers)
        response_session_start.raise_for_status()

    def provide_uk_address(self):
        ct_data = {
            "connect_token": self.connect_token,
            "route": "postal_address_capture",
            "data": {
                "postal_address": {
                    "address_line1": "1-3",
                    "address_line2": "Strand",
                    "city": "London",
                    "state": "Greater London",
                    "post_code": "WC2N 5EH",
                    "country_code": "GB"
                }
            }
        }
        response_address = requests.request("POST", Connect_Url, json=ct_data, headers=self.headers)
        response_address.raise_for_status()
        Providers_list = response_address.json().get('data').get("providers")
        for provider in Providers_list:
            if provider['display_name'] == 'Ecotricity':
                ecotricity_id = provider['id']
                break
        return ecotricity_id

    def provider_select(self, ecotricity_id):
        p_data = {
            "connect_token": self.connect_token,
            "route": "provider_select",
            "data": {
                "provider": {
                    "id": ecotricity_id
                }
            }
        }
        response_provider = requests.request("POST", Connect_Url, json=p_data, headers=self.headers)
        response_provider.raise_for_status()

    def tariff_structure_select(self):
        ts_data = {
            "connect_token": self.connect_token,
            "route": "tariff_structure_select",
            "data": {
                "options": [
                    "MARKET"
                ]
            }
        }
        response_tariff_select = requests.request("POST", Connect_Url, json=ts_data, headers=self.headers)
        response_tariff_select.raise_for_status()

    def market_surcharge_capture(self):
        msc_data = {
            "connect_token": self.connect_token,
            "route": "market_surcharge_capture",
            "data": {
                "surcharge": {
                    "fixed": 0.5,
                    "percentage": 18.50
                },
                "region": "GB"
            }
        }
        response_tariff_surcharge = requests.request("POST", Connect_Url, json=msc_data, headers=self.headers)
        response_tariff_surcharge.raise_for_status()

    def tariff_name_capture(self):
        tnc_data = {
            "connect_token": self.connect_token,
            "route": "tariff_name_capture",
            "data": {
                "tariff": {
                    "name": "Test Tariff_OM"
                }
            }
        }
        response_tariff_name = requests.request("POST", Connect_Url, json=tnc_data, headers=self.headers)
        response_tariff_name.raise_for_status()

    def contract_term_capture(self):
        cd_data = {
            "connect_token": self.connect_token,
            "route": "contract_term_capture",
            "data": {
                "contract_end_date": (datetime.now() + timedelta(days=30)).replace(hour=0, minute=0, second=0,
                                                                                   microsecond=0).strftime(
                    "%Y-%m-%dT%H:%M:%SZ")
            }
        }
        response_contract_data = requests.request("POST", Connect_Url, json=cd_data, headers=self.headers)
        response_contract_data.raise_for_status()

    def save_contract(self):
        c_data = {
            "connect_token": self.connect_token,
            "route": "summary_tou_confirm",
            "action": "SAVE"
        }
        response_contract_save = requests.request("POST", Connect_Url, json=c_data, headers=self.headers)
        response_contract_save.raise_for_status()

    def exchange_the_connect_token(self):
        querystring = {"connect_token": self.connect_token}
        response_ec = requests.request("GET", Connect_token_Url, headers=self.headers, params=querystring)
        response_ec.raise_for_status()
        location_id = response_ec.json().get('location_id')
        return location_id

    def fetch_tariff_rates(self, location_id):
        response_tariff_rates = requests.request("GET", url=f"https://api.flatpeak.com/tariffs/rates/{location_id}",
                                                 headers=self.headers,
                                                 params={"direction": "IMPORT",
                                                         "end_time": end_time,
                                                         "start_time": current_time})
        # with open("response_rates.json", "w") as f:
        #     f.write(response_tariff_rates.text)
        return response_tariff_rates.json()
