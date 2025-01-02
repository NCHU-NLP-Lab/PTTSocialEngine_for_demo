'''
Comment:
    type: str
    board: str
    article_id: str
    article_title: str
    user_id: str
    content: str
    comment_tag: str
    date: int
'''

class Comment:
    def __init__(self, type: str, board: str, article_id: str, article_title: str, user_id: str, content: str, comment_tag: str, date: int) -> None:
        # field
        self.type = type
        self.board = board
        self.article_id = article_id
        self.article_title = article_title
        self.user_id = user_id
        self.content = content
        self.comment_tag = comment_tag
        self.date = date