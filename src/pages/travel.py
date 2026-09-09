import streamlit as st
from db import get_db_connection


st.title("旅行管理")


# ==================================================
# 新しい旅行を作成
# ==================================================

st.header("新しい旅行を作成")

travel_name = st.text_input("旅行先を入力してください")


# メンバー一覧を保存
if "members" not in st.session_state:
    st.session_state.members = []


# メンバー追加フォーム
with st.form("member_form", clear_on_submit=True):

    name = st.text_input("名前を入力してください")

    add_button = st.form_submit_button("メンバーを追加")

    if add_button:
        if name:
            st.session_state.members.append(name)
            st.success(f"{name}さんを追加しました")
        else:
            st.warning("名前を入力してください")


# 現在のメンバーを表示
st.subheader("現在のメンバー")

for i, member in enumerate(st.session_state.members):

    col1, col2 = st.columns([4, 1])

    with col1:
        st.write(f"・{member}")

    with col2:
        if st.button("削除", key=f"delete_member_{i}"):
            st.session_state.members.pop(i)
            st.rerun()


# 旅行を開始
if st.button("旅行を開始"):

    if travel_name and len(st.session_state.members) >= 2:

        conn = get_db_connection()
        cursor = conn.cursor()

        # 旅行を登録
        sql = """
            INSERT INTO mydb.travels (name)
            VALUES (%s)
        """

        cursor.execute(sql, (travel_name,))

        # 登録した旅行のIDを取得
        travel_id = cursor.lastrowid

        # メンバーを登録
        for member in st.session_state.members:

            sql = """
                INSERT INTO mydb.members (travel_id, name)
                VALUES (%s, %s)
            """

            cursor.execute(sql, (travel_id, member))

        conn.commit()

        cursor.close()
        conn.close()

        st.success("旅行を開始しました！")

        # 入力中のメンバーをリセット
        st.session_state.members = []

    else:
        st.warning(
            "旅行名と2人以上のメンバーを登録してください。"
        )


# ==================================================
# 既存の旅行を管理
# ==================================================

st.divider()

st.header("既存の旅行を管理")


# 旅行一覧を取得
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
        f"{travel[1]}（ID: {travel[0]}）": travel[0]
        for travel in travels
    }

    selected_travel = st.selectbox(
        "管理する旅行を選択してください",
        list(travel_options.keys())
    )

    travel_id = travel_options[selected_travel]


    # 選択した旅行のメンバーを取得
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, name
        FROM mydb.members
        WHERE travel_id = %s
        ORDER BY id
    """, (travel_id,))

    existing_members = cursor.fetchall()

    cursor.close()
    conn.close()


    # ------------------------------------------
    # メンバー一覧
    # ------------------------------------------

    st.subheader("現在のメンバー")

    if existing_members:

        for member_id, member_name in existing_members:

            col1, col2 = st.columns([4, 1])

            with col1:
                st.write(f"・{member_name}")

            with col2:
                if st.button(
                    "削除",
                    key=f"existing_delete_{member_id}"
                ):

                    conn = get_db_connection()
                    cursor = conn.cursor()

                    cursor.execute("""
                        DELETE FROM mydb.members
                        WHERE id = %s
                    """, (member_id,))

                    conn.commit()

                    cursor.close()
                    conn.close()

                    st.success(
                        f"{member_name}さんを削除しました"
                    )

                    st.rerun()

    else:
        st.write("メンバーが登録されていません。")


    # ------------------------------------------
    # メンバーを追加
    # ------------------------------------------

    st.subheader("メンバーを追加")

    with st.form(
        f"existing_member_form_{travel_id}",
        clear_on_submit=True
    ):

        new_member_name = st.text_input(
            "追加する名前を入力してください"
        )

        add_existing_member = st.form_submit_button(
            "メンバーを追加"
        )

        if add_existing_member:

            if new_member_name:

                conn = get_db_connection()
                cursor = conn.cursor()

                cursor.execute("""
                    INSERT INTO mydb.members
                    (travel_id, name)
                    VALUES (%s, %s)
                """, (travel_id, new_member_name))

                conn.commit()

                cursor.close()
                conn.close()

                st.success(
                    f"{new_member_name}さんを追加しました"
                )

                st.rerun()

            else:
                st.warning("名前を入力してください。")

else:

    st.info("まだ旅行が登録されていません。")

