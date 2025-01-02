import requests
import json
from entity.article import Article
import re

class Article_Fetcher:
    def __init__(self) -> None:
        self.base_url = 'http://ptt-search.nlpnchu.org/api/'
        self.headers = {'Accept': 'application/json'}

    def get_article_by_keyword(self, keyword: str, tag: str, K: int, size: int, start: int, end: int) -> list[Article]:
        type = 'article' # for query only article from elasticsearch return
        count_for_K = 0
        artile_array = []
        
        if start is None or end is None:
            url = self.base_url + f'GetArticleByType?content={keyword}&type={type}&size={size}'
        else:
            url = self.base_url + f'GetArticleByType?start={start}&end={end}&content={keyword}&type={type}&size={size}'

        print(url)
        res = requests.get(url, headers=self.headers)
        res = res.json()
        
        for hit in res['hits']:
            if count_for_K >= K:
                break
            article_title = hit['_source']['article_title']
            title_re_exist = re.search(r'Re:', article_title)
            article_tag = article_title[article_title.find('[')+1:article_title.find(']')]
            if tag is not None and article_tag == tag and not title_re_exist:
                article = Article(type=hit['_source']['type'],
                        artcle_id=hit['_source']['article_id'],
                        article_title=hit['_source']['article_title'],
                        user_id=hit['_source']['user_id'],
                        user_nickname=hit['_source']['user_nickname'],
                        board=hit['_source']['board'],
                        content=hit['_source']['content'],
                        date=hit['_source']['date'],
                        tag=article_tag,
                        ip=hit['_source']['ip']
                        )
                count_for_K += 1
                artile_array.append(article)
        
        return artile_array
        