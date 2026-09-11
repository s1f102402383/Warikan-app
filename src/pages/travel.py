import streamlit as st
from db import get_db_connection


st.title("旅行")

st.caption(
    "旅行を作成して、参加するメンバーを登録します。"
)


# ==================================================
# 新しい旅行
# ==================================================

st.subheader("新しい旅行を作成")

travel_name = st.text_input(
    "旅行名",
    placeholder="例：岡山旅行"
)


# ==================================================
# 作成中メンバー
# ==================================================

if "members" not in st.session_state:
    st.session_state.members = []


with st.form(
    "member_form",
    clear_on_submit=True
):

    name = st.text_input(
        "メンバーの名前",
        placeholder="例：田中"
    )

    add_button = st.form_submit_button(
        "メンバーを追加",
        use_container_width=True
    )

    if add_button:

        if name.strip():

            st.session_state.members.append(
                name.strip()
            )

            st.success(
                f"{name.strip()}さんを追加しました。"
            )

        else:

            st.warning(
                "名前を入力してください。"
            )


st.write("")


if st.session_state.members:

    st.write("現在のメンバー")

    for i, member in enumerate(
        st.session_state.members
    ):

        with st.container(border=True):

            col1, col2 = st.columns(
                [4, 1]
            )

            with col1:

                st.markdown(
                    f"**{member}**"
                )

            with col2:

                if st.button(
                    "削除",
                    key=f"new_delete_{i}"
                ):

                    st.session_state.members.pop(i)

                    st.rerun()

else:

    st.info(
        "まだメンバーが登録されていません。"
    )


st.write("")


# ==================================================
# 旅行開始
# ==================================================

if st.button(
    "このメンバーで旅行を開始",
    type="primary",
    use_container_width=True
):

    if not travel_name.strip():

        st.warning(
            "旅行名を入力してください。"
        )

    elif len(st.session_state.members) < 2:

        st.warning(
            "2人以上のメンバーを登録してください。"
        )

    else:

        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute(
            """
            INSERT INTO mydb.travels (name)
            VALUES (%s)
            """,
            (travel_name.strip(),)
        )

        travel_id = cursor.lastrowid

        for member in st.session_state.members:

            cursor.execute(
                """
                INSERT INTO mydb.members
                (travel_id, name)
                VALUES (%s, %s)
                """,
                (
                    travel_id,
                    member
                )
            )

        conn.commit()

        cursor.close()
        conn.close()

        st.session_state.created_travel_id = travel_id
        st.session_state.members = []

        st.success(
            f"{travel_name.strip()}を作成しました。"
        )

        st.rerun()


# ==================================================
# レシート登録への導線
# ==================================================

if "created_travel_id" in st.session_state:

    st.divider()

    st.subheader("次のステップ")

    st.write(
        "旅行を作成しました。レシートを登録してみましょう。"
    )

    if st.button(
        "レシートを登録する",
        type="primary",
        use_container_width=True
    ):

        st.switch_page(
            "pages/home.py"
        )


# ==================================================
# 既存の旅行
# ==================================================

st.divider()

st.subheader("既存の旅行")


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
        "まだ旅行が登録されていません。"
    )

else:

    travel_labels = [
        f"{travel[1]}（ID: {travel[0]}）"
        for travel in travels
    ]

    selected_label = st.selectbox(
        "旅行を選択",
        travel_labels
    )

    selected_index = travel_labels.index(
        selected_label
    )

    selected_travel_id = travels[
        selected_index
    ][0]

    selected_travel_name = travels[
        selected_index
    ][1]


    # ----------------------------------------------
    # メンバー取得
    # ----------------------------------------------

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT id, name
        FROM mydb.members
        WHERE travel_id = %s
        ORDER BY id
        """,
        (selected_travel_id,)
    )

    existing_members = cursor.fetchall()

    cursor.close()
    conn.close()


    st.write("")

    st.write(
        f"**{selected_travel_name}のメンバー**"
    )


    if existing_members:

        for member_id, member_name in existing_members:

            with st.container(border=True):

                col1, col2 = st.columns(
                    [4, 1]
                )

                with col1:

                    st.markdown(
                        f"**{member_name}**"
                    )

                with col2:

                    if st.button(
                        "削除",
                        key=f"existing_delete_{member_id}"
                    ):

                        conn = get_db_connection()
                        cursor = conn.cursor()

                        cursor.execute(
                            """
                            DELETE FROM mydb.members
                            WHERE id = %s
                            """,
                            (member_id,)
                        )

                        conn.commit()

                        cursor.close()
                        conn.close()

                        st.success(
                            f"{member_name}さんを削除しました。"
                        )

                        st.rerun()

    else:

        st.info(
            "メンバーが登録されていません。"
        )


    # ----------------------------------------------
    # 既存旅行へメンバー追加
    # ----------------------------------------------

    st.write("")

    with st.form(
        f"existing_member_form_{selected_travel_id}",
        clear_on_submit=True
    ):

        new_member_name = st.text_input(
            "新しく追加するメンバー",
            placeholder="例：佐藤"
        )

        add_existing_member = st.form_submit_button(
            "メンバーを追加",
            use_container_width=True
        )


        if add_existing_member:

            if not new_member_name.strip():

                st.warning(
                    "名前を入力してください。"
                )

            else:

                conn = get_db_connection()
                cursor = conn.cursor()

                cursor.execute(
                    """
                    INSERT INTO mydb.members
                    (travel_id, name)
                    VALUES (%s, %s)
                    """,
                    (
                        selected_travel_id,
                        new_member_name.strip()
                    )
                )

                conn.commit()

                cursor.close()
                conn.close()

                st.success(
                    f"{new_member_name.strip()}さんを追加しました。"
                )

                st.rerun()