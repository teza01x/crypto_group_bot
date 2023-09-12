import asyncio
import random
from telebot.async_telebot import AsyncTeleBot
from telebot.types import InlineKeyboardMarkup
from telebot import types
from telebot.types import InputFile
from datetime import datetime
from config import *
from sql_scripts import *
from rss_news import *
from coingecko_api import *


bot = AsyncTeleBot(telegram_token)


async def random_img_name():
    name_list = list()

    for i in range(1, 15):
        name_list.append(random.randint(97, 122))

    for i in range(1, 5):
        name_list.append(random.randint(48, 57))

    name_list = [chr(i) for i in name_list]

    return "{}.jpg".format("".join(name_list))


@bot.message_handler(commands=['start'])
async def start(message):
    user_id = message.from_user.id
    group_chat_id = message.chat.id

    # print(message)
    with open("admin_id.txt", 'r') as file:
        admin_id = int(file.readline())

    with open("group_id.txt", 'r') as file:
        group_id = int(file.readline())

    if user_id == admin_id and group_id == group_chat_id:
        await bot.send_message(message.chat.id, text="Hello!👋\n⭐️This is Crypto Bot.⭐️\n")
    elif user_id == admin_id:
        await bot.send_message(message.chat.id, text="Hello!👋\n⭐️This is Crypto Bot.⭐️\n")


@bot.message_handler(commands=['commands'])
async def commands_list(message):
    user_id = message.from_user.id
    group_chat_id = message.chat.id

    with open("admin_id.txt", 'r') as file:
        admin_id = int(file.readline())

    with open("group_id.txt", 'r') as file:
        group_id = int(file.readline())

    if user_id == admin_id and group_id == group_chat_id:
        await bot.send_message(message.chat.id, text="📝 List of commands: 📝\n"
                                                     "\n/launch_bot - Starts the bot and all functions."
                                                     "\n/stop_bot - Stops the bot and all functions."
                                                     "\n/add_token <contract address> - Adds a token to the database using the token contract address."
                                                     "\n/del_token <contract address> - Deletes a token from the database using the token contract address."
                                                     "\n/add_wallet <wallet address> - Adds a wallet to the database using the blockchain address of the wallet."
                                                     "\n/del_wallet <wallet address> - Removes the specified wallet from the database."
                                                     "\n/add_image <wallet address> - Adds an image for the specified wallet.")
    elif user_id == admin_id:
        await bot.send_message(message.chat.id, text="📝 List of commands: 📝\n"
                                                     "\n/launch_bot - Starts the bot and all functions."
                                                     "\n/stop_bot - Stops the bot and all functions."
                                                     "\n/add_token <contract address> - Adds a token to the database using the token contract address."
                                                     "\n/del_token <contract address> - Deletes a token from the database using the token contract address."
                                                     "\n/add_wallet <wallet address> - Adds a wallet to the database using the blockchain address of the wallet."
                                                     "\n/del_wallet <wallet address> - Removes the specified wallet from the database."
                                                     "\n/add_image <wallet address> - Adds an image for the specified wallet.")


@bot.message_handler(commands=['add_token'])
async def add_token(message):
    user_id = message.from_user.id
    group_chat_id = message.chat.id

    with open("admin_id.txt", 'r') as file:
        admin_id = int(file.readline())

    with open("group_id.txt", 'r') as file:
        group_id = int(file.readline())

    if user_id == admin_id and group_id == group_chat_id:
        text = message.text
        text = text.replace('/add_token', '')
        lst = [i for i in text.split() if i != '']
        contract_address = lst[0].lower()
        try:
            add_token_to_db(contract_address)
            await bot.send_message(message.chat.id, text="✅ You have successfully ADDED TOKEN ✅\n\nUsing the following contract address:\n{}".format(contract_address))
        except Exception as error:
            print(error)
    elif user_id == admin_id:
        text = message.text
        text = text.replace('/add_token', '')
        lst = [i for i in text.split() if i != '']
        contract_address = lst[0].lower()
        try:
            add_token_to_db(contract_address)
            await bot.send_message(message.chat.id, text="✅ You have successfully ADDED TOKEN ✅\n\nUsing the following contract address:\n{}".format(contract_address))
        except Exception as error:
            print(error)


@bot.message_handler(commands=['del_token'])
async def del_token(message):
    user_id = message.from_user.id
    group_chat_id = message.chat.id

    with open("admin_id.txt", 'r') as file:
        admin_id = int(file.readline())

    with open("group_id.txt", 'r') as file:
        group_id = int(file.readline())

    if user_id == admin_id and group_id == group_chat_id:
        text = message.text
        text = text.replace('/del_token', '')
        lst = [i for i in text.split() if i != '']
        contract_address = lst[0].lower()
        try:
            del_token_by_contract(contract_address)
            await bot.send_message(message.chat.id, text='❌ You have successfully DELETED TOKEN ❌\n\nUsing the following contract address:\n{}'.format(contract_address))
        except Exception as error:
            print(error)
    elif user_id == admin_id:
        text = message.text
        text = text.replace('/del_token', '')
        lst = [i for i in text.split() if i != '']
        contract_address = lst[0].lower()
        try:
            del_token_by_contract(contract_address)
            await bot.send_message(message.chat.id, text='❌ You have successfully DELETED TOKEN ❌\n\nUsing the following contract address:\n{}'.format(contract_address))
        except Exception as error:
            print(error)


@bot.message_handler(commands=['add_wallet'])
async def add_wallet(message):
    user_id = message.from_user.id
    group_chat_id = message.chat.id

    with open("admin_id.txt", 'r') as file:
        admin_id = int(file.readline())

    with open("group_id.txt", 'r') as file:
        group_id = int(file.readline())

    if user_id == admin_id and group_id == group_chat_id:
        text = message.text
        text = text.replace('/add_wallet', '')
        lst = [i for i in text.split() if i != '']
        lst.append('')
        wallet_address = lst[0].lower()
        wallet_name = lst[1]
        try:
            add_wallet_to_db(wallet_address, wallet_name)
            await bot.send_message(message.chat.id, text='✅ You have successfully ADDED WALLET ✅\n\nUsing the following blockchain address:\n{}'.format(wallet_address))
        except Exception as error:
            print(error)
    elif user_id == admin_id:
        text = message.text
        text = text.replace('/add_wallet', '')
        lst = [i for i in text.split() if i != '']
        lst.append('')
        wallet_address = lst[0].lower()
        wallet_name = lst[1]
        try:
            add_wallet_to_db(wallet_address, wallet_name)
            await bot.send_message(message.chat.id, text='✅ You have successfully ADDED WALLET ✅\n\nUsing the following blockchain address:\n{}'.format(wallet_address))
        except Exception as error:
            print(error)


@bot.message_handler(commands=['del_wallet'])
async def del_wallet(message):
    user_id = message.from_user.id
    group_chat_id = message.chat.id

    with open("admin_id.txt", 'r') as file:
        admin_id = int(file.readline())

    with open("group_id.txt", 'r') as file:
        group_id = int(file.readline())

    if user_id == admin_id and group_id == group_chat_id:
        text = message.text
        text = text.replace('/del_wallet', '')
        lst = [i for i in text.split() if i != '']
        wallet_address = lst[0].lower()
        try:
            del_wallet_from_db(wallet_address)
            await bot.send_message(message.chat.id, text='❌ You have successfully DELETED WALLET ❌\n\nUsing the following blockchain address:\n{}'.format(wallet_address))
        except Exception as error:
            print(error)
    elif user_id == admin_id:
        text = message.text
        text = text.replace('/del_wallet', '')
        lst = [i for i in text.split() if i != '']
        wallet_address = lst[0].lower()
        try:
            del_wallet_from_db(wallet_address)
            await bot.send_message(message.chat.id, text='❌ You have successfully DELETED WALLET ❌\n\nUsing the following blockchain address:\n{}'.format(wallet_address))
        except Exception as error:
            print(error)


@bot.message_handler(commands=['launch_bot'])
async def launch_bot(message):
    user_id = message.from_user.id
    group_chat_id = message.chat.id

    with open("admin_id.txt", 'r') as file:
        admin_id = int(file.readline())

    with open("group_id.txt", 'r') as file:
        group_id = int(file.readline())

    if user_id == admin_id and group_id == group_chat_id:
        try:
            change_bot_status("True")
            await bot.send_message(message.chat.id, text=dct['launch_bot'])
        except Exception as error:
            print(error)
    elif user_id == admin_id:
        try:
            change_bot_status("True")
            await bot.send_message(message.chat.id, text=dct['launch_bot'])
        except Exception as error:
            print(error)


@bot.message_handler(commands=['stop_bot'])
async def stop_bot(message):
    user_id = message.from_user.id
    group_chat_id = message.chat.id

    with open("admin_id.txt", 'r') as file:
        admin_id = int(file.readline())

    with open("group_id.txt", 'r') as file:
        group_id = int(file.readline())

    if user_id == admin_id and group_id == group_chat_id:
        try:
            change_bot_status("False")
            await bot.send_message(message.chat.id, text=dct['stop_bot'])
        except Exception as error:
            print(error)
    elif user_id == admin_id:
        try:
            change_bot_status("False")
            await bot.send_message(message.chat.id, text=dct['stop_bot'])
        except Exception as error:
            print(error)


@bot.message_handler(content_types=["photo"])
async def add_image(message):
    user_id = message.from_user.id
    group_chat_id = message.chat.id

    with open("admin_id.txt", 'r') as file:
        admin_id = int(file.readline())

    with open("group_id.txt", 'r') as file:
        group_id = int(file.readline())

    if user_id == admin_id and group_id == group_chat_id:
        try:
            check_command = message.caption.split(" ")
            if check_command[0] == '/add_image':
                text = message.caption
                text = text.replace('/add_image', '')
                lst = [i for i in text.split() if i != '']
                wallet_address = lst[0].lower()


                fileID = message.photo[-1].file_id
                file_info = await bot.get_file(fileID)
                downloaded_file = await bot.download_file(file_info.file_path)

                random_file_name = await random_img_name()
                image = image_path + random_file_name

                with open(image, 'wb') as new_file:
                    new_file.write(downloaded_file)

                db_wallets = database_wallets()

                for wallet in db_wallets:
                    if wallet.lower() == wallet_address:
                        write_wallet_image_name(random_file_name, wallet_address)
                        await bot.send_message(message.chat.id, text=dct['add_wallet_image'].format(wallet_address))
        except Exception as error:
            print(error)

    elif user_id == admin_id:
        try:
            check_command = message.caption.split(" ")
            if check_command[0] == '/add_image':
                text = message.caption
                text = text.replace('/add_image', '')
                lst = [i for i in text.split() if i != '']
                wallet_address = lst[0].lower()

                fileID = message.photo[-1].file_id
                file_info = await bot.get_file(fileID)
                downloaded_file = await bot.download_file(file_info.file_path)

                random_file_name = await random_img_name()
                image = image_path + random_file_name

                with open(image, 'wb') as new_file:
                    new_file.write(downloaded_file)

                db_wallets = database_wallets()

                for wallet in db_wallets:
                    if wallet.lower() == wallet_address:
                        write_wallet_image_name(random_file_name, wallet_address)
                        await bot.send_message(message.chat.id, text=dct['add_wallet_image'].format(wallet_address))
        except Exception as error:
            print(error)


## point 4
async def trending_coins_info():
    while True:
        if get_bot_status() == "True":
            try:
                with open("group_id.txt", 'r') as file:
                    group_id = int(file.readline())

                trand_tokens_text = trending_coins()

                await bot.send_message(group_id, text=trand_tokens_text)
            except Exception as error:
                print("ERROR TRENDING COINS BLOCK\n", error)
        await asyncio.sleep(3600)


## point 3
async def check_coin_info():
    while True:
        if get_bot_status() == "True":
            try:
                with open("group_id.txt", 'r') as file:
                    group_id = int(file.readline())

                coin_id_list = get_coin_id_list()

                for coin_id in coin_id_list:
                    result = check_coin_price(coin_id)
                    coin_contract = get_coin_contract_from_db(coin_id)

                    current_time = datetime.now()
                    formatted_time = current_time.strftime("%d.%m.%Y / %H:%M:%S")

                    if result[0] == True:
                        if result[1] == "UP":
                            await bot.send_message(group_id, text="⚠️ Token Tracker Alert ⚠️\n\nToken: {}\n\nTicker: {}\n\nLast update: {}\n\nPrice: +{}% (${})".format(
                                                       coin_contract, coin_id, formatted_time, result[3], result[2]))
                        elif result[1] == "DOWN":
                            await bot.send_message(group_id, text="⚠️ Token Tracker Alert ⚠️\n\nToken: {}\n\nTicker: {}\n\nLast update: {}\n\nPrice: {}% (${})".format(
                                                        coin_contract, coin_id, formatted_time, result[3], result[2]))
                    elif result[0] == False:
                        pass
            except Exception as error:
                print("ERROR CHECK PRICE BLOCK\n", error)
        await asyncio.sleep(25)

## point 2
async def send_rss_news():
    while True:
        if get_bot_status() == "True":
            try:
                with open("group_id.txt", 'r') as file:
                    group_id = int(file.readline())

                rss_coindesk = rss_coindesk_news()
                rss_cointelegraph = rss_cointelegraph_news()

                if rss_coindesk != get_coindesk_news():
                    write_rss_news(rss_coindesk, "coindesk")
                    await bot.send_message(group_id, text="🆕 NEWS 🆕\n" + rss_coindesk)

                if rss_cointelegraph != get_cointelegraph_news():
                    write_rss_news(rss_cointelegraph, "cointelegraph")
                    await bot.send_message(group_id, text="🆕 NEWS 🆕\n" + rss_cointelegraph)
            except Exception as error:
                print("ERROR RSS NEWS BLOCK\n", error)
        await asyncio.sleep(120)

## point 1
async def send_live_thx():
    while True:
        if get_bot_status() == "True":
            try:
                with open("group_id.txt", 'r') as file:
                    group_id = int(file.readline())

                thx_list = get_thx_list()
                if len(thx_list) > 0:
                    for i in range(len(thx_list)):
                        text_alert = thx_list[i][0]
                        wallet_address = thx_list[i][1]

                        txs_link = get_txs_link(wallet_address, text_alert)
                        button1 = [
                            types.InlineKeyboardButton("Transaction link", url=txs_link)
                            ]
                        reply_markup = InlineKeyboardMarkup([button1])

                        try:
                            photo_name = get_wallet_image_name(wallet_address)
                            if len(photo_name) > 0:
                                photo_path = image_path + photo_name

                                with open(photo_path, 'rb') as photo:
                                    await bot.send_photo(group_id, photo, caption=text_alert, reply_markup=reply_markup)
                            else:
                                await bot.send_message(group_id, text=text_alert, reply_markup=reply_markup)
                        except:
                            pass
                        change_thx_status(1, text_alert)
            except Exception as error:
                print("ERROR LIVE THX BLOCK\n", error)
        await asyncio.sleep(10)


async def main():
    bot_task = asyncio.create_task(bot.polling(non_stop=True, request_timeout=120))
    send_thx = asyncio.create_task(send_live_thx())
    send_news = asyncio.create_task(send_rss_news())
    check_price = asyncio.create_task(check_coin_info())
    trend_coins = asyncio.create_task(trending_coins_info())

    await asyncio.gather(bot_task, send_thx, send_news, check_price, trend_coins)
    # await asyncio.gather(bot_task, send_thx)


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.create_task(main())
    loop.run_forever()