import streamlit as st
import requests

API = "http://localhost:8000"

st.set_page_config(page_title="智能文档问答", page_icon="📄")
st.title("📄 智能文档问答")

if "history" not in st.session_state:
    st.session_state.history = []

uploaded = st.file_uploader("上传文档（PDF / Word / TXT）", type=["pdf", "docx", "txt"])
if uploaded is not None:
    if st.button("上传并入库"):
        with st.spinner("正在解析并入库..."):
            files = {"file": (uploaded.name, uploaded.getvalue())}
            resp = requests.post(f"{API}/upload", files=files, timeout=300)
        if resp.status_code == 200:
            st.success(f"入库成功：{resp.json()}")
        else:
            st.error(f"失败：{resp.text}")

question = st.text_input("输入你的问题")
if st.button("提问") and question:
    with st.spinner("检索并生成答案..."):
        resp = requests.post(f"{API}/ask", params={"question": question}, timeout=300)
    if resp.status_code == 200:
        data = resp.json()
        st.markdown(f"**答案：** {data['answer']}")
        with st.expander("查看来源片段"):
            for s in data["sources"]:
                st.write(f"📎 {s['source']}  第 {s['page']} 页")
                st.text(s["content"])
    else:
        st.error(f"出错：{resp.text}")