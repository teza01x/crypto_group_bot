import sqlite3
import random
from config import *


def add_alert_to_database(data, link, wallet):
    conn = sqlite3.connect(data_base)
    cursor = conn.cursor()

    def order_id_generation():
        cursor.execute("SELECT order_id FROM wallet_tracking")
        data = cursor.fetchall()


        uniq_numbers = [i[0] for i in data]
        while True:
            random_number = random.randint(101, 9999999)
            if random_number in uniq_numbers:
                pass
            else:
                break
        return random_number


    cursor.execute("INSERT INTO wallet_tracking (order_id, text_alert, status, txs_link, wallet_adr) VALUES(?, ?, ?, ?, ?)",(order_id_generation(), data, 0, link, wallet,))

    conn.commit()
    conn.close()


def database_wallets():
    conn = sqlite3.connect(data_base)
    cursor = conn.cursor()

    cursor.execute("SELECT wallet FROM wallets")
    wallets = cursor.fetchall()

    wallets = [i[0].lower() for i in wallets]

    conn.close()

    return wallets


def get_coindesk_news():
    conn = sqlite3.connect(data_base)
    cursor = conn.cursor()

    cursor.execute("SELECT news FROM rss_news WHERE website = ?", ("coindesk",))

    news = cursor.fetchone()[0]

    conn.close()

    return news


def get_cointelegraph_news():
    conn = sqlite3.connect(data_base)
    cursor = conn.cursor()

    cursor.execute("SELECT news FROM rss_news WHERE website = ?", ("cointelegraph",))

    news = cursor.fetchone()[0]

    conn.close()

    return news


def write_rss_news(news, website):
    conn = sqlite3.connect(data_base)
    cursor = conn.cursor()

    cursor.execute("UPDATE rss_news SET news = ? WHERE website = ?", (news, website,))

    conn.commit()
    conn.close()


def get_token_price_from_db(coin):
    conn = sqlite3.connect(data_base)
    cursor = conn.cursor()

    cursor.execute("SELECT price FROM coin_tracker WHERE coin = ?", (coin,))
    coin_price = cursor.fetchone()[0]

    conn.close()

    if coin_price == None:
        return 0.1 * 10**(-20)
    else:
        return coin_price


def rewrite_coin_price(price, coin):
    conn = sqlite3.connect(data_base)
    cursor = conn.cursor()

    cursor.execute("UPDATE coin_tracker SET price = ? WHERE coin = ?", (price, coin,))

    conn.commit()
    conn.close()


def write_coin_info(price, coin, contract):
    conn = sqlite3.connect(data_base)
    cursor = conn.cursor()

    cursor.execute("INSERT INTO coin_tracker (coin, price, contract) VALUES(?, ?, ?)", (coin, price, contract,))

    conn.commit()
    conn.close()


def get_bot_status():
    conn = sqlite3.connect(data_base)
    cursor = conn.cursor()

    cursor.execute("SELECT status FROM bot_status WHERE operation = ?", ("work_status",))
    result = cursor.fetchone()[0]

    conn.close()

    return result


def change_bot_status(bot_status):
    conn = sqlite3.connect(data_base)
    cursor = conn.cursor()

    cursor.execute("UPDATE bot_status SET status = ? WHERE operation = ?", (bot_status, "work_status",))

    conn.commit()
    conn.close()


def get_thx_list():
    conn = sqlite3.connect(data_base)
    cursor = conn.cursor()

    cursor.execute("SELECT text_alert, wallet_adr FROM wallet_tracking WHERE status = ?", (0,))
    result = cursor.fetchall()

    conn.close()

    return result


def change_thx_status(status, text_alert):
    conn = sqlite3.connect(data_base)
    cursor = conn.cursor()

    cursor.execute("UPDATE wallet_tracking SET status = ? WHERE text_alert = ?", (status, text_alert,))

    conn.commit()
    conn.close()


def get_coin_id_list():
    conn = sqlite3.connect(data_base)
    cursor = conn.cursor()

    cursor.execute("SELECT coin FROM coin_tracker")
    result = cursor.fetchall()

    conn.close()

    return [i[0] for i in result]


def get_coin_contract_from_db(coin_id):
    conn = sqlite3.connect(data_base)
    cursor = conn.cursor()

    cursor.execute("SELECT contract FROM coin_tracker WHERE coin = ?", (coin_id,))
    result = cursor.fetchone()[0]

    conn.close()

    return result


def del_token_by_contract(contract):
    conn = sqlite3.connect(data_base)
    cursor = conn.cursor()

    cursor.execute("DELETE FROM coin_tracker WHERE contract = ?", (contract,))

    conn.commit()
    conn.close()


def add_wallet_to_db(wallet, name):
    conn = sqlite3.connect(data_base)
    cursor = conn.cursor()

    cursor.execute("INSERT INTO wallets (wallet, name) VALUES(?, ?)", (wallet.lower(), name,))

    conn.commit()
    conn.close()


def del_wallet_from_db(wallet):
    conn = sqlite3.connect(data_base)
    cursor = conn.cursor()

    cursor.execute("DELETE FROM wallets WHERE wallet = ?", (wallet,))

    conn.commit()
    conn.close()


def get_wallet_name(wallet):
    conn = sqlite3.connect(data_base)
    cursor = conn.cursor()

    cursor.execute("SELECT name FROM wallets WHERE wallet = ?", (wallet.lower(),))
    result = cursor.fetchone()[0]

    conn.close()

    if result != None and len(result) > 0:
        return result
    else:
        return ""


def write_wallet_image_name(image_name, wallet):
    conn = sqlite3.connect(data_base)
    cursor = conn.cursor()

    cursor.execute("UPDATE wallets SET image = ? WHERE wallet = ?", (image_name, wallet,))

    conn.commit()
    conn.close()


def get_wallet_image_name(wallet):
    conn = sqlite3.connect(data_base)
    cursor = conn.cursor()

    cursor.execute("SELECT image from wallets WHERE wallet = ?", (wallet,))
    result = cursor.fetchone()[0]

    conn.close()

    if result != None and len(result) > 0:
        return result
    else:
        return ""


def get_txs_link(wallet, text_alert):
    conn = sqlite3.connect(data_base)
    cursor = conn.cursor()

    cursor.execute("SELECT txs_link FROM wallet_tracking WHERE wallet_adr = ? AND text_alert = ?", (wallet, text_alert,))
    result = cursor.fetchone()[0]

    conn.close()

    return result
