# from TonTools import TonCenterClient, Wallet
# import asyncio


# async def main():
#     mnemonics = ['cotton', 'sight', 'key', 'digital', 'surround' ,'coral' ,'swift', 'cotton' ,'beyond' ,'obey' ,'youth', 'omit', 'proof',
#                 'heavy','jungle', 'old' ,'vanish', 'clog', 'nominee' ,'rally' ,'leopard', 'course', 'sample', 'warrior']
#     provider = TonCenterClient(base_url='https://toncenter.com/api/v2/')
#     wallet = Wallet(mnemonics=mnemonics, version='v3r2', provider=provider)

#     await wallet.transfer_ton(destination_address='UQCpnfSGHg1Iy74tk-RtU5pToQfjONi0CM1cCkxGfqAvLAUx',
#                               amount=0.01, message='str')

# if __name__ == '__main__':
#     asyncio.get_event_loop().run_until_complete(main())

print((41731122174410236047796743722730466018640279171473593600/10000)/3600)

import math

n = 2048 # Общее число элементов
k = 24  # Число элементов в сочетании

# Вычисление числа сочетаний
combinations = math.comb(n, k)
print(combinations)
