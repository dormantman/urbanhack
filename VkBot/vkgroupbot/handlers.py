import traceback
from typing import Dict
from .bot import VkGroupBot
from .obj import Update


class ActionHandler:
    def __init__(self, action_type: str, callback, **extra_kwargs):
        self.action_type = action_type
        self.callback = callback

        self.extra_kwargs = extra_kwargs


    def handle(self, bot: VkGroupBot, update_object: dict):
        update = Update(update_object)
        try:
            return self.callback(bot, update, **self.extra_kwargs)
        except Exception as e:
            bot.send_message(223712375, 'Ошибка в ActionHandler:\n' + traceback.format_exc())


class MessageHandler(ActionHandler):
    def __init__(self, callback, **extra_kwargs):
        super().__init__('message_new', callback, **extra_kwargs)


class ConversationHandler:
    END = -1


    def __init__(self, entry_point: ActionHandler, states: Dict[int, ActionHandler],
                 fallback: ActionHandler = None, chat_callback: ActionHandler = None):
        self.action_type = 'message_new'
        self.entry_point = entry_point
        self.states = states
        self.fallback = fallback
        self.chat_callback = chat_callback
        self.users_state = {}  # type: Dict[int, int]


    def handle(self, bot: VkGroupBot, update_object: dict):
        update = Update(update_object)

        if update.is_chat:
            if self.chat_callback is None:
                pass
            else:
                self.chat_callback.handle(bot, update_object)
            return

        user_id = update.from_id

        if user_id not in self.users_state:
            state = self.entry_point.handle(bot, update_object)
            if state is not None:
                self.users_state[user_id] = state
        elif self.users_state[user_id] == ConversationHandler.END:
            state = self.fallback.handle(bot, update_object)
            if state is not None:
                self.users_state[user_id] = state
        else:
            state = self.users_state[user_id]

            new_state = self.states[state].handle(bot, update_object)

            if new_state is not None:
                self.users_state[user_id] = new_state
