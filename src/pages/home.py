
import streamlit as st
import requests
import os
import uuid
from db import get_db_connection


def main():
    st.title("レシート登録")

    uploaded_file = st.file_uploader(
        "画像を選択してください",
        type=["png", "jpg", "jpeg", "pdf"]
    )

    if uploaded_file is not None:
        st.image(uploaded_file)

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
                f"{travel[1]}（ID: {travel[0]}）": travel[0]
                for travel in travels
            }

            travel_names = list(travel_options.keys())

            # 直前に作成した旅行を取得
            created_travel_id = st.session_state.get(
                "created_travel_id"
            )

            # 初期状態では一番上の旅行を選択
            default_index = 0

            # 直前に作成した旅行があれば自動選択
            if created_travel_id is not None:

                for i, travel in enumerate(travels):

                    if travel[0] == created_travel_id:
                        default_index = i
                        break

            selected_travel = st.selectbox(
                "旅行を選択してください",
                travel_names,
                index=default_index
            )

            travel_id = travel_options[selected_travel]

            # ==========================================
            # 選択した旅行のメンバーを取得
            # ==========================================

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

                # メンバーを選択
                member_options = {
                    member[1]: member[0]
                    for member in members
                }

                selected_payer = st.selectbox(
                    "支払った人を選択してください",
                    list(member_options.keys())
                )

                payer_id = member_options[selected_payer]

                # ==========================================
                # OCR実行
                # ==========================================

                if st.button("OCR実行"):

                    # 画像を保存
                    save_dir = "src/uploads"
                    os.makedirs(save_dir, exist_ok=True)

                    extension = os.path.splitext(
                        uploaded_file.name
                    )[1]

                    file_name = f"{uuid.uuid4()}{extension}"

                    image_path = os.path.join(
                        save_dir,
                        file_name
                    )

                    with open(image_path, "wb") as f:
                        f.write(uploaded_file.getvalue())

                    # OCRに送るファイル
                    files = {
                        "file": (
                            file_name,
                            uploaded_file.getvalue(),
                            uploaded_file.type,
                        )
                    }

                    # OCR APIのデータ
                    data = {
                        "evidence_type": "receipt"
                    }

                    # OCR APIのヘッダー
                    headers = {
                        "Accept": "application/ocrv3+json",
                        "Authorization": "REMOVED_API_KEY"
                    }

                    # OCR APIを実行
                    response = requests.post(
                        "https://ocr-bridge-dev.inv.sorimachi.biz/recognize",
                        headers=headers,
                        files=files,
                        data=data,
                    )

                    result = response.json()

                    # OCRで読み取った文章
                    test = result[
                        "result"
                    ][
                        "ocrInfo"
                    ][
                        "fullText"
                    ][
                        "text"
                    ]

                    # 合計金額
                    amount = result[
                        "result"
                    ][
                        "totalPrice"
                    ][
                        "price"
                    ][
                        "formatted"
                    ][
                        "value"
                    ]

                    # ==========================================
                    # DBに保存
                    # ==========================================

                    conn = get_db_connection()
                    cursor = conn.cursor()

                    sql = """
                        INSERT INTO mydb.evidences
                        (name, text, image_path, travel_id, payer_id, amount)
                        VALUES (%s, %s, %s, %s, %s, %s)
                    """

                    cursor.execute(
                        sql,
                        (
                            uploaded_file.name,
                            test,
                            image_path,
                            travel_id,
                            payer_id,
                            amount
                        )
                    )

                    conn.commit()

                    cursor.close()
                    conn.close()

                    # ==========================================
                    # OCR結果を保存
                    # ==========================================

                    st.session_state.ocr_completed = True
                    st.session_state.ocr_amount = amount
                    st.session_state.ocr_travel_id = travel_id

                    st.rerun()

                # ==========================================
                # OCR完了後の表示
                # ==========================================

                if st.session_state.get(
                    "ocr_completed",
                    False
                ):

                    st.divider()

                    st.subheader(
                        "レシートの合計金額"
                    )

                    st.markdown(
                        f"""
                        <div style="
                            font-size: 36px;
                            font-weight: bold;
                            text-align: center;
                            padding: 15px;
                        ">
                            {st.session_state.ocr_amount} 円
                        </div>
                        """,
                        unsafe_allow_html=True
                    )

                    st.success(
                        "レシートを登録しました！"
                    )

                    st.write("")

                    # ==========================================
                    # 割り勘ページへ
                    # ==========================================

                    if st.button(
                        "💰 割り勘結果を見る",
                        use_container_width=True
                    ):

                        st.session_state.settlement_travel_id = (
                            st.session_state.ocr_travel_id
                        )

                        st.switch_page(
                            "pages/settlement.py"
                        )

            else:
                st.warning(
                    "この旅行にはメンバーが登録されていません。"
                )

        else:
            st.warning(
                "旅行が登録されていません。"
            )


main()
