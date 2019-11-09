import json
from typing import List, Tuple


class Update:
    def __init__(self, params: dict):
        self.date = params['date']            # type: int
        self.from_id = params['from_id']      # type: int
        self.id = params['id']                # type: int
        self.out = params['out']              # type: int
        self.peer_id = params['peer_id']      # type: int
        self.message = params['text']         # type: str
        self.important = params['important']  # type: bool
        self.random_id = params['random_id']  # type: int
        self.is_hidden = params['is_hidden']  # type: bool
        self.attachments = params['attachments']     # type: list
        self.fwd_messages = params['fwd_messages']   # type: list
        self.is_chat = self.from_id != self.peer_id  # type: bool
        self.conversation_message_id = params['conversation_message_id']  # type: int

        if params.get('geo') is not None:
            self.geo = True
            self.geo_latitude = str(params['geo']['coordinates']['latitude'])
            self.geo_longitude = str(params['geo']['coordinates']['longitude'])
        else:
            self.geo = False
            self.geo_latitude = None
            self.geo_longitude = None


class Keyboard:
    def __init__(self, buttons: List[List[Tuple[str, int]]], one_time: bool = False):
        self.button_rows = buttons
        self.one_time = one_time


    def to_payload(self) -> str:
        """
        Button types (https://vk.com/dev/bots_docs_3?f=4.1.+Подключение):
            1. primary — синяя кнопка, обозначает основное действие. #5181B8
            2. default — обычная белая кнопка. #FFFFFF
            3. negative — опасное действие, или отрицательное действие (отклонить, удалить и тд). #E64646
            4. positive — согласиться, подтвердить. #4BB34B
        :return:
        """
        colors = {1: 'primary', 2: 'default', 3: 'negative', 4: 'positive'}
        buttons = []
        index = 0
        for row in self.button_rows:
            btn_row = []
            for btn_text, btn_type in row:
                btn_row.append({
                    "action": {
                        "type":    "text",
                        "payload": '{\"button\": \"' + str(index) + '\"}',
                        "label":   btn_text},
                    "color":  colors[btn_type]})
                index += 1
            buttons.append(btn_row)

        js = {"one_time": self.one_time, "buttons": buttons}

        return json.dumps(js, ensure_ascii=False)


    def was_pressed(self, message: str) -> Tuple[int, int]:
        for row_ind, row in enumerate(self.button_rows):
            for col_ind, btn in enumerate(row):
                if btn[0] == message:
                    return row_ind, col_ind

        return -1, -1
