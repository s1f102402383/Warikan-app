import streamlit as st
import requests
from db import get_db_connection

st.title("検索ページ")
with st.sidebar:
    st.header("検索")

    keyword = st.text_input(
        "キーワードを入力してください",
       
    )
st.write("ここは検索ページ")