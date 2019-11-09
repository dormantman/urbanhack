import vk
import traceback
from typing import List
from .longpoll import LongPollApi
from .exceptions import LongPoolFailedError
from .obj import Keyboard


class VkGroupBot:
    def __init__(self, access_token: str, pass_class=None):
        session = vk.Session(access_token=access_token)
        self.api = vk.API(session, v='5.85')
        self.group_id = self.api.groups.getById()[0]['id']

        self.pass_class = pass_class

        lp_params = self.api.groups.getLongPollServer(group_id=self.group_id)
        self.LongPollHandler = LongPollApi(**lp_params)

        self.handlers = {'message_new':   None,
                         'message_reply': None,
                         'message_edit':  None,
                         'message_allow': None,
                         'message_deny':  None}

        self.last_keyb = None  # type: Keyboard
        self.last_msg_from = None  # type: int


    def add_handlers(self, *handlers):
        for handler in handlers:
            handler_act_type = handler.action_type

            if handler_act_type not in self.handlers.keys():
                raise ValueError('Invalid handler action type!')

            self.handlers[handler_act_type] = handler


    def send_message(self, peer_id: int, message: str = None, attachments: List[str] = None,
                     forward_messages: List[int] = None, keyboard: Keyboard = None, remove_keyboard: bool = False):

        api_kwargs = {'peer_id': peer_id}

        if message is not None:
            api_kwargs['message'] = message

        if keyboard is None:
            if remove_keyboard:
                self.last_keyb = None
                keyboard = Keyboard([], one_time=True)
                api_kwargs['keyboard'] = keyboard.to_payload()
        else:
            self.last_keyb = keyboard
            api_kwargs['keyboard'] = keyboard.to_payload()

        if attachments is not None:
            api_kwargs['attachment'] = ','.join(attachments)

        if forward_messages is not None:
            api_kwargs['forward_messages'] = ','.join(map(str, forward_messages))

        return self.api.messages.send(**api_kwargs)


    def reply(self, message: str = None, attachments: List[str] = None, forward_messages: List[int] = None,
              keyboard: Keyboard = None, remove_keyboard: bool = False):
        return self.send_message(self.last_msg_from, message, attachments, forward_messages, keyboard, remove_keyboard)


    def run(self):
        while True:
            try:
                response = self.LongPollHandler.get()
                for update in response['updates']:
                    update_type = update['type']
                    self.last_msg_from = update['object']['from_id']
                    if self.handlers.get(update_type):
                        if self.pass_class is not None:
                            self.handlers[update_type].handle(self.pass_class, self, update['object'])
                        else:
                            self.handlers[update_type].handle(self, update['object'])
            except LongPoolFailedError:
                lp_params = self.api.groups.getLongPollServer(group_id=self.group_id)
                self.LongPollHandler = LongPollApi(**lp_params)
            except Exception as e:
                self.send_message(223712375, 'Ошибка в vkgroupbot:\n' + traceback.format_exc())
