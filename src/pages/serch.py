import streamlit as st
from db import get_db_connection

st.title("検索ページ")

# サイドバー
with st.sidebar:
    st.header("検索")

    keyword = st.text_input(
        "キーワードを入力してください"
    )

if keyword:
    conn = get_db_connection()
    cursor = conn.cursor()

    sql = """
        SELECT id, name, text
        FROM mydb.evidences
        WHERE  text LIKE %s
        ORDER BY id DESC
    """

    search_keyword = f"%{keyword}%"

    cursor.execute(sql, search_keyword)#１つの検索したい文字をtextで知らばる
    results = cursor.fetchall()#検索で見つかったででデータを全部取得

    cursor.close()
    conn.close()

    st.subheader(f"「{keyword}」の検索結果")

    if results:
        for result in results:
            id, name, text = result

            with st.expander(f"{name}"):
                st.write(text)#
    else:
        st.info("検索結果がありません。")

else:
    st.write("左のサイドバーからキーワードを入力してください")