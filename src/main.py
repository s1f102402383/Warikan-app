import streamlit as st


def main():
    # ページ設定
    st.set_page_config(page_title="旅行精算アプリ")

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
                title="レシート登録",
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

