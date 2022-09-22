import environs
from requests import get
from pycoingecko import CoinGeckoAPI
from telebot import TeleBot

env = environs.Env()
env.read_env('.env')

BOT_TOKEN = env('BOT_TOKEN')
API_KEY = env('API_KEY')
BASE_URL = "https://api.etherscan.io/api"
ETH_VALUE = 10 ** 18
address = "wallet_address"

def make_api_url(module,action,address,**kwargs):
    url = BASE_URL + f"?module={module}&action={action}&address={address}&apikey={API_KEY}"

    for key, value in kwargs.items():
        url+=f"&{key}={value}"
    
    return url

def get_account_balance():
    get_balance_url = make_api_url("account", "balance", address, tag="latest", x="2")

    response = get(get_balance_url)
    data = response.json()
    return int(data["result"]) / ETH_VALUE

eth_amount = get_account_balance()

bot = TeleBot(token=BOT_TOKEN)
coin_client = CoinGeckoAPI()

@bot.message_handler(content_types=['text'])
def crypto_price_message_handler(message):
    price_response = coin_client.get_price(ids="ethereum", vs_currencies="usd")
    if price_response:
        price = price_response["ethereum"]["usd"] * eth_amount
    else:
        price = 0
    if message.text == "g":
        bot.send_message(chat_id=message.chat.id, text=f"balance of ethereum: {eth_amount}\nusd value: {price}")

if __name__ == '__main__':
    bot.polling()