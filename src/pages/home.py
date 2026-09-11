import streamlit as st
import requests
import os
import uuid
from db import get_db_connection


st.title("レシート")

st.caption(
    "レシート画像を登録すると、OCRで内容と合計金額を読み取ります。"
)


# ==================================================
# レシート選択
# ==================================================

uploaded_file = st.file_uploader(
    "レシートを選択してください",
    type=[
        "png",
        "jpg",
        "jpeg",
        "pdf"
    ]
)


# ==================================================
# レシートが選択された場合
# ==================================================

if uploaded_file is not None:

    if uploaded_file.type != "application/pdf":

        st.image(
            uploaded_file,
            use_container_width=True
        )

    else:

        st.info(
            "PDFファイルが選択されています。"
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

        st.warning(
            "先に旅行を作成してください。"
        )

        st.stop()


    # ==================================================
    # 旅行選択
    # ==================================================

    travel_labels = [
        f"{travel[1]}（ID: {travel[0]}）"
        for travel in travels
    ]

    travel_ids = [
        travel[0]
        for travel in travels
    ]


    created_travel_id = st.session_state.get(
        "created_travel_id"
    )


    default_index = 0


    if created_travel_id is not None:

        for i, travel_id in enumerate(
            travel_ids
        ):

            if travel_id == created_travel_id:

                default_index = i

                break


    selected_label = st.selectbox(
        "旅行",
        travel_labels,
        index=default_index
    )


    selected_index = travel_labels.index(
        selected_label
    )

    travel_id = travel_ids[
        selected_index
    ]


    # ==================================================
    # メンバー取得
    # ==================================================

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT id, name
        FROM mydb.members
        WHERE travel_id = %s
        ORDER BY id
        """,
        (travel_id,)
    )

    members = cursor.fetchall()

    cursor.close()
    conn.close()


    if not members:

        st.warning(
            "この旅行にはメンバーが登録されていません。"
        )

        st.stop()


    # ==================================================
    # 支払った人
    # ==================================================

    member_labels = [
        f"{member[1]}（ID: {member[0]}）"
        for member in members
    ]


    selected_member_label = st.selectbox(
        "支払った人",
        member_labels
    )


    member_index = member_labels.index(
        selected_member_label
    )

    payer_id = members[
        member_index
    ][0]


    st.write("")


    # ==================================================
    # OCR
    # ==================================================

    if st.button(
        "OCRでレシートを読み取る",
        type="primary",
        use_container_width=True
    ):

        save_dir = "src/uploads"

        os.makedirs(
            save_dir,
            exist_ok=True
        )


        extension = os.path.splitext(
            uploaded_file.name
        )[1]


        file_name = (
            f"{uuid.uuid4()}{extension}"
        )


        image_path = os.path.join(
            save_dir,
            file_name
        )


        with open(
            image_path,
            "wb"
        ) as f:

            f.write(
                uploaded_file.getvalue()
            )


        files = {
            "file": (
                file_name,
                uploaded_file.getvalue(),
                uploaded_file.type
            )
        }


        data = {
            "evidence_type": "receipt"
        }


        # ==================================================
        # OCR API
        # ==================================================

        headers = {
            "Accept": "application/ocrv3+json",
            "Authorization": "REMOVED_API_KEY"
        }


        try:

            response = requests.post(
                "https://ocr-bridge-dev.inv.sorimachi.biz/recognize",
                headers=headers,
                files=files,
                data=data,
                timeout=60
            )


            response.raise_for_status()

            result = response.json()


            # ==================================================
            # OCRテキスト取得
            # ==================================================

            ocr_text = (
                result
                ["result"]
                ["ocrInfo"]
                ["fullText"]
                ["text"]
            )


            # ==================================================
            # 金額取得
            # ==================================================

            amount = (
                result
                ["result"]
                ["totalPrice"]
                ["price"]
                ["formatted"]
                ["value"]
            )


            # ==================================================
            # DB登録
            # ==================================================

            conn = get_db_connection()
            cursor = conn.cursor()


            cursor.execute(
                """
                INSERT INTO mydb.evidences
                (
                    name,
                    text,
                    image_path,
                    travel_id,
                    payer_id,
                    amount
                )
                VALUES (
                    %s,
                    %s,
                    %s,
                    %s,
                    %s,
                    %s
                )
                """,
                (
                    uploaded_file.name,
                    ocr_text,
                    image_path,
                    travel_id,
                    payer_id,
                    amount
                )
            )


            conn.commit()


            cursor.close()
            conn.close()


            # ==================================================
            # OCR結果を保存
            # ==================================================

            st.session_state.ocr_completed = True

            st.session_state.ocr_amount = amount

            st.session_state.ocr_travel_id = travel_id


            st.rerun()


        except Exception as e:

            st.error(
                f"OCR処理に失敗しました：{e}"
            )


# ==================================================
# OCR結果
# ==================================================

if st.session_state.get(
    "ocr_completed",
    False
):

    st.divider()

    st.subheader("読み取り結果")


    amount = st.session_state.get(
        "ocr_amount",
        0
    )


    with st.container(border=True):

        st.caption(
            "レシートの合計金額"
        )


        st.markdown(
            f"""
            <div style="
                font-size:42px;
                font-weight:750;
                color:#2f6b53;
                margin-top:5px;
                margin-bottom:5px;
            ">
                {amount} 円
            </div>
            """,
            unsafe_allow_html=True
        )


    st.success(
        "レシートを登録しました。"
    )


    st.write("")


    if st.button(
        "割り勘結果を見る",
        type="primary",
        use_container_width=True
    ):

        st.session_state.settlement_travel_id = (
            st.session_state.ocr_travel_id
        )


        st.switch_page(
            "pages/settlement.py"
        )