# 基于 RAG 的智能文档问答系统

基于 RAG 架构的本地知识库问答系统，支持 PDF / Word / TXT 文档解析。

## 技术栈
- 后端：Python / FastAPI / LangChain / ChromaDB
- 前端：Streamlit
- 模型：DeepSeek (LLM) + 阿里云百炼 (Embedding)

## 快速启动
1. 克隆项目：`git clone https://github.com/你的用户名/rag-doc-qa.git`
2. 创建虚拟环境：`python -m venv venv`
3. 激活环境：`venv\Scripts\activate` (Windows)
4. 安装依赖：`pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple`
5. 复制 `.env.example` 为 `.env`，填入你的 API Key。
6. 启动后端：`python -m uvicorn main:app --reload --port 8000`
7. 启动前端：`streamlit run frontend.py`