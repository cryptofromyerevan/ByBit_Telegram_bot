from telethon.sync import TelegramClient, events
import configparser
import json
import bybit

from telethon import TelegramClient

def check_new_order():
    client = bybit.bybit(test=False, api_key="__", api_secret="__")
    resp = (client.Order.Order_getOrders().result())
    if 'New' in resp[0]['result']['data'][0]['order_status']:
        return 0
    else:
        return 1


def bybit_trade(action, entry_point, stop_loss__, tp):
    client = bybit.bybit(test=False, api_key="__", api_secret="__")
    print(client.Order.Order_new(side=action, symbol="BTCUSD", order_type="Limit", qty=1, price=entry_point,
                                 time_in_force="GoodTillCancel", take_profit=tp, stop_loss=stop_loss__).result())

config = configparser.ConfigParser()
config.read("config.ini")

# Setting configuration values
api_id = config['Telegram']['api_id']
api_hash = config['Telegram']['api_hash']

api_hash = str(api_hash)

phone = config['Telegram']['phone']
username = config['Telegram']['username']

client = TelegramClient(username, api_id, api_hash)
client.start()
print("Client Created")
# Ensure you're authorized
if not client.is_user_authorized():
    client.send_code_request(phone)
    try:
        client.sign_in(phone, input('Enter the code: '))
    except:
        client.sign_in(password=input('Password: '))


async def handler(update):
    tg = (update.to_dict())
    msg = tg['message']['message']
    if check_new_order()==0:
        print("[*] There is some new order")
        return

    if ("XBTUSD LONG" in msg):
        msg_arr = msg.split('\n')
        entry_point = stop_loss__ = __targets__ = 0
        for _msg_parsed in msg_arr:
            if ("Entry" in _msg_parsed):
                entry_point = _msg_parsed.split(":")[1].split('/')[1]
                print(entry_point)
            if ("Stop loss" in _msg_parsed):
                stop_loss__ = _msg_parsed.split(":")[1]
                print(stop_loss__)
            if ("Targets" in _msg_parsed):
                __targets__ = _msg_parsed.split(":")[1].split('/')[0]
                print(__targets__)

        entry_point = entry_point.strip()
        stop_loss__ = stop_loss__.strip()
        __targets__ = __targets__.strip()
        bybit_trade("Buy", int(entry_point)+5, stop_loss__, int(__targets__)-5)

    if ("XBTUSD SHORT" in msg):
        msg_arr = msg.split('\n')
        entry_point = stop_loss__ = __targets__ = 0
        for _msg_parsed in msg_arr:
            if ("Entry" in _msg_parsed):
                entry_point = _msg_parsed.split(":")[1].split('/')[0]
                print(entry_point)
            if ("Stop loss" in _msg_parsed):
                stop_loss__ = _msg_parsed.split(":")[1]
                print(stop_loss__)
            if ("Targets" in _msg_parsed):
                __targets__ = _msg_parsed.split(":")[1].split('/')[0]
                print(__targets__)

        entry_point = entry_point.strip()
        stop_loss__ = stop_loss__.strip()
        __targets__ = __targets__.strip()
        bybit_trade("Sell", int(entry_point)-5, stop_loss__, int(__targets__)+5)


# Use the client in a `with` block. It calls `start/disconnect` automatically.
with TelegramClient('za_c_k.session', api_id, api_hash) as client:
    # Register the update handler so that it gets called
    client.add_event_handler(handler)

    # Run the client until Ctrl+C is pressed, or the client disconnects
    print('(Press Ctrl+C to stop this)')
    client.run_until_disconnected()
