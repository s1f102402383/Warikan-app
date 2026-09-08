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

        if st.button("OCR実行"):

            # 画像を保存
            save_dir = "src/uploads"
            os.makedirs(save_dir, exist_ok=True)

            # 元のファイルの拡張子でやる
            extension = os.path.splitext(uploaded_file.name)[1]

            # UUIDを使って重複しないファイル名を作る
            file_name = f"{uuid.uuid4()}{extension}"
            ##ここでパスを入れる
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

            # DBに接続
            conn = get_db_connection()
            cursor = conn.cursor()

            sql = """
                INSERT INTO mydb.evidences (name, text, image_path)
                VALUES (%s, %s, %s)
            """

            cursor.execute(
                sql,
                (uploaded_file.name, test, image_path)
            )

            conn.commit()

            cursor.close()
            conn.close()

            st.write(result)


main()