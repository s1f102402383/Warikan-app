import streamlit as st
from db import get_db_connection


st.title("割り勘")

st.caption(
    "旅行で使った金額をもとに、誰が誰にいくら支払えばよいかを自動で計算します。"
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

    st.info(
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


settlement_travel_id = st.session_state.get(
    "settlement_travel_id"
)


default_index = 0


if settlement_travel_id is not None:

    for i, travel_id in enumerate(
        travel_ids
    ):

        if travel_id == settlement_travel_id:

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

selected_travel_name = travels[
    selected_index
][1]


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


if len(members) < 2:

    st.warning(
        "割り勘には2人以上のメンバーが必要です。"
    )

    st.stop()


# ==================================================
# 支払いデータ取得
# ==================================================

conn = get_db_connection()
cursor = conn.cursor()

cursor.execute(
    """
    SELECT
        payer_id,
        COALESCE(SUM(amount), 0)
    FROM mydb.evidences
    WHERE travel_id = %s
    GROUP BY payer_id
    """,
    (travel_id,)
)

payment_data = cursor.fetchall()

cursor.close()
conn.close()


# ==================================================
# 支払額
# ==================================================

payments = {}

for member_id, member_name in members:

    payments[member_id] = 0


for payer_id, amount in payment_data:

    if payer_id in payments:

        payments[payer_id] = int(
            amount or 0
        )


# ==================================================
# 金額計算
# ==================================================

total_amount = sum(
    payments.values()
)

member_count = len(
    members
)

per_person = (
    total_amount / member_count
)


# ==================================================
# 旅行情報
# ==================================================

st.subheader(
    selected_travel_name
)

st.caption(
    f"{member_count}人で割り勘"
)


# ==================================================
# 金額
# ==================================================

col1, col2 = st.columns(2)


with col1:

    st.metric(
        "旅行で使った合計",
        f"{total_amount:,} 円"
    )


with col2:

    st.metric(
        "1人あたり",
        f"{per_person:,.0f} 円"
    )


# ==================================================
# 支払った金額
# ==================================================

st.divider()

st.subheader(
    "支払った金額"
)


for member_id, member_name in members:

    paid = payments[
        member_id
    ]


    with st.container(border=True):

        col1, col2 = st.columns(
            [3, 1]
        )


        with col1:

            st.markdown(
                f"**{member_name}**"
            )


        with col2:

            st.markdown(
                f"**{paid:,} 円**"
            )


# ==================================================
# 差額計算
# ==================================================

balances = []


for member_id, member_name in members:

    balance = (
        payments[member_id]
        - per_person
    )

    balances.append(
        (
            member_id,
            member_name,
            balance
        )
    )


creditors = []
debtors = []


for (
    member_id,
    member_name,
    balance
) in balances:

    if balance > 0.01:

        creditors.append(
            [
                member_id,
                member_name,
                balance
            ]
        )

    elif balance < -0.01:

        debtors.append(
            [
                member_id,
                member_name,
                -balance
            ]
        )


# ==================================================
# 精算計算
# ==================================================

settlements = []

i = 0
j = 0


while (
    i < len(debtors)
    and j < len(creditors)
):

    debtor = debtors[i]
    creditor = creditors[j]

    amount = min(
        debtor[2],
        creditor[2]
    )

    settlements.append(
        (
            debtor[1],
            creditor[1],
            amount
        )
    )

    debtor[2] -= amount

    creditor[2] -= amount


    if debtor[2] < 0.01:

        i += 1


    if creditor[2] < 0.01:

        j += 1


# ==================================================
# 精算
# ==================================================

st.divider()

st.subheader(
    "精算"
)


if settlements:

    st.write(
        "以下の支払いを行えば、旅行の精算が完了します。"
    )


    for (
        debtor_name,
        creditor_name,
        amount
    ) in settlements:


        with st.container(border=True):

            st.markdown(
                f"### {amount:,.0f} 円"
            )


            col1, col2, col3 = st.columns(
                [2, 1, 2]
            )


            with col1:

                st.caption(
                    "支払う人"
                )

                st.markdown(
                    f"**{debtor_name}**"
                )


            with col2:

                st.markdown(
                    "<div style='text-align:center; font-size:28px; color:#80a594;'>→</div>",
                    unsafe_allow_html=True
                )


            with col3:

                st.caption(
                    "受け取る人"
                )

                st.markdown(
                    f"**{creditor_name}**"
                )


            st.success(
                f"{debtor_name}さんが"
                f"{creditor_name}さんに"
                f"{amount:,.0f}円支払います。"
            )


else:

    st.success(
        "精算は完了しています。追加の支払いはありません。"
    )