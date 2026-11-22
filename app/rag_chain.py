from langchain_openai import ChatOpenAI
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
from app.config import settings

PROMPT_TEMPLATE = """你是一个严谨的文档问答助手。请仅根据以下上下文回答问题，并在关键结论后标注来源。
如果上下文中没有相关信息，回答“根据已上传的文档，无法回答该问题”。

上下文：
{context}

问题：{question}

答案："""

def build_qa_chain(vectorstore):
    llm = ChatOpenAI(
        model=settings.LLM_MODEL,
        temperature=0,
        api_key=settings.OPENAI_API_KEY,
        base_url=settings.OPENAI_BASE_URL,
    )
    prompt = PromptTemplate(
        template=PROMPT_TEMPLATE,
        input_variables=["context", "question"],
    )
    return RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=vectorstore.as_retriever(search_kwargs={"k": 4}),
        return_source_documents=True,
        chain_type_kwargs={"prompt": prompt},
    )
