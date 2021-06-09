from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json, os, datetime

class CoinMarketCapAPI:
    def __init__(self, api_key):

        self.api_key = api_key
        self.url = 'https://pro-api.coinmarketcap.com/v1/tools/price-conversion'
        self.parameters = {
            'symbol':'BCH',
            'amount':1,
        }
        self.headers = {
            'Accepts': 'application/json',
            'X-CMC_PRO_API_KEY': self.api_key,
        }

    def get_bch_price(self):
        '''
        returns the following:
        {
            "full_response": {
                "data": {
                    "amount": 1,
                    "id": 1831,
                    "last_updated": "2021-06-09T03:09:07.000Z",
                    "name": "Bitcoin Cash",
                    "quote": {
                        "USD": {
                            "last_updated": "2021-06-09T03:09:07.000Z",
                            "price": 570.8301798074937
                        }
                    },
                    "symbol": "BCH"
                },
                "status": {
                    "credit_count": 1,
                    "elapsed": 19,
                    "error_code": 0,
                    "error_message": null,
                    "notice": null,
                    "timestamp": "2021-06-09T03:09:34.028Z"
                }
            },
            "price": 570.8301798074937,
            "price_format": "570.83",
            "time": "2021-06-09T03:09:07.000Z"
            'time_dt': datetime.datetime(2021, 6, 9, 3, 8, 8),
        }
        '''
        api_response = {}

        session = Session()
        session.headers.update(self.headers)
        try:
            response = session.get(self.url, params=self.parameters)
            data = json.loads(response.text)
            api_response['price'] = data['data']['quote']['USD']['price']
            api_response['price_format'] = "{:.2f}".format(api_response['price'])
            api_response['time'] = data['data']['quote']['USD']['last_updated']
            api_response['time_dt'] = datetime.datetime.strptime(api_response['time'], "%Y-%m-%dT%H:%M:%S.000Z")
            api_response['full_response'] = data
            print(f"1 BCH = {api_response['price_format']} USD")
        except (ConnectionError, Timeout, TooManyRedirects) as e:
            print(e)
            api_response = 'error'

        return api_response

if __name__ == '__main__':
    credentials_file = 'credentials.json'
    credentials_path = os.path.join(os.path.abspath('..'), credentials_file)   
    with open(credentials_path) as f:
        data = f.read()
    credential_dict = json.loads(data)
    cmcapi = CoinMarketCapAPI(credential_dict['coinmarketcap_apikey'])
    api_response = cmcapi.get_bch_price()
    print(api_response)