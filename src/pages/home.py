import streamlit as st
import requests


def main():
    st.title("ホーム")

    uploaded_file = st.file_uploader(
        "画像を選択してください",
        type=["png", "jpg", "jpeg", "pdf"]
    )

    if uploaded_file is not None:
        st.image(uploaded_file)

        if st.button("OCR実行"):
            files = {
                "file": (
                    uploaded_file.name,
                    uploaded_file.getvalue(),
                    uploaded_file.type,
                )
            }

            data = {
                "evidence_type": "receipt"
            }

            headers = {
                "Accept": "application/ocrv3+json",
                "Authorization": "REMOVED_API_KEY" #APikey
            }

            response = requests.post(
                "https://ocr-bridge-dev.inv.sorimachi.biz/recognize",
                headers=headers,
                files=files,
                data=data,
            )

            result = response.json()

            st.write(result)


main()