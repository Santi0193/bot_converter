import requests
import json

class APIException(Exception):
    pass

class CurrencyConverter:
    @staticmethod
    def get_price(base, quote, amount):
        try:
            base = base.upper()
            quote = quote.upper()
            amount = float(amount)
            if base == quote:
                return amount, base, quote
            url = f"https://api.exchangerate-api.com/v4/latest/{base}"
            response = requests.get(url)
            response.raise_for_status()  # Raises a HTTPError for 4xx and 5xx status codes.
            data = json.loads(response.text)
            if 'error' in data:
                raise APIException(data['error'])
            if quote not in data['rates']:
                raise APIException(f"Валюта '{quote}' не поддерживается.")
            return round(data['rates'][quote] * amount, 2), base, quote
        except ValueError:
            raise APIException("Сумма должна быть числом.")
        except requests.exceptions.RequestException:
            raise APIException("Некорректная команда. Сообщение должно быть следующего формата: <валюта для проверки> <валюта для конвертации> <сумма>")