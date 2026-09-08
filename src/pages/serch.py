import streamlit as st
import os
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
        SELECT id, name, text, image_path
        FROM mydb.evidences
        WHERE text LIKE %s
        ORDER BY id DESC
    """

    search_keyword = f"%{keyword}%"

    cursor.execute(sql, search_keyword)  # SQL文をデータベースに対して実行
    results = cursor.fetchall()  # execute() で検索した結果をすべて取得

    cursor.close()
    conn.close()

    st.subheader(f"「{keyword}」の検索結果")

    if results:
        for result in results:
            id, name, text, image_path = result

            with st.expander(f"{name}"):
                if image_path and os.path.exists(image_path):
                    st.image(image_path)
                else:
                    st.write("画像ファイルが存在しません。")

                st.write(text)

                # 削除ボタン
                if st.button("削除", key=f"delete_{id}"):
                    st.session_state[f"confirm_{id}"] = True

                # 削除確認
                if st.session_state.get(f"confirm_{id}", False):
                    st.warning("本当に削除しますか？")

                    if st.button("削除する", key=f"confirm_delete_{id}"):
                        conn = get_db_connection()
                        cursor = conn.cursor()

                        sql = """
                            DELETE FROM mydb.evidences
                            WHERE id = %s
                        """

                        cursor.execute(sql, (id,))
                        conn.commit()

                        # 画像ファイルも削除
                        if image_path and os.path.exists(image_path):
                            os.remove(image_path)

                        cursor.close()
                        conn.close()

                        st.success("削除しました")
                        st.rerun()

    else:
        st.info("検索結果がありません。")

else:
    st.write("左のサイドバーからキーワードを入力してください")