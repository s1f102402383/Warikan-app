FROM python:3.12-slim

# uv を公式イメージからコピー
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

WORKDIR /app

# 依存定義を先に入れる
COPY pyproject.toml uv.lock ./
COPY .streamlit ./.streamlit

# 本番用依存だけ入れる
ENV UV_NO_DEV=1
RUN uv sync --locked

# アプリ本体をコピー
COPY src ./src

# アプリ起動
CMD ["uv", "run", "streamlit", "run", "src/main.py"]
