import streamlit as st
import pandas as pd
from datetime import datetime
from pytz import timezone
from collections import defaultdict

# 商品清單
stalls = {
    "清涼飲品": [
        {"name": "珍珠奶茶", "price": 50, "stock": 20},
        {"name": "檸檬綠茶", "price": 40, "stock": 15}
    ],
    "美味小吃": [
        {"name": "炸雞塊", "price": 60, "stock": 10},
        {"name": "熱狗堡", "price": 45, "stock": 12}
    ],
    "趣味遊戲": [
        {"name": "套圈圈（1次）", "price": 30, "stock": 50},
        {"name": "射氣球（1次）", "price": 35, "stock": 30}
    ]
}

# 初始化
if "users" not in st.session_state:
    st.session_state.users = {}
if "current_user" not in st.session_state:
    st.session_state.current_user = None
if "product_sales" not in st.session_state:
    st.session_state.product_sales = defaultdict(int)
if "purchase_log" not in st.session_state:
    st.session_state.purchase_log = []

st.title("🎪 校園園遊會交易模擬系統（多人版）")

# 使用者登入或切換
col1, col2 = st.columns([3,1])
with col1:
    username = st.text_input("輸入你的名字來登入或切換：")
with col2:
    if st.button("✅ 登入 / 切換使用者") and username:
        if username not in st.session_state.users:
            st.session_state.users[username] = {
                "balance": 500,
                "cart": []
            }
        st.session_state.current_user = username

# 未登入就中止
if not st.session_state.current_user:
    st.stop()

user_data = st.session_state.users[st.session_state.current_user]
st.markdown(f"👤 目前使用者：**{st.session_state.current_user}**，餘額：${user_data['balance']}")

# 購買介面
for stall_name, products in stalls.items():
    st.header(f"📍 {stall_name}")
    for i, product in enumerate(products):
        col1, col2, col3 = st.columns([3, 2, 1])
        with col1:
            st.text(f"{product['name']} (${product['price']}) - 剩 {product['stock']}")
        with col2:
            if st.button(f"購買 {product['name']}", key=f"{stall_name}-{i}-{st.session_state.current_user}"):
                if product["stock"] <= 0:
                    st.warning("庫存不足！")
                elif user_data["balance"] < product["price"]:
                    st.warning("餘額不足！")
                else:
                    product["stock"] -= 1
                    user_data["balance"] -= product["price"]
                    user_data["cart"].append(product["name"])
                    timestamp = datetime.now(timezone("Asia/Taipei")).strftime("%Y-%m-%d %H:%M")
                    st.session_state.purchase_log.append({
                        "buyer": st.session_state.current_user,
                        "item": product["name"],
                        "price": product["price"],
                        "time": timestamp
                    })
                    st.session_state.product_sales[product["name"]] += 1
                    st.success(f"{product['name']} 購買成功！")

# 顯示個人紀錄
st.subheader("🧾 你的購買紀錄")
if user_data["cart"]:
    for item in user_data["cart"]:
        st.write(f"• {item}")
else:
    st.write("尚未購買任何商品。")

st.write(f"💰 剩餘餘額：${user_data['balance']}")

# 排行榜（消費前5名）
st.subheader("🏆 消費排行榜（前5名）")
ranked_users = sorted(
    [(u, sum([r["price"] for r in st.session_state.purchase_log if r["buyer"] == u]))
     for u in st.session_state.users],
    key=lambda x: x[1], reverse=True
)[:5]
for i, (user, total) in enumerate(ranked_users, 1):
    st.write(f"{i}. {user} - ${total}")

# 商品銷售排行
st.subheader("🔥 熱銷商品排行榜（前5名）")
top_products = sorted(st.session_state.product_sales.items(), key=lambda x: x[1], reverse=True)[:5]
for i, (item, count) in enumerate(top_products, 1):
    st.write(f"{i}. {item}（賣出 {count} 件）")

# 交易紀錄下載
st.subheader("📥 下載交易紀錄")
if st.session_state.purchase_log:
    df = pd.DataFrame(st.session_state.purchase_log)
    st.dataframe(df)
    csv = df.to_csv(index=False).encode("utf-8-sig")
    st.download_button("📥 下載 CSV", csv, "交易紀錄.csv", "text/csv")
else:
    st.info("目前尚無交易紀錄。")
import time

public_url = ngrok.connect(8501)
print(f"🔗 開啟網址：{public_url}")
time.sleep(3)
