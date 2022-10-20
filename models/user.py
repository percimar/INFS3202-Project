from datetime import datetime
from typing import Optional


class User:
    def __init__(self, user_id: int, user_name: str, last_login: Optional[datetime] = None):
        self.user_id = user_id
        self.user_name = user_name
        self.last_login = last_login
