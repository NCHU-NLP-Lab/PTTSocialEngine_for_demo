'''
Article:
    # field -> 變數
    type: str
    article_id: str
    article_title: str
    user_id: str
    user_nickname: str
    board: str
    content: str
    date: int
    ip: str
    tag: str # 問卦，新聞，爆掛...
    comments: [Comment]

    def get_all_comment_content(self) -> list:
        return []
'''
from entity.comment import Comment
import requests
from text_cleaner.text_cleaner import Text_Cleaner

class Article:
    def __init__(self, type: str, artcle_id: str, article_title: str, user_id: str, user_nickname: str,
                board: str, content: str, date: int, ip: str, tag: str = None) -> None:
        # field
        self.type = type
        self.artcle_id = artcle_id
        self.article_title = article_title
        self.user_id = user_id
        self.user_nickname = user_nickname
        self.board = board
        self.content = content
        self.date = date
        self.ip = ip
        self.tag = tag
        self.comments = self.__get_all_comment()
        self.tc = Text_Cleaner()

    def __get_all_comment(self) -> list[Comment]:
        all_comment = []
        url = f'http://ptt-search.nlpnchu.org/api/GetCommentByArticle?article_id={self.artcle_id}'
        
        print(url)
        res = requests.get(url, {'Accept': 'application/json'})
        res = res.json()
        for hit in res['hits']:
            all_comment.append(Comment(type=hit['_source']['type'],
                                       board=hit['_source']['board'],
                                       article_id=hit['_source']['article_id'],
                                       article_title=hit['_source']['article_title'],
                                       user_id=hit['_source']['user_id'],
                                       content=hit['_source']['content'],
                                       comment_tag=hit['_source']['comment_tag'],
                                       date=hit['_source']['date']))
        return all_comment
    
    def get_all_comment_list(self) -> list[str]:
        all_comment = []
        # url = f'http://ptt-search.nlpnchu.org/api/GetCommentByArticle?article_id={self.artcle_id}'
        
        # print(url)
        # res = requests.get(url, {'Accept': 'application/json'})
        # res = res.json()
        for comment in self.comments:
            all_comment.append(self.tc.clean_URL(comment.content))
        return all_comment

    