from entity.resultDTO import ResultDTO
from openai import OpenAI
import os
from dotenv import load_dotenv
from article_fetcher.article_fetcher import Article_Fetcher
from text_cleaner.text_cleaner import Text_Cleaner
from db.db_connect import result_collection

class Analyzer:
    # This global variable is to save GPT's response. Use UUID check response,
    response_db = {} # {UUID : Response}
    
    def __init__(self) -> None:
        load_dotenv()
        self.client = OpenAI(
            api_key=os.getenv("OPENAI_API_KEY"),
        )
        self.current_directory = os.getcwd()
        self.comment_fetcher_model = os.getenv("COMMENT_FETCHER_MODEL")
        self.summary_model = os.getenv("SUMMARY_MODEL")
        self.AF = Article_Fetcher()
        self.TC = Text_Cleaner()
        self.check_folder()
        self.delete_txt()

    def delete_txt(self):
        with open("./result/prompt_summary.txt", "w") as file:
            file.write("")
        with open("./result/GPT_report.txt", "w") as file:
            file.write("")

    def check_folder(self):
        # 檢查 result 資料夾是否存在
        result_folder = "result"
        if not os.path.exists(result_folder):
            # 如果不存在，則創建資料夾
            os.makedirs(result_folder)
            print(f"已創建 {result_folder} 資料夾")
        else:
            print(f"{result_folder} 資料夾已存在")

    # Generate response and save to text file
    def prompt_input(self, system: str, prompt: str):
        print(f"=============== Call {self.comment_fetcher_model} ===============")
        completion = self.client.chat.completions.create(
            model=self.comment_fetcher_model,
            messages=[
                {
                    "role": "system",
                    "content": system,
                    "role": "user",
                    "content": prompt,
                }
            ],
            temperature=0,
            max_tokens=2048,
        )
        print(completion.choices[0].message.content)

        with open("./result/prompt_summary.txt", "a") as file:
            file.write(completion.choices[0].message.content + "\n")

        return completion.choices[0].message.content

    def prompt_report(self, system: str, prompt: str):
        print(f"=============== Call {self.summary_model} ===============")
        completion = self.client.chat.completions.create(
            model=self.summary_model,
            messages=[
                {
                    "role": "system",
                    "content": system,
                    "role": "user",
                    "content": prompt,
                }
            ],
            temperature=1,
        )
        print(completion.choices[0].message.content)

        with open("./result/GPT_report.txt", "a") as file:
            completion.choices[0].message.content = completion.choices[0].message.content.replace("/\n/g", "<br>")
            file.write(completion.choices[0].message.content + "\n")

        return completion.choices[0].message.content

    def prompt_analyzer(
        self, keyword: str, tag: str, K: int, size: int, start: int, end: int, uuid: str
    ):
        print(f"------------------- start of {uuid} session.")
        contents = []
        comments = []
        # Read article's summary to list
        content_and_comment = ""
        content_and_comment_list = []

        # Create result model
        result = ResultDTO(
            result="initial_result",
            keyword=keyword,
            date=str(start) + '-' + str(end),
            session_id=uuid
        )

        # Retrieve related article
        prompt_AF = self.AF.get_article_by_keyword(
            keyword=keyword, tag=tag, K=K, size=size, start=start, end=end
        )

        # Extract all content and content
        for article in prompt_AF:
            article.content = self.TC.clean_text(article.content)
            contents.append(article.content)
            comments.append(article.get_all_comment_list())

        # Generate article's summary to text file
        for i in range(len(contents)):
            prompt = (
                """現在給你[文章]以及[留言]，請對文章做200字以內總結\n並且條列式列出你覺得跟這篇文章內容有高度相關的留言(最多100則留言)。回復格式為\n(文章):\n(留言):\n[文章]\n"""
                + str(contents[i])
                + "\n[留言]\n"
                + str(comments[i])
            )
            content_and_comment_list.append(self.prompt_input("你是一位在臺灣的資深時事分析專家", prompt))

        for content in content_and_comment_list:
            content_and_comment += content

        # Generate report
        prompt ="""你是一位時事分析專家，我會給你幾篇(文章)以及(留言)，請綜合分析這些留言對事件的風向看法，以及留言對事件的觀點為何?\n給出一個對事件總結的標題，以及做一個[表格]分析，[表格]以markdown language呈現，
(1)列出事件的觀點\n
(2)對此觀點的詳細描述或是依據\n
(3)留言對此觀點的看法(每個觀點最多10則留言)\n""" + content_and_comment
        res = self.prompt_report("你是一位在台灣的資深時事分析專家", prompt)
        
        print(f"------------------- report generate done.")
        result.result = res

        result_collection.insert_one(
            result.dict(by_alias=True, exclude=["id"])
        )
        print(f"------------------- save {result.session_id} to db done.")
