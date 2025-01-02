# PTTSocialEngine
---
## 啟動程式
1. 將 .env.example 複製一份，並改名成 .env，將以下內容填入
``` bash
MONGODB_URL=YOUR_MONGO_URL
OPENAI_API_KEY=YOUR_API_KEY
COMMENT_FETCHER_MODEL=gpt-4o-mini
SUMMARY_MODEL=gpt-4o-mini
```
2. 跑以下指令
``` bash
pip install -r requirements.txt
```
3. 使用 uvicorn 啟動 fastAPI (Hot reload)
```bash
cd backend
uvicorn main:app --reload
```

---
## Swagger Doc：localhost:8000/docs
