import streamlit as st
from db import get_db_connection

st.title("旅行メンバー登録")
travel_name = st.text_input("旅行先を入力してください")

# メンバー一覧を保存
if "members" not in st.session_state:
    st.session_state.members = []

name = st.text_input("名前を入力してください")

if st.button("メンバーを追加"):
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

        st.success("旅行を開始します！")

    else:
        st.warning("旅行名と2人以上のメンバーを登録してください。")