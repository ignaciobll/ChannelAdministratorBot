import telebot
import json

with open("./bot.token", "r") as TOKEN:
    bot = telebot.TeleBot(TOKEN.read().strip())

with open("./channel_info.json", "r") as channel_info:
    channel_info = json.load(channel_info)
    idChannel = channel_info['idChannel']

with open('./data/admins.json', 'r') as adminData:
    admins = json.load(adminData)

with open("./data/text.json", 'r') as text:
    jtext = json.load(text)
    start_text = jtext['start']
    nuevoCanal_text = jtext['nuevoCanal']
    nuevoCanal_ack_text = jtext['nuevoCanal_ack']
    cancel_text = jtext['cancel']
    cancel_ack_text = jtext['cancel_ack']


def isAdmin_fromPrivate(message):
    if message.chat.type == 'private':
        userID = message.from_user.id
        if str(userID) in admins:
            return True
        return False


def parse_group_name(name):
    if (name.strip()[0] == '@'):
        return name.strip()
    else:
        return '@' + name.split('/')[-1]

# Lista de usuarios activos, uid -> paso por el que van
active_users = {849577: {'canales': [{'nombre': ''}], 'paso': 0}}


@bot.message_handler(commands=['start'])
def start(m):
    active_users[m.from_user.id]['paso'] = 0
    bot.send_message(m.chat.id, start_text)


@bot.message_handler(commands=['nuevoCanal'])
def nuevoCanal(m):
    active_users[m.from_user.id]['paso'] = 1
    bot.send_message(m.chat.id, nuevoCanal_text)
    bot.send_message(m.chat.id, cancel_text)


@bot.message_handler(func=lambda m: m.content_type == 'text' and
                     active_users[m.from_user.id]['paso'] == 1)
def nombre_del_grupo(m):
    name = parse_group_name(m.text)
    active_users[m.from_user.id]['canales'][0]['nombre'] = name
    bot.send_message(m.chat.id, nuevoCanal_ack_text + name)


@bot.message_handler(commands=['cancelar'])
def cancelar(m):
    active_users[m.from_user.id] = {'paso': 0}
    bot.send_message(m.chat.id, cancel_ack_text)


# bot.send_message("@ignaciobllChannelTest", "Hiper test")

bot.skip_pending = True

print("Running...")

bot.polling()
