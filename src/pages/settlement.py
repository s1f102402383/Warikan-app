import streamlit as st
from db import get_db_connection


st.title("割り勘計算")

# 旅行を取得
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

    # 旅行名ではなくIDを使って選択肢を作る
    travel_options = {
        f"{travel[1]}（ID: {travel[0]}）": travel[0]
        for travel in travels
    }

    selected_travel = st.selectbox(
        "旅行を選択してください",
        list(travel_options.keys())
    )

    travel_id = travel_options[selected_travel]

    st.write("選択した旅行ID:", travel_id)

    # =========================
    # メンバーを取得
    # =========================

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

    st.subheader("メンバー")

    for member in members:
        st.write(f"・{member[1]}（ID: {member[0]}）")

    # =========================
    # 支払額を取得
    # =========================

    st.subheader("支払額")

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT payer_id, SUM(amount)
        FROM mydb.evidences
        WHERE travel_id = %s
        GROUP BY payer_id
    """, (travel_id,))

    payments = cursor.fetchall()

    cursor.close()
    conn.close()

    # メンバーごとの支払額を保存
    paid_amounts = {}

    for member in members:
        member_id = member[0]
        member_name = member[1]

        paid = 0

        for payment in payments:
            payer_id, total_paid = payment

            if payer_id == member_id:
                paid = total_paid

        paid_amounts[member_id] = paid

        st.write(
            f"{member_name}（ID: {member_id}）：{paid}円"
        )

    # =========================
    # 旅行全体の合計金額
    # =========================

    st.subheader("旅行全体の合計金額")

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT SUM(amount)
        FROM mydb.evidences
        WHERE travel_id = %s
    """, (travel_id,))

    total_amount = cursor.fetchone()[0]

    cursor.close()
    conn.close()

    if total_amount is None:
        total_amount = 0

    st.write(f"合計：{total_amount}円")

    # =========================
    # 1人あたりの負担額
    # =========================

    st.subheader("1人あたりの負担額")

    if members:
        per_person = total_amount / len(members)
        st.write(f"1人あたり：{per_person:.0f}円")

        # =========================
        # 精算額
        # =========================

        st.subheader("精算額")

        balances = {}

        for member in members:
            member_id = member[0]
            member_name = member[1]

            paid = paid_amounts[member_id]

            balance = paid - per_person

            balances[member_id] = balance

            if balance > 0:
                st.write(
                    f"{member_name}（ID: {member_id}）："
                    f"{balance:.0f}円 もらう"
                )
            elif balance < 0:
                st.write(
                    f"{member_name}（ID: {member_id}）："
                    f"{abs(balance):.0f}円 払う"
                )
            else:
                st.write(
                    f"{member_name}（ID: {member_id}）："
                    "精算なし"
                )

        # =========================
        # 誰が誰にいくら払うか
        # =========================

        st.subheader("精算方法")

        # お金を払う人
        debtors = []

        # お金をもらう人
        creditors = []

        for member in members:
            member_id = member[0]
            member_name = member[1]
            balance = balances[member_id]

            if balance < 0:
                debtors.append({
                    "id": member_id,
                    "name": member_name,
                    "amount": -balance
                })

            elif balance > 0:
                creditors.append({
                    "id": member_id,
                    "name": member_name,
                    "amount": balance
                })

        # 支払いを計算
        i = 0
        j = 0

        while i < len(debtors) and j < len(creditors):

            debtor = debtors[i]
            creditor = creditors[j]

            payment = min(
                debtor["amount"],
                creditor["amount"]
            )

            st.write(
                f"**{debtor['name']}（ID: {debtor['id']}）"
                f" → "
                f"{creditor['name']}（ID: {creditor['id']}）"
                f"：{payment:.0f}円**"
            )

            debtor["amount"] -= payment
            creditor["amount"] -= payment

            if debtor["amount"] < 0.01:
                i += 1

            if creditor["amount"] < 0.01:
                j += 1

    else:
        st.write("メンバーがいません。")

else:
    st.warning("旅行が登録されていません。")