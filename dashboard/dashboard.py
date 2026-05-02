import streamlit as st
import requests
import random
import pandas as pd
import time
import os

st.set_page_config(page_title="ML Dashboard", layout="wide")

st.title("🚀 Real-Time ML Monitoring Dashboard")

# 🔥 LIVE API (UPDATED)
API = "https://ml-pipeline-project-qbkm.onrender.com/predict"

# =========================
# 📂 STORAGE VIEWER SECTION
# =========================
st.subheader("📂 Stored Data (Cloud Simulation)")

if os.path.exists("stored_data.csv"):
    stored_df = pd.read_csv("stored_data.csv")
    st.dataframe(stored_df)

    st.write("### Summary")
    summary = stored_df["prediction"].value_counts().reset_index()
    summary.columns = ["prediction", "count"]
    st.write(summary)

    # Chart
    st.write("### 📊 Prediction Distribution")
    st.bar_chart(stored_df["prediction"].value_counts())

else:
    st.info("No stored data yet. Start streaming first.")

st.markdown("---")

# =========================
# 🔴 STREAM CONTROL
# =========================
if "running" not in st.session_state:
    st.session_state.running = False

col1, col2 = st.columns(2)

if col1.button("▶ Start Streaming"):
    st.session_state.running = True

if col2.button("⏹ Stop Streaming"):
    st.session_state.running = False

# =========================
# 📊 LIVE METRICS ROW
# =========================
metric1, metric2, metric3 = st.columns(3)

counter_placeholder = metric1.empty()
safe_placeholder    = metric2.empty()
churn_placeholder   = metric3.empty()

# =========================
# 🚨 ALERT PLACEHOLDER
# =========================
alert_placeholder = st.empty()

# =========================
# 📊 LIVE DATA DISPLAY
# =========================
data_log = []

table_placeholder = st.empty()
chart_placeholder = st.empty()

# =========================
# 🔁 STREAM LOOP
# =========================
while st.session_state.running:

    # 🔥 Realistic pattern generation
    if random.random() < 0.4:
        payload = {
            "age": random.randint(18, 40),
            "session_duration": random.uniform(1, 8),
            "pages_visited": random.randint(1, 5),
            "purchase_amount": random.uniform(0, 120),
            "is_mobile": random.choice([0, 1])
        }
    else:
        payload = {
            "age": random.randint(25, 65),
            "session_duration": random.uniform(15, 60),
            "pages_visited": random.randint(5, 25),
            "purchase_amount": random.uniform(200, 1000),
            "is_mobile": random.choice([0, 1])
        }

    try:
        res = requests.post(API, json=payload, timeout=5)

        if res.status_code == 200:
            output = res.json()

            new_row = {
                "age": payload["age"],
                "prediction": output.get("result", "UNKNOWN"),
                "confidence": round(output.get("confidence", 0), 3)
            }

            data_log.append(new_row)

            # 💾 SAVE TO "CLOUD" (CSV)
            df = pd.DataFrame(data_log)
            df.to_csv("stored_data.csv", index=False)

            total       = len(df)
            safe_count  = len(df[df["prediction"] == "SAFE USER"])
            churn_count = len(df[df["prediction"] == "CHURN RISK"])
            churn_pct   = (churn_count / total) * 100 if total > 0 else 0

            # Metrics
            counter_placeholder.metric("📊 Total Predictions", total)
            safe_placeholder.metric("🟢 Safe Users", safe_count)
            churn_placeholder.metric("🔴 Churn Risk", churn_count)

            # Alert system
            if churn_pct > 40:
                alert_placeholder.error(
                    f"🚨 ALERT — Churn rate is {churn_pct:.1f}%!"
                )
            else:
                alert_placeholder.success(
                    f"✅ Churn rate is {churn_pct:.1f}%"
                )

            # Table (last 50 rows)
            table_placeholder.dataframe(df.tail(50), use_container_width=True)

            # Graph
            df["numeric"] = df["prediction"].apply(
                lambda x: 1 if x == "CHURN RISK" else 0
            )
            chart_placeholder.line_chart(df["numeric"])

        else:
            st.warning("⚠ API returned error")

    except Exception as e:
        st.error(f"API error: {e}")

    time.sleep(1)