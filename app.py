import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px

# ----------------------------
# PAGE CONFIG
# ----------------------------
st.set_page_config(page_title="SaaS Data Dashboard", layout="wide")

# ----------------------------
# CUSTOM CSS (SaaS STYLE)
# ----------------------------
st.markdown("""
<style>
.main {
    background-color: #0E1117;
}
.metric-card {
    background-color: #1c1f26;
    padding: 15px;
    border-radius: 10px;
    text-align: center;
}
</style>
""", unsafe_allow_html=True)

st.title("🚀 SaaS Data Visualization Dashboard")

# ----------------------------
# DATA LOADING
# ----------------------------
@st.cache_data
def load_default_data():
    np.random.seed(42)
    return pd.DataFrame({
        "Feature_A": np.random.randn(100),
        "Feature_B": np.random.randn(100),
        "Feature_C": np.random.randint(1, 50, 100),
        "Category": np.random.choice(["X", "Y", "Z"], 100),
        "Group": np.random.choice(["G1", "G2", "G3"], 100)
    })

uploaded_file = st.sidebar.file_uploader("📤 Upload CSV", type=["csv"])

if uploaded_file:
    df = pd.read_csv(uploaded_file)
    st.sidebar.success("Custom dataset loaded ✅")
else:
    df = load_default_data()

# ----------------------------
# COLUMN DETECTION
# ----------------------------
num_cols = df.select_dtypes(include=["number"]).columns.tolist()
cat_cols = df.select_dtypes(include=["object"]).columns.tolist()

# ----------------------------
# SIDEBAR FILTERS
# ----------------------------
st.sidebar.header("🔍 Filters")

selected_num_cols = st.sidebar.multiselect(
    "Select Numeric Columns",
    num_cols,
    default=num_cols[:2] if len(num_cols) >= 2 else num_cols
)

selected_cat = None
if cat_cols:
    selected_cat = st.sidebar.selectbox("Select Category Column", cat_cols)

filtered_df = df.copy()

if selected_cat:
    category_values = st.sidebar.multiselect(
        "Filter Category",
        df[selected_cat].unique(),
        default=df[selected_cat].unique()
    )
    filtered_df = filtered_df[filtered_df[selected_cat].isin(category_values)]

# ----------------------------
# EMPTY CHECK
# ----------------------------
if filtered_df.empty:
    st.warning("No data available after filtering")
    st.stop()

# ----------------------------
# DOWNLOAD BUTTON
# ----------------------------
def convert_df(df):
    return df.to_csv(index=False).encode('utf-8')

st.sidebar.download_button(
    "📥 Download Filtered Data",
    data=convert_df(filtered_df),
    file_name="filtered_data.csv",
    mime="text/csv"
)

# ----------------------------
# KPI CARDS
# ----------------------------
col1, col2, col3 = st.columns(3)

col1.metric("📊 Total Rows", len(filtered_df))
col2.metric("🔢 Numeric Columns", len(num_cols))
col3.metric("🏷️ Categories", len(cat_cols))

st.markdown("---")

# ----------------------------
# TABS
# ----------------------------
tab1, tab2, tab3 = st.tabs(["📄 Data", "📊 Charts", "⚡ Advanced"])

# ----------------------------
# TAB 1: DATA
# ----------------------------
with tab1:
    st.subheader("📄 Data Preview")
    st.dataframe(filtered_df, use_container_width=True)

# ----------------------------
# TAB 2: BASIC CHARTS
# ----------------------------
with tab2:
    col1, col2 = st.columns(2)

    if len(selected_num_cols) >= 1:
        col1.subheader("📈 Line Chart")
        col1.line_chart(filtered_df[selected_num_cols])

        col1.subheader("📊 Bar Chart")
        col1.bar_chart(filtered_df[selected_num_cols])

        col2.subheader("🌊 Area Chart")
        col2.area_chart(filtered_df[selected_num_cols])

    if len(selected_num_cols) >= 2:
        col2.subheader("📦 Box Plot")
        fig, ax = plt.subplots()
        sns.boxplot(data=filtered_df[selected_num_cols], ax=ax)
        col2.pyplot(fig)

# ----------------------------
# TAB 3: ADVANCED
# ----------------------------
with tab3:
    col1, col2 = st.columns(2)

    if len(selected_num_cols) >= 2:
        col1.subheader("🔵 Scatter Plot")
        fig = px.scatter(
            filtered_df,
            x=selected_num_cols[0],
            y=selected_num_cols[1],
            color=selected_cat if selected_cat else None
        )
        col1.plotly_chart(fig, use_container_width=True)

    if len(selected_num_cols) >= 1:
        col1.subheader("📊 Histogram")
        fig, ax = plt.subplots()
        ax.hist(filtered_df[selected_num_cols[0]], bins=30)
        col1.pyplot(fig)

    # Heatmap (SAFE)
    numeric_df = filtered_df.select_dtypes(include=["number"])

    if numeric_df.shape[1] >= 2:
        col2.subheader("🔥 Heatmap")
        fig, ax = plt.subplots()
        sns.heatmap(numeric_df.corr(), annot=True, cmap="coolwarm", ax=ax)
        col2.pyplot(fig)

    # Pie Chart
    if selected_cat:
        col2.subheader("🥧 Pie Chart")
        pie_data = filtered_df[selected_cat].value_counts()
        fig, ax = plt.subplots()
        ax.pie(pie_data, labels=pie_data.index, autopct='%1.1f%%')
        col2.pyplot(fig)

# ----------------------------
# FOOTER
# ----------------------------
st.markdown("---")
st.caption("🚀 SaaS Dashboard | Upload • Filter • Visualize • Download")