import streamlit as st
import pandas as pd
import plotly.express as px
from algorithms import compare_algorithms, max_profit_k, prepare_data
from auth import login, register

st.set_page_config(page_title="Stock Market Trend Analyzer", page_icon="📈", layout="wide")

st.markdown("""
<style>
.stApp {background: #0b1220; color: #e8eef8;}
[data-testid="stSidebar"] {background: #111c2e;}
h1,h2,h3 {color:#e8eef8;}
div[data-testid="stMetric"] {background:#142238;padding:16px;border-radius:12px;border:1px solid #263a55;}
.stButton>button {background:#19a889;color:white;border:0;border-radius:8px;}
</style>
""", unsafe_allow_html=True)

if "users" not in st.session_state:
    st.session_state.users = {"demo": "demo123"}
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "prices" not in st.session_state:
    st.session_state.prices = pd.DataFrame({
        "Date": pd.date_range("2025-01-01", periods=15, freq="D"),
        "Close": [63, 65, 62, 70, 68, 75, 72, 63, 81, 99, 119, 112, 124, 130, 127]
    })
if "history" not in st.session_state:
    st.session_state.history = []

def show_auth():
    st.title("📈 Stock Market Trend Analyzer")
    st.caption("DAA · Maximum Subarray · Kadane's · Divide-and-Conquer · Dynamic Programming")
    tab1, tab2 = st.tabs(["Login", "Register"])
    with tab1:
        with st.form("login_form"):
            username = st.text_input("Username")
            password = st.text_input("Password", type="password")
            submitted = st.form_submit_button("Login", use_container_width=True)
        if submitted:
            if login(st.session_state.users, username, password):
                st.session_state.logged_in = True
                st.session_state.username = username
                st.rerun()
            else:
                st.error("Invalid username or password.")
        st.info("Demo access: username `demo`, password `demo123`")
    with tab2:
        with st.form("register_form"):
            new_user = st.text_input("Create username")
            new_pass = st.text_input("Create password", type="password")
            confirm = st.text_input("Confirm password", type="password")
            submitted = st.form_submit_button("Create account", use_container_width=True)
        if submitted:
            message = register(st.session_state.users, new_user, new_pass, confirm)
            if message == "ok":
                st.success("Account created. Please log in.")
            else:
                st.error(message)

if not st.session_state.logged_in:
    show_auth()
    st.stop()

with st.sidebar:
    st.title("MARKETMIND")
    st.caption("ALGORITHM LAB · CSA 0617")
    page = st.radio("WORKSPACE", [
        "Overview", "Stock Data Collection", "Data Preprocessing",
        "Best Buy–Sell Analysis", "Algorithm Comparison",
        "Multiple Transactions", "Results & Visualization",
        "Reports & History", "About Project"
    ])
    st.divider()
    st.caption(f"Signed in as **{st.session_state.username}**")
    if st.button("Log out", use_container_width=True):
        st.session_state.logged_in = False
        st.rerun()

prices = st.session_state.prices.copy()
prepared = prepare_data(prices)

def set_prices(df):
    st.session_state.prices = df

if page == "Overview":
    st.title("Stock Market Trend Analysis")
    st.write("Find the strongest profit window from historical daily stock prices.")
    best = compare_algorithms(prepared["change"].dropna().tolist())
    c1,c2,c3 = st.columns(3)
    c1.metric("Latest closing price", f"{prices.Close.iloc[-1]:.2f}")
    c2.metric("Maximum single-transaction profit", f"{best['Kadane']['profit']:.2f}")
    c3.metric("Trading days", len(prices))
    st.subheader("Price trend")
    st.plotly_chart(px.line(prices, x="Date", y="Close", markers=True, title="Historical closing prices"), use_container_width=True)
    st.info("Use the sidebar to upload stock data, preprocess prices, compare algorithms and explore multiple transactions.")

elif page == "Stock Data Collection":
    st.title("Stock Data Collection")
    st.write("Upload a CSV containing at least a `Close` column. An optional `Date` column is supported.")
    uploaded = st.file_uploader("Upload stock price CSV", type=["csv"])
    if uploaded:
        try:
            df = pd.read_csv(uploaded)
            if "Close" not in df.columns:
                st.error("CSV must contain a column named Close.")
            else:
                if "Date" not in df.columns:
                    df["Date"] = range(1, len(df)+1)
                df = df[["Date","Close"]].copy()
                df["Close"] = pd.to_numeric(df["Close"], errors="coerce")
                df = df.dropna(subset=["Close"]).reset_index(drop=True)
                if len(df) < 2:
                    st.error("Please upload at least two valid closing prices.")
                else:
                    set_prices(df)
                    st.success(f"Loaded {len(df)} valid price records.")
        except Exception as e:
            st.error(f"Could not read CSV: {e}")
    a,b = st.columns(2)
    if a.button("Load sample dataset"):
        set_prices(pd.DataFrame({"Date":pd.date_range("2025-01-01", periods=15, freq="D"),
            "Close":[63,65,62,70,68,75,72,63,81,99,119,112,124,130,127]}))
        st.success("Sample data loaded.")
    if b.button("Download current data as CSV"):
        st.download_button("Download CSV", prices.to_csv(index=False), "stock_prices.csv", "text/csv")
    st.dataframe(st.session_state.prices, use_container_width=True)

elif page == "Data Preprocessing":
    st.title("Data Preprocessing")
    st.write("Daily change = Current closing price − Previous closing price.")
    st.dataframe(prepared, use_container_width=True)
    st.plotly_chart(px.bar(prepared.dropna(), x="Date", y="change",
        color=prepared.dropna()["change"].apply(lambda x: "Gain" if x >= 0 else "Loss"),
        title="Daily gains and losses"), use_container_width=True)
    st.caption("Preprocessing takes O(n) time because each daily change is calculated once.")

elif page == "Best Buy–Sell Analysis":
    st.title("Best Buy–Sell Analysis")
    changes = prepared["change"].dropna().tolist()
    results = compare_algorithms(changes)
    selected = st.selectbox("Choose algorithm", ["Kadane", "Divide and Conquer", "Brute Force"])
    result = results[selected]
    st.metric("Maximum profit", f"{result['profit']:.2f}")
    if result["profit"] > 0:
        st.write(f"Buy on **{prepared.iloc[result['start']]['Date']}** at **{prices.iloc[result['start']]['Close']:.2f}**")
        st.write(f"Sell on **{prepared.iloc[result['end']+1]['Date']}** at **{prices.iloc[result['end']+1]['Close']:.2f}**")
    else:
        st.warning("No profitable buy–sell period was found in this dataset.")
    st.caption(f"Time complexity: {result['complexity']}")

elif page == "Algorithm Comparison":
    st.title("Algorithm Comparison")
    results = compare_algorithms(prepared["change"].dropna().tolist())
    rows = [{"Algorithm":name, "Maximum profit":val["profit"], "Time complexity":val["complexity"],
             "Measured runtime (ms)":round(val["runtime_ms"],4)} for name,val in results.items()]
    st.dataframe(pd.DataFrame(rows), use_container_width=True)
    st.plotly_chart(px.bar(pd.DataFrame(rows), x="Algorithm", y="Measured runtime (ms)",
        title="Measured execution time"), use_container_width=True)
    profits = {round(v["profit"],8) for v in results.values()}
    if len(profits) == 1:
        st.success("Correctness check passed: all three algorithms return the same maximum profit.")
    else:
        st.warning("The algorithms returned different profits; inspect the input data.")

elif page == "Multiple Transactions":
    st.title("Multiple Transactions")
    st.write("Dynamic programming calculates maximum profit using at most k buy–sell transactions.")
    k = st.slider("Maximum transactions (k)", 1, 5, 2)
    profit = max_profit_k(prices["Close"].tolist(), k)
    st.metric(f"Maximum profit with at most {k} transactions", f"{profit:.2f}")
    rows = [{"k":i, "Maximum profit":max_profit_k(prices["Close"].tolist(),i)} for i in range(1,6)]
    st.dataframe(pd.DataFrame(rows), use_container_width=True)
    st.plotly_chart(px.line(pd.DataFrame(rows), x="k", y="Maximum profit", markers=True,
        title="Profit by transaction limit"), use_container_width=True)
    st.caption("Dynamic programming time complexity: O(n × k).")

elif page == "Results & Visualization":
    st.title("Results & Visualization")
    st.plotly_chart(px.line(prices, x="Date", y="Close", markers=True, title="Closing price history"), use_container_width=True)
    st.plotly_chart(px.bar(prepared.dropna(), x="Date", y="change", title="Daily price changes"), use_container_width=True)
    result = compare_algorithms(prepared["change"].dropna().tolist())["Kadane"]
    st.metric("Best single transaction profit", f"{result['profit']:.2f}")
    if st.button("Save this analysis to history"):
        st.session_state.history.append({"Records":len(prices),"Best profit":result["profit"],"Algorithm":"Kadane"})
        st.success("Analysis saved in this session.")

elif page == "Reports & History":
    st.title("Reports & History")
    if not st.session_state.history:
        st.info("No saved analyses in this session yet. Save an analysis from Results & Visualization.")
    else:
        history = pd.DataFrame(st.session_state.history)
        st.dataframe(history, use_container_width=True)
        st.download_button("Download report CSV", history.to_csv(index=False), "analysis_report.csv", "text/csv")

elif page == "About Project":
    st.title("About the Project")
    st.write("This project analyzes historical stock prices to identify the maximum profit buy–sell period using classic Design and Analysis of Algorithms techniques.")
    st.subheader("Algorithms used")
    st.markdown("""
    - **Brute Force — O(n²):** checks every possible buy–sell pair.
    - **Divide and Conquer — O(n log n):** compares the best left, right and crossing subarrays.
    - **Kadane's Algorithm — O(n):** finds the maximum subarray in one pass.
    - **Dynamic Programming — O(n × k):** supports up to k transactions (k = 1 to 5).
    """)
    st.subheader("Project modules")
    st.markdown("1. Price Data Collection & Preprocessing  \n2. Best Buy–Sell Period  \n3. Multiple Transactions & Analysis")
    st.subheader("Future scope")
    st.markdown("- Live market-data API integration\n- Brokerage fees and taxes\n- Larger datasets and benchmarking\n- User-defined alerts")
    st.caption("DAA Project · CSA 0617")
