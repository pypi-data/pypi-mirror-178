import time
from typing import Union
from zaiclient.request.BaseEvent import BaseEvent


class PageViewEvent(BaseEvent):

    __default_event_type = "page_view"
    __default_item_id = "null"

    def __init__(
        self, user_id: str, page_type: str, timestamp: Union[float, None] = None
    ):

        if not isinstance(user_id, str):
            raise TypeError("User ID must be a string value.")

        if not isinstance(page_type, str):
            raise TypeError("Page Type must be a string value.")

        _item_ids = [self.__default_item_id]
        _event_values = [page_type]
        _timestamp = timestamp if timestamp is not None else time.time()

        super().__init__(
            user_id, _item_ids, _timestamp, self.__default_event_type, _event_values
        )
