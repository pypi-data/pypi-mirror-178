import requests

r = requests.get('https://discord.com/api/last_price/BTC/USD')
print(r.json())
