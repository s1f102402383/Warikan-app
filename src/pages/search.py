import streamlit as st
import os
from db import get_db_connection


st.title("検索")

st.caption(
    "旅行を選択して、登録したレシートを確認・検索できます。"
)


# ==================================================
# 旅行取得
# ==================================================

conn = get_db_connection()
cursor = conn.cursor()

cursor.execute(
    """
    SELECT id, name
    FROM mydb.travels
    ORDER BY id DESC
    """
)

travels = cursor.fetchall()

cursor.close()
conn.close()


if not travels:

    st.info(
        "先に旅行を作成してください。"
    )

    st.stop()


travel_labels = [
    f"{travel[1]}（ID: {travel[0]}）"
    for travel in travels
]

travel_ids = [
    travel[0]
    for travel in travels
]


# ==================================================
# 旅行選択
# ==================================================

selected_label = st.selectbox(
    "旅行",
    travel_labels
)

selected_index = travel_labels.index(
    selected_label
)

travel_id = travel_ids[
    selected_index
]

selected_travel_name = travels[
    selected_index
][1]


# ==================================================
# キーワード
# ==================================================

keyword = st.text_input(
    "キーワード検索",
    placeholder="レシートの内容を入力してください"
)


# ==================================================
# レシート取得
# ==================================================

conn = get_db_connection()
cursor = conn.cursor()


if keyword.strip():

    cursor.execute(
        """
        SELECT
            id,
            name,
            text,
            image_path,
            amount,
            payer_id
        FROM mydb.evidences
        WHERE travel_id = %s
        AND text LIKE %s
        ORDER BY id DESC
        """,
        (
            travel_id,
            f"%{keyword.strip()}%"
        )
    )

else:

    cursor.execute(
        """
        SELECT
            id,
            name,
            text,
            image_path,
            amount,
            payer_id
        FROM mydb.evidences
        WHERE travel_id = %s
        ORDER BY id DESC
        """,
        (travel_id,)
    )


results = cursor.fetchall()

cursor.close()
conn.close()


# ==================================================
# 見出し
# ==================================================

st.divider()

st.subheader(
    f"{selected_travel_name}のレシート"
)


if keyword.strip():

    st.caption(
        f"「{keyword}」の検索結果"
    )


# ==================================================
# 結果
# ==================================================

if not results:

    if keyword.strip():

        st.info(
            "検索結果がありません。"
        )

    else:

        st.info(
            "この旅行にはレシートがありません。"
        )

    st.stop()


for result in results:

    (
        evidence_id,
        name,
        text,
        image_path,
        amount,
        payer_id
    ) = result


    # ==============================================
    # メンバー名取得
    # ==============================================

    payer_name = "不明"


    if payer_id:

        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT name
            FROM mydb.members
            WHERE id = %s
            """,
            (payer_id,)
        )

        payer = cursor.fetchone()

        cursor.close()
        conn.close()

        if payer:

            payer_name = payer[0]


    # ==============================================
    # レシートカード
    # ==============================================

    with st.container(border=True):

        st.markdown(
            f"### {name}"
        )


        col1, col2 = st.columns(
            2
        )


        with col1:

            st.caption(
                "支払った人"
            )

            st.write(
                payer_name
            )


        with col2:

            st.caption(
                "金額"
            )

            if amount is not None:

                st.markdown(
                    f"**{int(amount):,} 円**"
                )

            else:

                st.write(
                    "金額なし"
                )


        st.divider()


        if image_path and os.path.exists(
            image_path
        ):

            st.image(
                image_path,
                use_container_width=True
            )

        else:

            st.info(
                "画像ファイルが存在しません。"
            )


        st.write("")


        st.caption(
            "読み取り結果"
        )


        if text:

            st.write(
                text
            )

        else:

            st.info(
                "読み取りテキストがありません。"
            )


        st.write("")


        # ==========================================
        # 削除確認
        # ==========================================

        delete_key = (
            f"confirm_delete_{evidence_id}"
        )


        if not st.session_state.get(
            delete_key,
            False
        ):

            if st.button(
                "レシートを削除",
                key=f"delete_{evidence_id}"
            ):

                st.session_state[
                    delete_key
                ] = True

                st.rerun()


        else:

            st.warning(
                "このレシートを削除しますか？"
            )


            col1, col2 = st.columns(
                2
            )


            with col1:

                if st.button(
                    "キャンセル",
                    key=f"cancel_{evidence_id}"
                ):

                    st.session_state[
                        delete_key
                    ] = False

                    st.rerun()


            with col2:

                if st.button(
                    "削除する",
                    key=f"confirm_{evidence_id}",
                    type="primary"
                ):

                    conn = get_db_connection()
                    cursor = conn.cursor()


                    cursor.execute(
                        """
                        DELETE FROM mydb.evidences
                        WHERE id = %s
                        """,
                        (evidence_id,)
                    )


                    conn.commit()

                    cursor.close()
                    conn.close()


                    if (
                        image_path
                        and os.path.exists(image_path)
                    ):

                        os.remove(
                            image_path
                        )


                    st.success(
                        "レシートを削除しました。"
                    )

                    st.rerun()