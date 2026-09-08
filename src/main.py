import streamlit as st


def main():
    # ページ設定
    st.set_page_config(page_title="画像アップロードアプリ")
    pages = st.navigation(
        [
            st.Page("pages/home.py", title="ホーム"),
            st.Page("pages/serch.py",title="検索"),
        ]
    )
    pages.run()


if __name__ == "__main__":
    main()
