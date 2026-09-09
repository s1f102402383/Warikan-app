import streamlit as st
import os
from db import get_db_connection


st.title("検索ページ")


# ==========================================
# 旅行を取得
# ==========================================

conn = get_db_connection()
cursor = conn.cursor()

cursor.execute("""
    SELECT id, name
    FROM mydb.travels
    ORDER BY id DESC
""")

travels = cursor.fetchall()

cursor.close()
conn.close()


if travels:

    # 旅行を選択
    travel_options = {
        f"{travel[1]}": travel[0]
        for travel in travels
    }

    selected_travel = st.selectbox(
        "旅行を選択してください",
        list(travel_options.keys())
    )

    travel_id = travel_options[selected_travel]


    # ==========================================
    # キーワード検索
    # ==========================================

    with st.sidebar:

        st.header("検索")

        keyword = st.text_input(
            "キーワードを入力してください"
        )


    # ==========================================
    # レシートを検索
    # ==========================================

    conn = get_db_connection()
    cursor = conn.cursor()

    if keyword:

        sql = """
            SELECT id, name, text, image_path
            FROM mydb.evidences
            WHERE travel_id = %s
            AND text LIKE %s
            ORDER BY id DESC
        """

        search_keyword = f"%{keyword}%"

        cursor.execute(
            sql,
            (travel_id, search_keyword)
        )

    else:

        sql = """
            SELECT id, name, text, image_path
            FROM mydb.evidences
            WHERE travel_id = %s
            ORDER BY id DESC
        """

        cursor.execute(
            sql,
            (travel_id,)
        )


    results = cursor.fetchall()

    cursor.close()
    conn.close()


    # ==========================================
    # 検索結果
    # ==========================================

    st.subheader(
        f"{selected_travel} のレシート"
    )


    if keyword:
        st.write(
            f"「{keyword}」の検索結果"
        )


    if results:

        for result in results:

            id, name, text, image_path = result

            with st.expander(f"{name}"):

                # 画像表示
                if image_path and os.path.exists(image_path):
                    st.image(image_path)
                else:
                    st.write(
                        "画像ファイルが存在しません。"
                    )


                # OCR結果
                st.write(text)


                # 削除ボタン
                if st.button(
                    "削除",
                    key=f"delete_{id}"
                ):

                    st.session_state[
                        f"confirm_{id}"
                    ] = True


                # 削除確認
                if st.session_state.get(
                    f"confirm_{id}",
                    False
                ):

                    st.warning(
                        "本当に削除しますか？"
                    )

                    if st.button(
                        "削除する",
                        key=f"confirm_delete_{id}"
                    ):

                        conn = get_db_connection()
                        cursor = conn.cursor()

                        sql = """
                            DELETE FROM mydb.evidences
                            WHERE id = %s
                        """

                        cursor.execute(
                            sql,
                            (id,)
                        )

                        conn.commit()


                        # 画像ファイルも削除
                        if (
                            image_path
                            and os.path.exists(image_path)
                        ):
                            os.remove(image_path)


                        cursor.close()
                        conn.close()


                        st.success(
                            "削除しました"
                        )

                        st.rerun()

    else:

        if keyword:
            st.info(
                "この旅行には検索結果がありません。"
            )
        else:
            st.info(
                "この旅行にはレシートがありません。"
            )


else:

    st.warning(
        "旅行が登録されていません。"
    )

