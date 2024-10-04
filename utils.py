from fake_useragent import UserAgent
import requests
import json

def get_balance(wallet: str) -> list[dict]:
    url = f'https://tonapi.io/v2/accounts/{wallet}'
    response = requests.get(url, headers={'User-Agent': f'{UserAgent().random}'})
    return json.loads(response.text)