import streamlit as st


def main():

    st.set_page_config(
        page_title="旅行精算アプリ",
        page_icon="",
        layout="centered"
    )

    st.markdown(
        """
        <style>

        /* =========================
           全体
        ========================= */

        .stApp {
            background-color: #f6faf8;
        }

        .block-container {
            max-width: 900px;
            padding-top: 2.5rem;
            padding-bottom: 5rem;
        }


        /* =========================
           見出し
        ========================= */

        h1 {
            color: #24372f !important;
            font-weight: 750;
            letter-spacing: -0.6px;
        }

        h2 {
            color: #30483d !important;
            font-weight: 700;
            margin-top: 2rem;
        }

        h3 {
            color: #3a5147 !important;
            font-weight: 700;
        }

        p {
            color: #65746d !important;
        }


        /* =========================
           入力欄
        ========================= */

        input {
            border-radius: 12px !important;
        }

        textarea {
            border-radius: 12px !important;
        }

        div[data-baseweb="select"] > div {
            border-radius: 12px;
            border: 1px solid #d8e7df;
            background-color: white;
        }


        /* =========================
           通常ボタン
        ========================= */

        .stButton > button {
            width: 100%;
            min-height: 46px;
            border-radius: 12px;
            border: 1px solid #d7e5de;
            background-color: white;
            color: #355247 !important;
            font-size: 15px;
            font-weight: 650;
            transition: 0.2s;
        }

        .stButton > button p {
            color: #355247 !important;
        }

        .stButton > button:hover {
            border-color: #91bfa9;
            background-color: #edf7f2;
        }

        .stButton > button:hover p {
            color: #285c48 !important;
        }


        /* =========================
           緑のボタン
        ========================= */

        button[kind="primary"] {
            background-color: #4f8a71 !important;
            border: 1px solid #4f8a71 !important;
            color: white !important;
        }

        button[kind="primary"] p {
            color: white !important;
        }

        button[kind="primary"] span {
            color: white !important;
        }

        button[kind="primary"] div {
            color: white !important;
        }

        button[kind="primary"]:hover {
            background-color: #41775f !important;
            border-color: #41775f !important;
        }

        button[kind="primary"]:hover p {
            color: white !important;
        }

        button[kind="primary"]:hover span {
            color: white !important;
        }

        button[kind="primary"]:hover div {
            color: white !important;
        }


        /* =========================
           区切り線
        ========================= */

        hr {
            border: none;
            border-top: 1px solid #dfeae4;
            margin: 2rem 0;
        }


        /* =========================
           カード
        ========================= */

        div[data-testid="stVerticalBlockBorderWrapper"] {
            border-radius: 18px;
            border: 1px solid #dfe9e4;
            background-color: white;
        }


        /* =========================
           Metric
        ========================= */

        div[data-testid="stMetric"] {
            background-color: white;
            border: 1px solid #dfe9e9;
            border-radius: 18px;
            padding: 22px 24px;
            box-shadow: 0 4px 14px rgba(48, 72, 61, 0.05);
        }

        div[data-testid="stMetricLabel"] {
            color: #718078 !important;
            font-size: 14px;
        }

        div[data-testid="stMetricValue"] {
            color: #294a3c !important;
            font-weight: 750;
        }


        /* =========================
           Alert
        ========================= */

        div[data-testid="stAlert"] {
            border-radius: 14px;
        }


        /* =========================
           File uploader
        ========================= */

        section[data-testid="stFileUploaderDropzone"] {
            border: 1px dashed #b8d3c5;
            border-radius: 16px;
            background-color: #fbfdfc;
        }


        /* =========================
           Expander
        ========================= */

        details {
            border: 1px solid #dfe9e4 !important;
            border-radius: 14px !important;
            background-color: white !important;
        }


        </style>
        """,
        unsafe_allow_html=True
    )


    # =========================
    # ページ設定
    # =========================

    pages = st.navigation(
        [
            st.Page(
                "pages/travel.py",
                title="旅行",
                url_path="travel",
                default=True
            ),

            st.Page(
                "pages/home.py",
                title="レシート",
                url_path="home"
            ),

            st.Page(
                "pages/search.py",
                title="検索",
                url_path="search"
            ),

            st.Page(
                "pages/settlement.py",
                title="割り勘",
                url_path="settlement"
            ),
        ]
    )


    pages.run()


if __name__ == "__main__":
    main()