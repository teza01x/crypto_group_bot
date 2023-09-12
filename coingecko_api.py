import requests
from config import *
from sql_scripts import *


def trending_coins():
    try:
        url = 'https://api.coingecko.com/api/v3/search/trending'

        r = requests.get(url)
        data = r.json()
        trend_coins = data["coins"]

        result = ["📈 Trending coins 📈\n",]

        for coin in trend_coins:
            result.append("🔥 {} ({})".format(coin['item']['name'], coin['item']['symbol']))

        return "\n".join(result)
    except Exception as error:
        print(error)


def add_token_to_db(contract_address):
    try:
        def find_id_by_contract_address(data, contract_address):
            for entry in data:
                platforms = entry.get("platforms", {})
                for platform, address in platforms.items():
                    if address == contract_address:
                        return entry["id"]
            return None

        url = 'https://api.coingecko.com/api/v3/coins/list?include_platform=true'

        address_response = requests.get(url)
        token_list = address_response.json()

        token_id = find_id_by_contract_address(token_list, contract_address)

        url = f'https://api.coingecko.com/api/v3/coins/{token_id}/market_chart?vs_currency=usd&days=0'
        r = requests.get(url)
        data = r.json()

        token_price = data['prices'][0][1]

        write_coin_info(token_price, token_id, contract_address)
    except Exception as error:
        print(error)


def check_coin_price(coin_id):
    try:
        url = f'https://api.coingecko.com/api/v3/coins/{coin_id}/market_chart?vs_currency=usd&days=0'
        r = requests.get(url)
        data = r.json()

        token_price = data['prices'][0][1]

        # print(token_price)

        old_price = get_token_price_from_db(coin_id)

        diff = ((token_price - old_price) / old_price) * 100

        if diff >= price_diff_up:
            rewrite_coin_price(token_price, coin_id)
            return [True, "UP", token_price, diff]
        elif diff <= (-price_diff_down):
            rewrite_coin_price(token_price, coin_id)
            return [True, "DOWN", token_price, diff]

        return [False, None, None, None]
    except Exception as error:
        print(error)
