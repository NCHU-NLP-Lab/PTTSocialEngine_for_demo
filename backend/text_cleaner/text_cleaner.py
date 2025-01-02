import re
class Text_Cleaner:
    def __init__(self):
        # loading 過濾詞表 stop_words.txt
        #self.stop_words = self.load_stop_words('./text_cleaner/stop_words.txt')
        #self.stop_words=['媒體','中央社','中時','民視','三立','自由時報','科技新報','記者','編輯','報導','新聞','來源','即時中心','示意圖']
        self.stop_words = self.load_stop_words("./text_cleaner/stop_words.txt")
        # url regular expression
        self.url_pattern = r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'

        #格式
        '''八卦新聞版規格式 (不一定有)
        1.媒體來源:
        2.記者署名:
        3.完整新聞標題:
        4.完整新聞內文:
        5.完整新聞連結 (或短網址):
        6.備註: 
        '''
        self.uniform = ['媒體來源','記者署名','完整新聞標題','完整新聞內文','完整新聞連結 (或短網址)不可用YAHOO、LINE、MSN等轉載媒體','※ 一個人一天只能張貼一則新聞(以天為單位)，被刪或自刪也算額度內，超貼者水桶，請注意','※ 備註請勿張貼三日內新聞(包含連結、標題等)']
    def load_stop_words(self, file_path):
        with open(file_path, 'r', encoding='utf-8') as file:
            stop_words = set(word.strip() for word in file)
        return stop_words
    def clean_URL(self,input_text : str):
        String_without_URL = re.sub(self.url_pattern, '', input_text)
        return String_without_URL   
    def clean_text(self, input_text : str):
        #print("------processing input article------")
        
        #刪除備註、簽名檔(包含\n的多行) -> (6.){(備註)|(--簽名檔\n\n\n\n....--)}
        cleaned_text = re.sub(rf'(\d?\.?)((備註)|(--\n)).*','',input_text,flags=re.DOTALL)
        #print(f"刪除備註={cleaned_text}\n")
        #刪除url
        #cleaned_text = re.sub(self.url_pattern, '', cleaned_text) 
        cleaned_text = self.clean_URL(cleaned_text)
        #刪除八卦新聞格式 -> (1.)(媒體來源)(:)
        gossiping_uniform='|'.join(re.escape(word) for word in self.uniform)
        gossiping_uniform_pattern=f'(\d?\.?)({gossiping_uniform})(：|:).*'
        cleaned_text = re.sub(gossiping_uniform_pattern,'',cleaned_text)
        #print(f"刪除格式={cleaned_text}\n")
        #刪除stopwords
        for word in self.stop_words:
            cleaned_text = cleaned_text.replace(word, '')
        #print(f"result={cleaned_text}\n")
        #print("-------saved cleaned_article.txt------")
        return cleaned_text
