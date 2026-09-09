import streamlit as st


def main():
    # ページ設定
    st.set_page_config(page_title="画像アップロードアプリ")
    pages = st.navigation(
        [
            st.Page("pages/travel.py",title="旅行"),
            st.Page("pages/home.py", title="レシート登録"),
            st.Page("pages/search.py",title="検索"),
            st.Page("pages/settlement.py",title="割り勘"),
        ]
    )
    pages.run()


if __name__ == "__main__":
    main()
