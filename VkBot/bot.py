from typing import Dict
from vkgroupbot.bot import VkGroupBot
from vkgroupbot.handlers import MessageHandler, ConversationHandler
from vkgroupbot.obj import Update, Keyboard
from api import UserApi

TEST = False
__site__ = 'urbanalerts.ml'
__version__ = '0.3.7'

class ConvIds:
    start = 0
    main = 1
    new_problem = 2
    account = 3


class Keyb:
    start = Keyboard([[('Перейти в главное меню', 1)]])
    menu = Keyboard([[('Добавить проблему', 1), ('Аккаунт', 1)], [('Помощь', 2)], [('О приложении Urban Alerts', 2)]])
    skip = Keyboard([[('Пропустить', 1)]])
    back = Keyboard([[('Назад', 1)]])
    cancel = Keyboard([[('Отменить', 1)]])
    help = Keyboard([[('Помощь', 2), ('Отмена', 3)]], one_time=True)
    tags = Keyboard([[('Экология', 1), ('Урбанистика', 1)], [('Социальные проблемы', 1)], [('Как определить тип?', 2)]])
    coords = Keyboard([[('Как отправить геопозицию?', 2)]])
    apply = Keyboard([[('Подтвердить', 1), ('Отменить', 1)]])
    account_main = Keyboard([[('Зарегистрироваться', 1), ('Авторизироваться', 1)], [('Назад', 1)]])


class RepliesEng:
    start_on = 'Start hello'
    main_menu = 'Main menu'
    back_main_menu = 'Returning to main menu'
    press_keyb = 'Unknown message. Please, use keyboard buttons'
    new_problem_title = 'New problem? Title it'
    new_problem_photo = 'Send photo of your problem'
    new_problem_descr = 'Describe your problem in a few words'
    new_problem_coord = 'Send me geo position of your problem'
    new_problem_settg = 'Choose one tag for your problem from given ones'
    new_problem_nottg = 'Please, choose one tag from given'
    new_problem_apply = 'Check your problem. If its correct, send it, or cancel\nTitle: {}\nDescription: {}\nPhoto:'
    new_problem_final_ok = 'Your problem has been sent to server'
    new_problem_final_er = 'Error occured while sending problem to server'
    new_problem_final_not_keyb = 'Please, choose press one button - accept or decline'

    new_problem_photo_skipped = 'You dont choose any problem photo'
    new_problem_photo_too_many = 'You should send me only 1 photo [also you can skip this step]'
    new_problem_taghelp = 'Eco - one, Urban - second, Human - third'

    account_main = 'This is account settings page'
    account_regr = 'You can register to connect your profile in different platforms (vk, telegram, alice, web)'
    account_auth = 'Copy your token from web-site and send it to me'
    account_sign_in = 'Sign it TODO'
    account_sign_up = 'Sign up TODO'


class Replies:
    start_on = 'Добрый день. Вас приветсвтует Urban Alerts Bot. С моей помощью вы сможете быстро сообщать ' \
               'о различных проблемах в Вашем городе. Возникают вопросы по функционалу? ' \
               'Напишите мне "Помощь" или нажмите на одноимённую кнопку. Также Вы можете посетить сайт ' \
               f'{__site__}\n' \
               f'&#10071;Внимание&#10071;\n' \
               f'Иногда вк не подгружает клавиатуру. Обновите страницу, если вы не видите кнопок'
    main_menu = 'Главное меню'
    back_main_menu = 'Возврат назад в главное меню'
    press_keyb = 'Пожалуйста, воспользуйтесь виртуальной клавиатурой для ответа'
    newprob_title = 'Сообщение о новой проблеме\nВведите заголовок для проблемы'
    newprob_photo = 'Отправьте фотографию проблемы. Вы можете пропустить этот шаг'
    newprob_descr = 'Опишите несколькими словами Вашу проблему'
    newprob_coord = 'Отметьте расположение проблемы на карте'
    newprob_settg = 'Выберите тип проблемы'
    newprob_apply = 'Проверьте правильность ввода. ' \
                    'Если все верно, Я отправлю данные о проблеме в систему. ' \
                    'Если вы не хотите изменить описание пробемы, нажмите на кнопку "Отменить" и ' \
                    'повторите ввод\nЗаголовок: {}\nОписание: {}\nФотография:'
    newprob_final_sending = 'Отправляю данные на сервер...'
    newprob_final_canceld = 'Отправка проблемы отменена. Возврат в главное меню'
    newprob_final_ok = 'Ваша проблема была успешно добавлена в базу данных.'
    newprob_final_er = 'Ошибка отправки проблемы. Пожалуйста, обратитесь к разработчикам'

    newprob_photo_too_many = 'На этом шаге Вам нужно отправить только 1 фотографию проблемы. ' \
                             'Вы так же можете пропустить этот шаг'
    newprob_coord_help = 'Чтобы отправить координаты, нажмите на скрепку возле поля, где вы набираете ' \
                         'сообщения, затем выберите тип "Карта". Двигайте метку, чтобы уточнить геопозицию.'
    newprob_settg_help = 'Экология - К этому типу можно отнести несанкционированные свалки, ' \
                         'сливные трубы в реки и озера и другие проблемы, связанные с природой\n' \
                         'Урбанистика - Плохой асфальт? Ямы на дорогах? Большие грязные лужи, которые постоянно ' \
                         'приходится обходить? Такие проблемы относятся к этому типу\n' \
                         'Социальные - Помощь нуждающимся людям, попавшим в беду; проблемы, связанные с ' \
                         'бездомными (как людьми, так и животными) - все это принадлежит этому типу.'

    account_main = 'Настройки аккаунта'
    account_regr = f'Вы можете зарегистрироваться на сайте {__site__}, ' \
                   f'чтобы связать аккаунты на разных платформах (Вк, Телеграмм, Яндекс Алиса)'
    account_auth = 'Для авторизации вам нужно скопировать токен из личного кабинета на сайте ' \
                   f'{__site__} и отправить его сообщением.'
    account_sign_in = 'Функция в разработке, возвращаемся назад'
    account_sign_up = 'Функция в разработке, возвращаемся назад'

    menu_help = '&#10067; Помощь\n' \
                'Мы создали UrbanAlerts именно для того, чтобы контролировать экологические ' \
                'службы и помогать вам добиваться улучшений. Приложение посвященное ' \
                'развитию городской системы оповещения.\n' \
                'Бот имеет интуитивно понятный интерфейс. Основное взаимодействие осуществляется ' \
                'посредством элементов управления.'
    menu_about = f'Urban Alerts Vk Bot v{__version__}\n' \
                 f'No any rights reserved, no sleep for 2 days, 10 doshiks have been eaten, ' \
                 f'great expirience & fun. #Urbanhack'


class BotMethods:
    def __init__(self):
        self.users_data = {}
        self.user_api = UserApi('http://urbanalerts.ml', 'vk')


    def start(self, bot: VkGroupBot, update: Update):
        if update.message == '!':
            bot.reply('Restarting dialog', remove_keyboard=True)
            return ConvIds.start

        user_id = update.from_id
        self.users_data[user_id] = {'state': ''}

        if bot.last_keyb is not None:
            row, col = bot.last_keyb.was_pressed(update.message)
            if row != -1:
                bot.reply(Replies.main_menu, keyboard=Keyb.menu)
                return ConvIds.main

        bot.reply(Replies.start_on, keyboard=Keyb.start)
        return ConvIds.start


    def main_menu(self, bot: VkGroupBot, update: Update):
        user_id = update.from_id
        self.users_data[user_id] = {'state': ''}

        row, col = Keyb.menu.was_pressed(update.message)

        if (row, col) == (0, 0):
            return self.new_problem(bot, update)
        elif (row, col) == (0, 1):
            return self.account(bot, update)
        elif (row, col) == (1, 0):
            bot.reply(Replies.menu_help)
        elif (row, col) == (2, 0):
            bot.reply(Replies.menu_about)
        else:
            bot.reply(Replies.press_keyb)

        return ConvIds.main


    def new_problem(self, bot: VkGroupBot, update: Update):
        user_id = update.from_id

        if self.users_data[user_id].get('data') is None:
            self.users_data[user_id] = {'state': 'title',
                                        'data':  {'title':    '',
                                                  'photo':    '',
                                                  'photo_id': '',
                                                  'descr':    '',
                                                  'coord':    '',
                                                  'tag':      ''}}
            bot.reply(Replies.newprob_title, remove_keyboard=True)
            return ConvIds.new_problem

        state = self.users_data[user_id]['state']

        if state == 'title':
            self.users_data[user_id]['data']['title'] = update.message
            bot.reply(Replies.newprob_photo, keyboard=Keyb.skip)
            state = 'photo'

        elif state == 'photo':
            if len(update.attachments) == 0:
                row, col = bot.last_keyb.was_pressed(update.message)
                if row == -1:
                    bot.reply(Replies.newprob_photo_too_many)
                    return ConvIds.new_problem
                self.users_data[user_id]['data']['photo'] = ''
            elif len(update.attachments) == 1:
                if update.attachments[0]['type'] == 'photo':
                    photo = update.attachments[0]['photo']
                    biggest_photo = sorted(photo['sizes'], key=lambda x: -x['width'])[0]['url']
                    self.users_data[user_id]['data']['photo'] = biggest_photo
                    # photo_id = f'photo{photo["owner_id"]}_{photo["id"]}_{photo["access_key"]}'
                    photo_id = update.id
                    self.users_data[user_id]['data']['photo_id'] = photo_id
                else:
                    bot.reply(Replies.newprob_photo_too_many)
                    return ConvIds.new_problem
            else:
                bot.reply(Replies.newprob_photo_too_many)
                return ConvIds.new_problem

            bot.reply(Replies.newprob_descr, remove_keyboard=True)
            state = 'descr'

        elif state == 'descr':
            self.users_data[user_id]['data']['descr'] = update.message
            bot.reply(Replies.newprob_coord, keyboard=Keyb.coords)
            state = 'coord'

        elif state == 'coord':
            row, col = bot.last_keyb.was_pressed(update.message)
            if (row, col) == (0, 0):
                bot.reply(Replies.newprob_coord_help)
            else:
                if update.geo:
                    self.users_data[user_id]['data']['coord'] = (update.geo_latitude, update.geo_longitude)
                    bot.reply(Replies.newprob_settg, keyboard=Keyb.tags)
                    state = 'tag'
                else:
                    bot.reply(Replies.newprob_coord)

        elif state == 'tag':
            if bot.last_keyb:
                row, col = bot.last_keyb.was_pressed(update.message)
                if row in [0, 1]:
                    self.users_data[user_id]['data']['tag'] = bot.last_keyb.button_rows[row][col][0]

                    problem_data = self.users_data[user_id]['data']
                    problem_str = Replies.newprob_apply.format(problem_data["title"], problem_data["descr"])
                    if problem_data['photo'] != '':
                        bot.reply(problem_str, forward_messages=[self.users_data[user_id]['data']['photo_id']],
                                  keyboard=Keyb.apply)
                    else:
                        problem_str += ' Не загружена'
                        bot.reply(problem_str, keyboard=Keyb.apply)
                    state = 'apply'
                elif (row, col) == (2, 0):
                    bot.reply(Replies.newprob_settg_help)
                    return ConvIds.new_problem
                else:
                    bot.reply(Replies.press_keyb)

        elif state == 'apply':
            row, col = bot.last_keyb.was_pressed(update.message)
            if (row, col) == (0, 0):
                # bot.reply(Replies.newprob_final_sending)
                data = self.users_data[user_id]['data']
                # = API REQUEST = #
                tag_transformed = {'Экология':            'Eco',
                                   'Урбанистика':         'Urban',
                                   'Социальные проблемы': 'Social'}[data['tag']]

                self.user_api.problem_new(token='tg:123',
                                          title=data['title'],
                                          photo=data['photo'],
                                          description=data['descr'],
                                          tag=tag_transformed,
                                          latitude=data['coord'][0],
                                          longitude=data['coord'][1])
                # = =========== = #
                bot.reply(Replies.newprob_final_ok, keyboard=Keyb.menu)
                return ConvIds.main
            elif (row, col) == (0, 1):
                bot.reply(Replies.newprob_final_canceld, keyboard=Keyb.menu)
                return ConvIds.main
            else:
                bot.reply(Replies.press_keyb)

        self.users_data[user_id]['state'] = state
        return ConvIds.new_problem


    def account(self, bot: VkGroupBot, update: Update):
        user_id = update.from_id

        if self.users_data[user_id]['state'] == '':
            self.users_data[user_id]['state'] = 'account'
            bot.reply(Replies.account_main, keyboard=Keyb.account_main)
            return ConvIds.account

        state = self.users_data[user_id]['state']

        if state == 'account':
            row, col = bot.last_keyb.was_pressed(update.message)
            if (row, col) == (0, 0):
                state = 'sign up'
                bot.reply(Replies.account_regr, keyboard=Keyb.back)
            elif (row, col) == (0, 1):
                state = 'sign in'
                bot.reply(Replies.account_auth, keyboard=Keyb.back)
            elif (row, col) == (1, 0):
                bot.reply(Replies.back_main_menu, keyboard=Keyb.menu)
                return ConvIds.main
            else:
                bot.reply(Replies.press_keyb)

        elif state == 'sign in':
            bot.reply(Replies.account_sign_in, keyboard=Keyb.account_main)
            state = 'account'

        elif state == 'sign up':
            bot.reply(Replies.account_sign_in, keyboard=Keyb.account_main)
            state = 'account'

        self.users_data[user_id]['state'] = state
        return ConvIds.account


def main():
    if TEST:
        access_token = 'f84062d7a9f626cca4d13ec2e5aed84e3aff576e5a03af5e44c64d687866f445f82ff75ccffca9d0c5c8b'
    else:
        access_token = 'e8f214c46caf96bff18f19c3bd361fbcc609ff022d8d239f880d2001df99f8268cc1a078f59d7de631dea'

    bot_methods = BotMethods()

    bot = VkGroupBot(access_token=access_token)

    ch = ConversationHandler(MessageHandler(bot_methods.start),
                             {ConvIds.start:       MessageHandler(bot_methods.start),
                              ConvIds.main:        MessageHandler(bot_methods.main_menu),
                              ConvIds.new_problem: MessageHandler(bot_methods.new_problem),
                              ConvIds.account:     MessageHandler(bot_methods.account)})
    bot.add_handlers(ch)

    print('### Bot Initialized ###')
    bot.run()


if __name__ == '__main__':
    main()
