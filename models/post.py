from datetime import datetime


class Post:
    def __init__(self, post_id: int, user_id: int, content: str, date_created: datetime):
        self.post_id = post_id
        self.user_id = user_id
        self.content = content
        self.date_created = date_created
