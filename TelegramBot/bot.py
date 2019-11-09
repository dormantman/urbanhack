# -*- coding: utf-8 -*-

# Imports

import json
import os
import random
import threading
import time

import telebot
from telebot import apihelper, types
import dmlogging
import logging

import base64

from user import api

dmlogging.init('bot.log', 'INFO')


class TelegramBot:
    """ This is Bot Class """

    site = 'urbanalerts.ml'

    def __init__(self):
        config = {'name': 'TelegramBot', 'version': '0.1.0', 'token': '514961786:AAEiDweTejyGGYgEhEhCchzUtHI8Uk2wXAg'}

        self.f = FilesExchange(config=config, users={}, strings={})

        commands = {
            'ping':  'on_ping',
            'stop':  'on_stop',
            'start': 'on_start',
        }

        contents = {
            'photo':    'on_photo',
            'audio':    'on_audio',
            'video':    'on_video',
            'voice':    'on_voice',
            'sticker':  'on_sticker',
            'contact':  'on_contact',
            'document': 'on_document',
            'location': 'on_location',
        }

        keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
        keyboard.add(types.KeyboardButton(text="Отправить местоположение", request_location=True),
                     types.KeyboardButton(text='Отмена'))

        self.migration = {
            'menu':        self.markups('Сообщить о проблеме 🌱'),
            'settings':    self.markups('Что-то настроить', 'Вернуться'),
            'title':       self.markups('Отмена'),
            'photo':       self.markups('Пропустить', 'Отмена'),
            'description': self.markups('Отмена'),
            'tag':         self.markups(['Экология', 'Урбанистика'], 'Общество', 'Отмена'),
            'address':     keyboard,
            'suggest':     self.markups(['Отправить', 'Отменить'])
        }

        self.strings = {
            'start':       'Добрый день.\n\nВас приветсвтует *Urban Alerts Bot*.\n\nС моей помощью вы сможете быстро '
                           'сообщать о различных проблемах в Вашем городе.\nТакже Вы можете посетить сайт '
                           f'{self.site}',

            'menu':        "При необходимости вы можете быстро сообщить об экологической проблеме, "
                           "наша система оповещений работает в реальном времени",
            'title':       'Сообщение о новой проблеме\n\nВведите заголовок для проблемы:',
            'photo':       '*Отправьте фотоотчет проблемы*\n\nПри необходимости вы можете пропустить этот шаг, '
                           'но для улучшения качества просим вас отправить фотоотчет...',
            'description': "Опишите несколькими словами вашу проблему:",
            'tag':         'Выберите тип проблемы:',
            'address':     "Отправьте местоположение проблемы",
            'suggest':     "Проверьте свою проблему.\nПодтверждаете ли вы отправку проблемы?\n\n{}"
        }

        print(self.f.config['name'], self.f.config['version'])

        self.bot = telebot.TeleBot(
            self.f.config['token'],
            num_threads=(self.f.config['num_threads'] if 'num_threads' in self.f.config else 2)
        )

        if 'proxy' in self.f.config:
            apihelper.proxy = {
                'https': self.f.config['proxy']
            }

        for command in commands:
            exec(
                '@self.bot.message_handler(commands=[command])\n'
                'def {0}(message):\n'
                '    if self.check_user(message):\n'
                '        return\n'
                '    # logging.info("Command /{1}")\n'
                '    self.{2}(message)\n'.format(command, command, commands[command]),
                locals()
            )

        for content in contents:
            exec(
                '@self.bot.message_handler(content_types=[content])\n'
                'def {0}(message):\n'
                '    if self.check_user(message):\n'
                '        return\n'
                '    # logging.info("{1}")\n'
                '    self.{2}(message)\n'.format(content, content, contents[content]),
                locals()
            )

        @self.bot.callback_query_handler(func=lambda call: True)
        def callback_inline(call):
            logging.info('Callback')
            self.on_callback(call)

        @self.bot.message_handler(content_types=['text'])
        def echo_message(message):
            if self.check_user(message):
                return
            logging.info('Message')

            if message.text[0] == '/':
                self.on_unknown_command(message)

            else:
                self.new_message(message)

        @self.bot.edited_message_handler(func=lambda message: True)
        def edit_message(message):
            if self.check_user(message):
                return
            logging.info('Edit message')

            self.on_edited_message(message)

        @self.bot.inline_handler(func=lambda query: True)
        def inline_mode(query):
            logging.info('Inline_mode')

            self.on_inline_mode(query)

    def on_inline_mode(self, query):
        plus_icon = "https://pp.vk.me/c627626/v627626512/2a627/7dlh4RRhd24.jpg"
        minus_icon = "https://pp.vk.me/c627626/v627626512/2a635/ILYe7N2n8Zo.jpg"
        divide_icon = "https://pp.vk.me/c627626/v627626512/2a620/oAvUk7Awps0.jpg"
        multiply_icon = "https://pp.vk.me/c627626/v627626512/2a62e/xqnPMigaP5c.jpg"
        error_icon = "https://pp.vk.me/c627626/v627626512/2a67a/ZvTeGq6Mf88.jpg"

        try:
            num1, num2 = query.query.split()

        except (AttributeError, ValueError):
            return

        try:
            m_sum = int(num1) + int(num2)
            r_sum = telebot.types.InlineQueryResultArticle(
                id='1', title="Сумма",
                description="Результат: {!s}".format(m_sum),
                input_message_content=telebot.types.InputTextMessageContent(
                    message_text="{!s} + {!s} = {!s}".format(num1, num2, m_sum)),
                thumb_url=plus_icon, thumb_width=48, thumb_height=48
            )
            m_sub = int(num1) - int(num2)
            r_sub = telebot.types.InlineQueryResultArticle(
                id='2', title="Разность",
                description="Результат: {!s}".format(m_sub),
                input_message_content=telebot.types.InputTextMessageContent(
                    message_text="{!s} - {!s} = {!s}".format(num1, num2, m_sub)),
                thumb_url=minus_icon, thumb_width=48, thumb_height=48
            )
            if num2 is not "0":
                m_div = int(num1) / int(num2)
                r_div = telebot.types.InlineQueryResultArticle(
                    id='3', title="Частное",
                    description="Результат: {0:.2f}".format(m_div),
                    input_message_content=telebot.types.InputTextMessageContent(
                        message_text="{0!s} / {1!s} = {2:.2f}".format(num1, num2, m_div)),
                    thumb_url=divide_icon, thumb_width=48, thumb_height=48
                )
            else:
                r_div = telebot.types.InlineQueryResultArticle(
                    id='3', title="Частное", description="На ноль делить нельзя!",
                    input_message_content=telebot.types.InputTextMessageContent(
                        message_text="Я нехороший человек и делю на ноль!"),
                    thumb_url=error_icon, thumb_width=48, thumb_height=48,
                    url="https://ru.wikipedia.org/wiki/%D0%94%D0%B5%D0%BB%D0%B5%D0%BD%D0%"
                        "B8%D0%B5_%D0%BD%D0%B0_%D0%BD%D0%BE%D0%BB%D1%8C",
                    hide_url=True
                )
            m_mul = int(num1) * int(num2)
            r_mul = telebot.types.InlineQueryResultArticle(
                id='4', title="Произведение",
                description="Результат: {!s}".format(m_mul),
                input_message_content=telebot.types.InputTextMessageContent(
                    message_text="{!s} * {!s} = {!s}".format(num1, num2, m_mul)),
                thumb_url=multiply_icon, thumb_width=48, thumb_height=48
            )
            self.bot.answer_inline_query(query.id, [r_sum, r_sub, r_div, r_mul], cache_time=0)
        except Exception as e:
            print("{!s}\n{!s}".format(type(e), str(e)))

    def on_edited_message(self, message):
        self.bot.send_message(
            message.chat.id,
            message.text
        )

    def on_unknown_command(self, message):
        self.bot.send_message(message.chat.id, "Неизвестная команда.")

    def on_callback(self, call):
        if call.message:
            self.bot.edit_message_text(
                chat_id=call.message.chat.id,
                message_id=call.message.message_id,
                text=f"Call data: {call.data}"
            )

    def on_stop(self, message):
        self.bot.send_message(message.chat.id, "Вы нажали /stop")

    def on_start(self, message):
        new_page = 'menu'
        self.ch_page(message.chat.id, new_page)
        self.bot.send_message(message.chat.id, self.strings['start'], reply_markup=self.migration[new_page],
                              parse_mode='Markdown')

    def on_sticker(self, message):
        logging.info('Sticker file id - %s' % message.sticker.file_id)
        self.bot.send_message(message.chat.id, "Вы прислали стикер.")

    def on_photo(self, message):
        user_id = message.from_user.id
        user = self.get_user(user_id)
        page = user["page"]

        if page == 'photo':
            photo = message.photo[-1]
            file_info = self.bot.get_file(photo.file_id)
            user['photo'] = 'data:;base64,' + base64.b64encode(self.bot.download_file(file_info.file_path)).decode()
            user['photo_table'] = photo.file_id
            new_page = 'tag'
            self.ch_page(user_id, new_page)
            self.bot.send_message(user_id, self.strings[new_page], reply_markup=self.migration[new_page],
                                  parse_mode="Markdown")

    def on_document(self, message):
        self.bot.send_message(message.chat.id, "Вы прислали документ.")

    def on_voice(self, message):
        self.bot.send_message(message.chat.id, "Вы прислали голос.")

    def on_video(self, message):
        self.bot.send_message(message.chat.id, "Вы прислали видео.")

    def on_audio(self, message):
        self.bot.send_message(message.chat.id, "Вы прислали аудио.")

    def on_contact(self, message):
        self.bot.send_message(message.chat.id, "Вы прислали контакт.")

    def on_location(self, message):
        user_id = message.from_user.id
        user = self.get_user(user_id)
        page = user["page"]

        if page == 'address':
            user['latitude'] = message.location.latitude
            user['longitude'] = message.location.longitude
            new_page = 'suggest'
            self.ch_page(user_id, new_page)
            table = '*{}*\n{}\n\n_{}_'.format(user['title'], user['description'], user['tag_table'])
            self.bot.send_message(user_id, self.strings[new_page].format(table), reply_markup=self.migration[new_page],
                                  parse_mode='Markdown')
            if 'photo_table' in user:
                self.bot.send_photo(user_id, user['photo_table'])

    def on_ping(self, message):
        self.bot.send_message(message.chat.id, random.choice(self.f.strings['ping']))

    def on_like(self, message):
        self.bot.send_message(message.chat.id, 'Благодарю! 😊\nМне очень приятно!')

        if 'stickers_like' in self.f.strings:
            self.bot.send_sticker(message.chat.id, random.choice(self.f.strings['stickers_like']))

    def ch_page(self, user_id, page):
        self.f.users[str(user_id)]['page'] = page

    def get_user(self, user_id):
        return self.f.users[str(user_id)]

    def check_user(self, message):
        # Check User in Dictionary Users

        if message.chat.id < 0:  # When bot was invited to a conversation
            return True

        if str(message.chat.id) in self.f.users:
            self.get_user(message.chat.id)['time'] = int(time.time())
            if self.get_user(message.chat.id)["chat"]:
                threading.Thread(target=self.f.update_users).start()
                return False
            else:
                threading.Thread(target=self.f.update_users).start()
                return True

        else:
            # self.clear()

            logging.warning('<<< new user >>>')

            self.f.users[str(message.chat.id)] = {
                "name":     message.from_user.first_name,
                "s_name":   message.from_user.last_name,
                "username": message.from_user.username,
                "page":     "start",
                "chat":     True,
                "start":    int(time.time()),
                "time":     int(time.time())

            }

            threading.Thread(target=self.f.update_users).start()
            return False

    def send_long_message(
            self,
            chat_id,
            text,
            disable_web_page_preview=None,
            reply_to_message_id=None,
            reply_markup=None,
            parse_mode=None,
            disable_notification=None,
            length=1000,
    ):
        for msg_text in map(''.join, zip(*[iter(text)] * min(len(text), length))):
            self.bot.send_message(
                chat_id,
                msg_text,
                disable_web_page_preview,
                reply_to_message_id,
                reply_markup,
                parse_mode,
                disable_notification)

        n = len(text) - (len(text) // length) * length

        if n > 0:
            self.bot.send_message(
                chat_id,
                text[-n:],
                disable_web_page_preview,
                reply_to_message_id,
                reply_markup,
                parse_mode,
                disable_notification)

    @staticmethod
    def markups(*args):
        markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
        if len(args):
            for i in args:
                if i is None:
                    return telebot.types.ReplyKeyboardRemove()

                if type(i) in (str, int):
                    markup.row(str(i))
                else:
                    markup.row(*i)

        else:
            return telebot.types.ReplyKeyboardRemove()
        return markup

    @staticmethod
    def keyboards(*args):
        if len(args):
            keyboard = telebot.types.InlineKeyboardMarkup(
                row_width=len(args[0]) if type(args[0]) != dict else 1
            )
            for i in args:
                if i is None:
                    return telebot.types.ReplyKeyboardRemove()

                if type(i) == dict:
                    keyboard.add(telebot.types.InlineKeyboardButton(
                        text=i['text'],
                        url=i['url'] if 'url' in i else None,
                        callback_data=i['data'] if 'data' in i else None,
                    ))
                else:
                    for j in i:
                        keyboard.add(telebot.types.InlineKeyboardButton(
                            text=j['text'],
                            url=j['url'] if 'url' in j else None,
                            callback_data=j['data'] if 'data' in j else None,
                        ))

        else:
            return telebot.types.ReplyKeyboardRemove()
        return keyboard

    def clear(self):
        os.system('cls' if os.name == 'nt' else 'clear')
        print(self.f.config['name'], self.f.config['version'])

    def run(self, restart=True):
        logging.info('The new process of the bot')

        try:
            self.bot.polling(none_stop=True)

        except telebot.apihelper.ApiException:
            if restart:
                threading.Thread(target=self.run).start()

    def new_message(self, message):
        user_id = message.from_user.id
        text = message.text
        user = self.get_user(user_id)
        page = user["page"]

        if page == "menu":
            if text == 'Сообщить о проблеме 🌱':
                new_page = 'title'
                self.ch_page(user_id, new_page)
                self.bot.send_message(user_id, self.strings[new_page], reply_markup=self.migration[new_page],
                                      parse_mode="Markdown")

            else:
                self.bot.send_message(user_id, self.strings[page], reply_markup=self.migration[page],
                                      parse_mode="Markdown")

        elif page == "title":
            if text == 'Отмена':
                new_page = 'menu'
                self.ch_page(user_id, new_page)
                self.bot.send_message(user_id, self.strings[new_page], reply_markup=self.migration[new_page],
                                      parse_mode="Markdown")

            else:
                user['title'] = text
                new_page = 'photo'
                self.ch_page(user_id, new_page)
                self.bot.send_message(user_id, self.strings[new_page], reply_markup=self.migration[new_page],
                                      parse_mode="Markdown")

        elif page == 'photo':
            if text == 'Пропустить':
                user['photo'] = None
                new_page = 'tag'
                self.ch_page(user_id, new_page)
                self.bot.send_message(user_id, self.strings[new_page], reply_markup=self.migration[new_page],
                                      parse_mode="Markdown")

            elif text == 'Отмена':
                new_page = 'menu'
                self.ch_page(user_id, new_page)
                self.bot.send_message(user_id, self.strings[new_page], reply_markup=self.migration[new_page],
                                      parse_mode="Markdown")

            else:
                self.bot.send_message(user_id, self.strings[page], reply_markup=self.migration[page],
                                      parse_mode="Markdown")

        elif page == 'tag':
            tags = {'Экология': 'Eco', 'Урбанистика': 'Urban', 'Общество': 'Social'}
            if text in tags:
                user['tag'] = tags[text]
                user['tag_table'] = text
                new_page = 'description'
                self.ch_page(user_id, new_page)
                self.bot.send_message(user_id, self.strings[new_page], reply_markup=self.migration[new_page],
                                      parse_mode="Markdown")

            elif text == 'Отмена':
                new_page = 'menu'
                self.ch_page(user_id, new_page)
                self.bot.send_message(user_id, self.strings[new_page], reply_markup=self.migration[new_page],
                                      parse_mode="Markdown")

            else:
                self.bot.send_message(user_id, self.strings[page], reply_markup=self.migration[page],
                                      parse_mode="Markdown")

        elif page == 'description':
            if text == 'Отмена':
                new_page = 'menu'
                self.ch_page(user_id, new_page)
                self.bot.send_message(user_id, self.strings[new_page], reply_markup=self.migration[new_page],
                                      parse_mode="Markdown")

            else:
                user['description'] = text
                new_page = 'address'
                self.ch_page(user_id, new_page)
                self.bot.send_message(user_id, self.strings[new_page], reply_markup=self.migration[new_page],
                                      parse_mode="Markdown")

        elif page == 'address':
            if text == 'Отмена':
                new_page = 'menu'
                self.ch_page(user_id, new_page)
                self.bot.send_message(user_id, self.strings[new_page], reply_markup=self.migration[new_page],
                                      parse_mode="Markdown")

            else:
                self.bot.send_message(user_id, self.strings[page], reply_markup=self.migration[page],
                                      parse_mode="Markdown")

        elif page == 'suggest':
            new_page = 'menu'
            self.ch_page(user_id, new_page)

            if text == 'Отправить':
                api.UserApi('http://urbanalerts.ml', 'tg').problem_new(
                    '', user['title'], user['photo'],
                    user['description'], user['tag'],
                    user['latitude'], user['longitude'],
                    '')

                user['photo'] = None
                user['photo_table'] = None

                self.bot.send_message(user_id, 'Успешно отправлено!', reply_markup=self.migration[new_page],
                                      parse_mode="Markdown")

            else:
                self.bot.send_message(user_id, self.strings[new_page], reply_markup=self.migration[new_page],
                                      parse_mode="Markdown")

        else:
            new_page = 'menu'
            self.ch_page(user_id, new_page)
            self.bot.send_message(
                user_id, "Что-то пошло не так.\nТы вернулся в меню.",
                reply_markup=self.migration[new_page]
            )


class FilesExchange:
    def __init__(self, config, users, strings):
        self.busy = False
        self.users = {}
        self.config = {}
        self.strings = {}

        self.boot(
            config=config,
            users=users,
            strings=strings
        )

    def boot(self, config, users, strings):
        if self.busy:
            return

        self.busy = True

        if not os.access('.dm', os.F_OK):
            os.mkdir('.dm')

        files = {
            'config':  json.dumps(config, ensure_ascii=False, indent=2),
            'users':   json.dumps(users, ensure_ascii=False, indent=2),
            'strings': json.dumps(strings, ensure_ascii=False, indent=2),
        }

        for file in files:
            filename = '%s.json' % file
            path = os.path.join('.dm', filename)

            if not os.access(path, mode=os.F_OK):
                with open(file=path, mode='w') as body:
                    body.write(files[file])

            with open(file=path, mode='r') as obj_raw:
                try:
                    setattr(self, file, json.loads(obj_raw.read()))

                except json.JSONDecodeError:
                    setattr(self, file, json.loads(files[file]))

        self.busy = False

    def update_users(self):
        with open(file=os.path.join('.dm', 'users.json'), mode='w') as file:
            file.write(json.dumps(self.users))


if __name__ == '__main__':
    bot = TelegramBot()
    bot.run()
