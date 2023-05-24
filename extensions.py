import requests
import json
from config import keys


class ConvertException(Exception):
    pass


class WalletConverter:
    @staticmethod
    def get_price(base: str, sym: str, amount):
        if base == sym:
            raise ConvertException(f'Валюты совпадают')

        try:
            sym_ticker = keys[sym]
        except KeyError:
            raise ConvertException(f'Не удалось обработать валюту {sym}')

        try:
            base_ticker = keys[base]
        except KeyError:
            raise ConvertException(f'Не удалось обработать валюту {base}')

        try:
            amount = float(amount)
        except ValueError:
            raise ConvertException(f'Не удалось обработать количество {amount}')
        url = f'https://api.apilayer.com/exchangerates_data/convert?to=' \
              f'{sym_ticker}&from={base_ticker}&amount={amount}'
        payload = {}
        header = {'apikey': 'dotGOB1Hk3LEF6k87UjKLL4FgTSeBi7C'}
        r = requests.get(url, headers=header, data=payload)
        resp = json.loads(r.content)
        result = round(resp['result'], 3)
        message = f'цена {amount} {base} в {sym} - {result}'
        return message

