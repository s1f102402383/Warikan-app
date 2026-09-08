import streamlit as st
import requests
import os
import uuid
from db import get_db_connection


def main():
    st.title("ホーム")

    uploaded_file = st.file_uploader(
        "画像を選択してください",
        type=["png", "jpg", "jpeg", "pdf"]
    )

    if uploaded_file is not None:
        st.image(uploaded_file)

        # 旅行を選択
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
            travel_options = {
                travel[1]: travel[0]
                for travel in travels
            }

            selected_travel = st.selectbox(
                "旅行を選択してください",
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
            """, (travel_id,))

            members = cursor.fetchall()

            cursor.close()
            conn.close()

            if members:
                member_options = {
                    member[1]: member[0]
                    for member in members
                }

                selected_payer = st.selectbox(
                    "支払った人を選択してください",
                    list(member_options.keys())
                )

                payer_id = member_options[selected_payer]

                if st.button("OCR実行"):

                    # 画像を保存
                    save_dir = "src/uploads"
                    os.makedirs(save_dir, exist_ok=True)

                    extension = os.path.splitext(uploaded_file.name)[1]

                    file_name = f"{uuid.uuid4()}{extension}"

                    image_path = os.path.join(save_dir, file_name)

                    with open(image_path, "wb") as f:
                        f.write(uploaded_file.getvalue())

                    files = {
                        "file": (
                            file_name,
                            uploaded_file.getvalue(),
                            uploaded_file.type,
                        )
                    }

                    data = {
                        "evidence_type": "receipt"
                    }

                    headers = {
                        "Accept": "application/ocrv3+json",
                        "Authorization": "REMOVED_API_KEY"
                    }

                    response = requests.post(
                        "https://ocr-bridge-dev.inv.sorimachi.biz/recognize",
                        headers=headers,
                        files=files,
                        data=data,
                    )

                    result = response.json()

                    test = result["result"]["ocrInfo"]["fullText"]["text"]

                    amount = result["result"]["totalPrice"]["price"]["formatted"]["value"]

                    st.write("合計金額:" + amount + "円")

                    # DBに接続
                    conn = get_db_connection()
                    cursor = conn.cursor()

                    sql = """
                        INSERT INTO mydb.evidences
                        (name, text, image_path, travel_id, payer_id, amount)
                        VALUES (%s, %s, %s, %s, %s, %s)
                            """

                    cursor.execute(
                        sql,(uploaded_file.name, test, image_path, travel_id, payer_id, amount))

                    conn.commit()

                    cursor.close()
                    conn.close()

                    st.write(result)

            else:
                st.warning("この旅行にはメンバーが登録されていません。")

        else:
            st.warning("旅行が登録されていません。")


main()