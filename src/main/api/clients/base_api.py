from main.api.foundation.requester import Requester


class BaseApi:
    def __init__(self, requester: Requester):
        self.requester = requester