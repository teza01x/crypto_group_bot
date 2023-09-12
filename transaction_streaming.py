from flask import Flask, request
from datetime import datetime
from moralis import evm_api
from sql_scripts import *
from language_scripts import *
from config import *


app = Flask(__name__)


@app.route('/', methods=['POST'])
def handle_post_request():
    if request.method == 'POST':
        data = request.json
        try:
            try:
                if data['confirmed'] == True and data['streamId'] == stream_id:

                    db_wallets = database_wallets()

                    wallet_1 = data['erc20Transfers'][0]['from'].lower()
                    wallet_2 = data['erc20Transfers'][0]['to'].lower()

                    wallet = str()
                    for wlt in db_wallets:
                        if wlt.lower() == wallet_1:
                            wallet = wallet_1
                        elif wlt.lower() == wallet_2:
                            wallet = wallet_2

                    transactionHash = data['erc20Transfers'][0]['transactionHash']
                    contract = data['erc20Transfers'][0]['contract']
                    value = float(data['erc20Transfers'][0]['valueWithDecimals'])
                    token_symbol = data['erc20Transfers'][0]['tokenSymbol']
                    contract_adress = '{} ({} {})'.format(contract, value, token_symbol)

                    timestamp = int(data['block']['timestamp'])
                    dt_object = datetime.fromtimestamp(timestamp)

                    formatted_date = dt_object.strftime('%Y.%m.%d / %H:%M:%S')

                    chain_id = str()
                    for chain in chains:
                        if chain == data['chainId']:
                            chain_id = chains[chain]

                    txs_link = str()
                    for blockchain in transfer_info:
                        if chain_id == blockchain:
                            scan_link = transfer_info[blockchain][1]

                    txs_link = scan_link + transactionHash

                    params = {
                        "address": contract,
                        "chain": chain_id,
                    }

                    result = evm_api.token.get_token_price(
                        api_key=api_key,
                        params=params,
                    )

                    token_value_usd = result['usdPrice']
                    total_value = round(value * token_value_usd, 2)

                    wallet_name = get_wallet_name(wallet)

                    if data['erc20Transfers'][0]['to'].lower() == wallet.lower():
                        status_txs = 'IN'
                        adr_from = data['erc20Transfers'][0]['from']
                        adr_to = wallet
                        whale_alert = dct['thx_alert_erc20_in'].format(wallet_name, wallet, transactionHash,
                                                                       contract_adress,
                                                                       formatted_date, total_value)
                    elif data['erc20Transfers'][0]['to'].lower() != wallet.lower():
                        status_txs = 'OUT'
                        adr_from = wallet
                        adr_to = data['erc20Transfers'][0]['to']
                        whale_alert = dct['thx_alert_erc20_out'].format(wallet_name, wallet, transactionHash,
                                                                        contract_adress,
                                                                        formatted_date, total_value)
                    add_alert_to_database(whale_alert, txs_link, wallet)
            except:
                try:
                    if data['confirmed'] == True and data['streamId'] == stream_id:

                        db_wallets = database_wallets()

                        wallet_1 = data['txs'][0]['fromAddress'].lower()
                        wallet_2 = data['txs'][0]['toAddress'].lower()

                        wallet = str()
                        for wlt in db_wallets:
                            if wlt.lower() == wallet_1:
                                wallet = wallet_1
                            elif wlt.lower() == wallet_2:
                                wallet = wallet_2

                        transactionHash = data['txs'][0]['hash']
                        value = int(data['txs'][0]['value']) / 10 ** 18
                        timestamp = int(data['block']['timestamp'])
                        dt_object = datetime.fromtimestamp(timestamp)
                        formatted_date = dt_object.strftime('%Y.%m.%d / %H:%M:%S')

                        chain_id = str()
                        for chain in chains:
                            if chain == data['chainId']:
                                chain_id = chains[chain]

                        token_symbol, txs_link, coin_contract = str(), str(), str()
                        for blockchain in transfer_info:
                            if chain_id == blockchain:
                                token_symbol, scan_link, coin_contract = transfer_info[blockchain][0], transfer_info[blockchain][1], transfer_info[blockchain][2]

                        txs_link = scan_link + transactionHash

                        params = {
                            "address": coin_contract,
                            "chain": 'eth',
                        }

                        result = evm_api.token.get_token_price(
                            api_key=api_key,
                            params=params,
                        )

                        token_value_usd = result['usdPrice']
                        total_value = round(value * token_value_usd, 2)

                        wallet_name = get_wallet_name(wallet)

                        if data['txs'][0]['toAddress'].lower() == wallet.lower():
                            status_txs = 'IN'
                            adr_from = data['txs'][0]['fromAddress'].lower()
                            adr_to = wallet
                            whale_alert = dct['thx_alert_native_in'].format(wallet_name, wallet, transactionHash, value, token_symbol, formatted_date, total_value)
                        elif data['txs'][0]['toAddress'].lower() != wallet.lower():
                            status_txs = 'OUT'
                            adr_from = wallet
                            adr_to = data['txs'][0]['toAddress'].lower()
                            whale_alert = dct['thx_alert_native_out'].format(wallet_name, wallet, transactionHash, value, token_symbol, formatted_date, total_value)
                        add_alert_to_database(whale_alert, txs_link, wallet)
                except Exception as error:
                    print(error)
        except:
            pass
        return 'Received and processed the POST request!', 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
