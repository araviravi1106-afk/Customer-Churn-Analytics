"""
E-Commerce Customer Churn Analytics Dashboard
Author: <Your Name>
Description:
    An interactive Streamlit dashboard for exploring, analyzing, and
    understanding customer churn behavior for an e-commerce business.
Run with:
    streamlit run app.py
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

# --------------------------------------------------------------------------
# PAGE CONFIG
# --------------------------------------------------------------------------
st.set_page_config(
    page_title="E-Commerce Customer Churn Dashboard",
    page_icon="🛒",
    layout="wide",
    initial_sidebar_state="expanded",
)

# --------------------------------------------------------------------------
# CUSTOM CSS
# --------------------------------------------------------------------------
st.markdown(
    """
    <style>
    .main {background-color: #f7f9fb;}
    div[data-testid="stMetric"] {
        background-color: #ffffff !important;
        border: 1px solid #e6e6e6;
        border-radius: 12px;
        padding: 14px 12px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.06);
    }
    div[data-testid="stMetric"] * {
        color: #1f2937 !important;
    }
    div[data-testid="stMetricLabel"] {
        color: #4b5563 !important;
        font-weight: 600;
    }
    div[data-testid="stMetricValue"] {
        font-size: 1.5rem !important;
        color: #111827 !important;
    }
    div[data-testid="stMetricDelta"] {
        color: #059669 !important;
    }
    .block-container {padding-top: 1.5rem;}
    h1, h2, h3 {color: #1f2937;}
    </style>
    """,
    unsafe_allow_html=True,
)

DATA_PATH = "ecommerce_customer_churn.csv"

CATEGORICAL_COLS = [
    "Gender", "City", "State", "Membership_Type",
    "Preferred_Category", "Risk_Level",
]
NUMERIC_COLS = [
    "Age", "Total_Orders", "Average_Order_Value", "Total_Spend",
    "Days_Since_Last_Purchase", "Login_Count", "Coupon_Usage",
    "Support_Calls", "Return_Count", "Refund_Amount", "Loyalty_Score",
    "Customer_Lifetime_Value", "Customer_Satisfaction",
]


# --------------------------------------------------------------------------
# DATA LOADING
# --------------------------------------------------------------------------
@st.cache_data(show_spinner="Loading customer data...")
def load_data(path):
    df = pd.read_csv(path)

    # Standardize / coerce types defensively
    if "Join_Date" in df.columns:
        df["Join_Date"] = pd.to_datetime(df["Join_Date"], errors="coerce")

    for col in NUMERIC_COLS:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")

    if "Churn" in df.columns:
        # Normalize churn to 0/1 whether it arrives as Yes/No, True/False, or 1/0
        if df["Churn"].dtype == object:
            df["Churn"] = (
                df["Churn"].astype(str).str.strip().str.lower()
                .map({"yes": 1, "no": 0, "true": 1, "false": 0, "1": 1, "0": 0})
            )
        df["Churn"] = df["Churn"].fillna(0).astype(int)

    df = df.drop_duplicates()
    return df


def kpi_card(label, value, help_text=None):
    st.metric(label, value, help=help_text)


def safe_mean(series):
    return round(series.mean(), 2) if len(series) else 0


# --------------------------------------------------------------------------
# LOAD DATA
# --------------------------------------------------------------------------
try:
    raw_df = load_data(DATA_PATH)
except FileNotFoundError:
    st.error(
        f"Could not find `{DATA_PATH}`. Please place the CSV file in the "
        "same directory as `app.py`, or upload it below."
    )
    uploaded = st.file_uploader("Upload ecommerce_customer_churn.csv", type="csv")
    if uploaded is not None:
        raw_df = load_data(uploaded)
    else:
        st.stop()

# --------------------------------------------------------------------------
# SIDEBAR FILTERS
# --------------------------------------------------------------------------
st.sidebar.title("🛒 Filters")
st.sidebar.caption("Refine the customer base shown across the dashboard.")

df = raw_df.copy()

if "Gender" in df.columns:
    genders = st.sidebar.multiselect(
        "Gender", sorted(df["Gender"].dropna().unique()),
        default=sorted(df["Gender"].dropna().unique()),
    )
    df = df[df["Gender"].isin(genders)]

if "State" in df.columns:
    states = st.sidebar.multiselect(
        "State", sorted(df["State"].dropna().unique()),
        default=sorted(df["State"].dropna().unique()),
    )
    df = df[df["State"].isin(states)]

if "Membership_Type" in df.columns:
    memberships = st.sidebar.multiselect(
        "Membership Type", sorted(df["Membership_Type"].dropna().unique()),
        default=sorted(df["Membership_Type"].dropna().unique()),
    )
    df = df[df["Membership_Type"].isin(memberships)]

if "Risk_Level" in df.columns:
    risk_levels = st.sidebar.multiselect(
        "Risk Level", sorted(df["Risk_Level"].dropna().unique()),
        default=sorted(df["Risk_Level"].dropna().unique()),
    )
    df = df[df["Risk_Level"].isin(risk_levels)]

if "Age" in df.columns and df["Age"].notna().any():
    age_min, age_max = int(df["Age"].min()), int(df["Age"].max())
    age_range = st.sidebar.slider("Age Range", age_min, age_max, (age_min, age_max))
    df = df[(df["Age"] >= age_range[0]) & (df["Age"] <= age_range[1])]

if "Churn" in df.columns:
    churn_filter = st.sidebar.radio(
        "Churn Status", ["All", "Churned Only", "Retained Only"], index=0
    )
    if churn_filter == "Churned Only":
        df = df[df["Churn"] == 1]
    elif churn_filter == "Retained Only":
        df = df[df["Churn"] == 0]

st.sidebar.markdown("---")
st.sidebar.caption(f"Showing **{len(df):,}** of **{len(raw_df):,}** customers")
st.sidebar.download_button(
    "⬇️ Download Filtered Data",
    df.to_csv(index=False).encode("utf-8"),
    file_name="filtered_customers.csv",
    mime="text/csv",
)

# --------------------------------------------------------------------------
# HEADER
# --------------------------------------------------------------------------
st.title("🛒 E-Commerce Customer Churn Analytics Dashboard")
st.caption(
    "An interactive view into customer behavior, satisfaction, and churn risk. "
    "Use the sidebar to filter the customer base."
)

if df.empty:
    st.warning("No customers match the current filter selection.")
    st.stop()

# --------------------------------------------------------------------------
# TOP-LEVEL KPIs
# --------------------------------------------------------------------------
total_customers = len(df)
churn_rate = df["Churn"].mean() * 100 if "Churn" in df.columns else np.nan
avg_clv = safe_mean(df["Customer_Lifetime_Value"]) if "Customer_Lifetime_Value" in df.columns else np.nan
avg_spend = safe_mean(df["Total_Spend"]) if "Total_Spend" in df.columns else np.nan
avg_satisfaction = safe_mean(df["Customer_Satisfaction"]) if "Customer_Satisfaction" in df.columns else np.nan
avg_loyalty = safe_mean(df["Loyalty_Score"]) if "Loyalty_Score" in df.columns else np.nan

k1, k2, k3, k4, k5, k6 = st.columns(6)
with k1:
    kpi_card("Total Customers", f"{total_customers:,}")
with k2:
    kpi_card("Churn Rate", f"{churn_rate:.1f}%")
with k3:
    kpi_card("Avg. CLV", f"₹{avg_clv:,.0f}")
with k4:
    kpi_card("Avg. Total Spend", f"₹{avg_spend:,.0f}")
with k5:
    kpi_card("Avg. Satisfaction", f"{avg_satisfaction:.2f}")
with k6:
    kpi_card("Avg. Loyalty Score", f"{avg_loyalty:.2f}")

st.markdown("---")

# --------------------------------------------------------------------------
# TABS
# --------------------------------------------------------------------------
tab_overview, tab_demo, tab_behavior, tab_churn, tab_risk, tab_data = st.tabs(
    ["📊 Overview", "🧑‍🤝‍🧑 Demographics", "🛍️ Behavior", "⚠️ Churn Analysis", "🚨 Risk & Support", "🗂️ Raw Data"]
)

# ---------------- OVERVIEW ----------------
with tab_overview:
    c1, c2 = st.columns(2)

    with c1:
        if "Churn" in df.columns:
            churn_counts = df["Churn"].map({1: "Churned", 0: "Retained"}).value_counts()
            fig = px.pie(
                names=churn_counts.index, values=churn_counts.values,
                title="Customer Churn Distribution", hole=0.45,
                color=churn_counts.index,
                color_discrete_map={"Churned": "#ef4444", "Retained": "#22c55e"},
            )
            fig.update_traces(textinfo="percent+label")
            st.plotly_chart(fig, use_container_width=True)

    with c2:
        if "Membership_Type" in df.columns:
            mem_counts = df["Membership_Type"].value_counts().reset_index()
            mem_counts.columns = ["Membership_Type", "Count"]
            fig = px.bar(
                mem_counts, x="Membership_Type", y="Count",
                title="Customers by Membership Type", color="Membership_Type",
                text="Count",
            )
            fig.update_layout(showlegend=False)
            st.plotly_chart(fig, use_container_width=True)

    c3, c4 = st.columns(2)
    with c3:
        if "Total_Spend" in df.columns:
            fig = px.histogram(
                df, x="Total_Spend", nbins=40, title="Total Spend Distribution",
                color="Churn" if "Churn" in df.columns else None,
                color_discrete_map={0: "#22c55e", 1: "#ef4444"},
            )
            fig.update_xaxes(tickprefix="₹")
            st.plotly_chart(fig, use_container_width=True)

    with c4:
        if "Customer_Lifetime_Value" in df.columns:
            fig = px.histogram(
                df, x="Customer_Lifetime_Value", nbins=40,
                title="Customer Lifetime Value Distribution",
                color="Churn" if "Churn" in df.columns else None,
                color_discrete_map={0: "#22c55e", 1: "#ef4444"},
            )
            fig.update_xaxes(tickprefix="₹")
            st.plotly_chart(fig, use_container_width=True)

    if "Join_Date" in df.columns and df["Join_Date"].notna().any():
        trend = df.copy()
        trend["Join_Month"] = trend["Join_Date"].dt.to_period("M").astype(str)
        monthly = trend.groupby("Join_Month").size().reset_index(name="New Customers")
        fig = px.line(
            monthly, x="Join_Month", y="New Customers", markers=True,
            title="New Customer Signups Over Time",
        )
        st.plotly_chart(fig, use_container_width=True)

# ---------------- DEMOGRAPHICS ----------------
with tab_demo:
    c1, c2 = st.columns(2)
    with c1:
        if "Gender" in df.columns:
            gender_counts = df["Gender"].value_counts().reset_index()
            gender_counts.columns = ["Gender", "Count"]
            fig = px.pie(gender_counts, names="Gender", values="Count", title="Gender Split", hole=0.4)
            st.plotly_chart(fig, use_container_width=True)

    with c2:
        if "Age" in df.columns:
            fig = px.histogram(
                df, x="Age", nbins=30, title="Age Distribution",
                color="Churn" if "Churn" in df.columns else None,
                color_discrete_map={0: "#22c55e", 1: "#ef4444"},
            )
            st.plotly_chart(fig, use_container_width=True)

    if "State" in df.columns:
        state_counts = df["State"].value_counts().reset_index().head(15)
        state_counts.columns = ["State", "Count"]
        fig = px.bar(
            state_counts, x="Count", y="State", orientation="h",
            title="Top 15 States by Customer Count", text="Count",
        )
        fig.update_layout(yaxis={"categoryorder": "total ascending"})
        st.plotly_chart(fig, use_container_width=True)

    if "City" in df.columns:
        city_counts = df["City"].value_counts().reset_index().head(15)
        city_counts.columns = ["City", "Count"]
        fig = px.bar(
            city_counts, x="Count", y="City", orientation="h",
            title="Top 15 Cities by Customer Count", text="Count",
        )
        fig.update_layout(yaxis={"categoryorder": "total ascending"})
        st.plotly_chart(fig, use_container_width=True)

# ---------------- BEHAVIOR ----------------
with tab_behavior:
    c1, c2 = st.columns(2)
    with c1:
        if "Preferred_Category" in df.columns:
            cat_counts = df["Preferred_Category"].value_counts().reset_index()
            cat_counts.columns = ["Preferred_Category", "Count"]
            fig = px.bar(
                cat_counts, x="Preferred_Category", y="Count",
                title="Preferred Product Category", color="Preferred_Category", text="Count",
            )
            fig.update_layout(showlegend=False)
            st.plotly_chart(fig, use_container_width=True)

    with c2:
        if "Total_Orders" in df.columns and "Average_Order_Value" in df.columns:
            fig = px.scatter(
                df, x="Total_Orders", y="Average_Order_Value",
                color="Churn" if "Churn" in df.columns else None,
                color_discrete_map={0: "#22c55e", 1: "#ef4444"},
                title="Total Orders vs. Average Order Value",
                hover_data=["Customer_ID"] if "Customer_ID" in df.columns else None,
            )
            fig.update_yaxes(tickprefix="₹")
            st.plotly_chart(fig, use_container_width=True)

    c3, c4 = st.columns(2)
    with c3:
        if "Login_Count" in df.columns:
            fig = px.box(
                df, x="Churn" if "Churn" in df.columns else None, y="Login_Count",
                title="Login Count by Churn Status", color="Churn" if "Churn" in df.columns else None,
                color_discrete_map={0: "#22c55e", 1: "#ef4444"},
            )
            st.plotly_chart(fig, use_container_width=True)

    with c4:
        if "Coupon_Usage" in df.columns:
            fig = px.box(
                df, x="Churn" if "Churn" in df.columns else None, y="Coupon_Usage",
                title="Coupon Usage by Churn Status", color="Churn" if "Churn" in df.columns else None,
                color_discrete_map={0: "#22c55e", 1: "#ef4444"},
            )
            st.plotly_chart(fig, use_container_width=True)

    if "Days_Since_Last_Purchase" in df.columns:
        fig = px.histogram(
            df, x="Days_Since_Last_Purchase", nbins=40,
            title="Recency: Days Since Last Purchase",
            color="Churn" if "Churn" in df.columns else None,
            color_discrete_map={0: "#22c55e", 1: "#ef4444"},
        )
        st.plotly_chart(fig, use_container_width=True)

# ---------------- CHURN ANALYSIS ----------------
with tab_churn:
    if "Churn" not in df.columns:
        st.info("No `Churn` column found in the dataset.")
    else:
        c1, c2 = st.columns(2)
        with c1:
            if "Membership_Type" in df.columns:
                grp = df.groupby("Membership_Type")["Churn"].mean().mul(100).reset_index()
                grp.columns = ["Membership_Type", "Churn_Rate_%"]
                fig = px.bar(
                    grp, x="Membership_Type", y="Churn_Rate_%",
                    title="Churn Rate by Membership Type", text_auto=".1f",
                    color="Churn_Rate_%", color_continuous_scale="Reds",
                )
                st.plotly_chart(fig, use_container_width=True)

        with c2:
            if "Preferred_Category" in df.columns:
                grp = df.groupby("Preferred_Category")["Churn"].mean().mul(100).reset_index()
                grp.columns = ["Preferred_Category", "Churn_Rate_%"]
                fig = px.bar(
                    grp, x="Preferred_Category", y="Churn_Rate_%",
                    title="Churn Rate by Preferred Category", text_auto=".1f",
                    color="Churn_Rate_%", color_continuous_scale="Reds",
                )
                st.plotly_chart(fig, use_container_width=True)

        c3, c4 = st.columns(2)
        with c3:
            if "Customer_Satisfaction" in df.columns:
                fig = px.box(
                    df, x="Churn", y="Customer_Satisfaction",
                    title="Customer Satisfaction by Churn Status",
                    color="Churn", color_discrete_map={0: "#22c55e", 1: "#ef4444"},
                )
                st.plotly_chart(fig, use_container_width=True)

        with c4:
            if "Customer_Lifetime_Value" in df.columns:
                fig = px.violin(
                    df, x="Churn", y="Customer_Lifetime_Value", box=True,
                    title="CLV Distribution by Churn Status",
                    color="Churn", color_discrete_map={0: "#22c55e", 1: "#ef4444"},
                )
                fig.update_yaxes(tickprefix="₹")
                st.plotly_chart(fig, use_container_width=True)

        # Correlation heatmap with churn
        numeric_present = [c for c in NUMERIC_COLS if c in df.columns] + ["Churn"]
        corr_df = df[numeric_present].corr(numeric_only=True)
        fig = px.imshow(
            corr_df, text_auto=".2f", aspect="auto",
            color_continuous_scale="RdBu_r", title="Correlation Matrix (Numeric Features)",
        )
        st.plotly_chart(fig, use_container_width=True)

        if "Churn" in corr_df.columns:
            churn_corr = corr_df["Churn"].drop("Churn").sort_values(key=abs, ascending=False)
            fig = px.bar(
                x=churn_corr.values, y=churn_corr.index, orientation="h",
                title="Feature Correlation with Churn",
                labels={"x": "Correlation", "y": "Feature"},
                color=churn_corr.values, color_continuous_scale="RdBu_r",
            )
            fig.update_layout(yaxis={"categoryorder": "total ascending"})
            st.plotly_chart(fig, use_container_width=True)

# ---------------- RISK & SUPPORT ----------------
with tab_risk:
    c1, c2 = st.columns(2)
    with c1:
        if "Risk_Level" in df.columns:
            risk_counts = df["Risk_Level"].value_counts().reset_index()
            risk_counts.columns = ["Risk_Level", "Count"]
            fig = px.pie(
                risk_counts, names="Risk_Level", values="Count",
                title="Customer Risk Level Distribution", hole=0.4,
            )
            st.plotly_chart(fig, use_container_width=True)

    with c2:
        if "Support_Calls" in df.columns:
            fig = px.box(
                df, x="Risk_Level" if "Risk_Level" in df.columns else None,
                y="Support_Calls", title="Support Calls by Risk Level",
                color="Risk_Level" if "Risk_Level" in df.columns else None,
            )
            st.plotly_chart(fig, use_container_width=True)

    c3, c4 = st.columns(2)
    with c3:
        if "Return_Count" in df.columns and "Refund_Amount" in df.columns:
            fig = px.scatter(
                df, x="Return_Count", y="Refund_Amount",
                color="Risk_Level" if "Risk_Level" in df.columns else None,
                title="Returns vs. Refund Amount",
                hover_data=["Customer_ID"] if "Customer_ID" in df.columns else None,
            )
            fig.update_yaxes(tickprefix="₹")
            st.plotly_chart(fig, use_container_width=True)

    with c4:
        if "Loyalty_Score" in df.columns:
            fig = px.histogram(
                df, x="Loyalty_Score", nbins=30, title="Loyalty Score Distribution",
                color="Risk_Level" if "Risk_Level" in df.columns else None,
            )
            st.plotly_chart(fig, use_container_width=True)

    if "Support_Calls" in df.columns and "Churn" in df.columns:
        grp = df.groupby("Support_Calls")["Churn"].mean().mul(100).reset_index()
        grp.columns = ["Support_Calls", "Churn_Rate_%"]
        fig = px.line(
            grp, x="Support_Calls", y="Churn_Rate_%", markers=True,
            title="Churn Rate vs. Number of Support Calls",
        )
        st.plotly_chart(fig, use_container_width=True)

# ---------------- RAW DATA ----------------
with tab_data:
    st.subheader("Filtered Customer Records")
    st.dataframe(df, use_container_width=True, height=500)
    st.caption(f"{len(df):,} rows × {len(df.columns)} columns")

    with st.expander("📈 Summary Statistics"):
        st.dataframe(df.describe(include="all").transpose(), use_container_width=True)

# --------------------------------------------------------------------------
# FOOTER
# --------------------------------------------------------------------------
st.markdown("---")
st.caption(
    "Built with ❤️ using Streamlit & Plotly · "
    f"Data last loaded: {datetime.now().strftime('%Y-%m-%d %H:%M')}"
)