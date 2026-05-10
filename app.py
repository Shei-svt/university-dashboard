import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
 
# ----------------------
# PAGE CONFIG
# ----------------------
st.set_page_config(page_title="University Dashboard", layout="wide")
st.title("University Student Data Dashboard")
 
# ----------------------
# LOAD DATA
# ----------------------
df = pd.read_csv('university_student_data.csv')
 
# ----------------------
# CLEAN COLUMN NAMES
# ----------------------
df.columns = df.columns.str.strip()
 
# ----------------------
# DETECT IMPORTANT COLUMNS
# ----------------------
retention_col = None
satisfaction_col = None
 
for col in df.columns:
    if "retention" in col.lower():
        retention_col = col
    if "satisfaction" in col.lower():
        satisfaction_col = col
 
# ----------------------
# CLEAN DATA (SAFE)
# ----------------------
if retention_col and df[retention_col].dtype == "object":
    df[retention_col] = df[retention_col].str.replace('%', '').astype(float)
 
if satisfaction_col and df[satisfaction_col].dtype == "object":
    df[satisfaction_col] = df[satisfaction_col].str.replace('%', '').astype(float)
 
# ----------------------
# SIDEBAR FILTERS
# ----------------------
st.sidebar.header("Filters")
 
year = st.sidebar.multiselect(
    "Select Year",
    options=sorted(df["Year"].unique()),
    default=sorted(df["Year"].unique())
)
 
term = st.sidebar.multiselect(
    "Select Term",
    options=df["Term"].unique(),
    default=df["Term"].unique()
)
 
df_filtered = df[
    (df["Year"].isin(year)) &
    (df["Term"].isin(term))
]
 
# ----------------------
# HANDLE EMPTY DATA
# ----------------------
if df_filtered.empty:
    st.warning("No data available for selected filters.")
    st.stop()
 
# ----------------------
# KPIs
# ----------------------
st.subheader("Key Metrics")
 
col1, col2, col3 = st.columns(3)
 
col1.metric("Total Enrolled", int(df_filtered["Enrolled"].sum()))
 
if retention_col:
    col2.metric("Avg Retention (%)", round(df_filtered[retention_col].mean(), 1))
 
if satisfaction_col:
    col3.metric("Avg Satisfaction (%)", round(df_filtered[satisfaction_col].mean(), 1))
 
# ----------------------
# RETENTION TREND
# ----------------------
if retention_col:
    st.subheader("Retention Rate Trend")
 
    retention = df_filtered.groupby("Year")[retention_col].mean().reset_index()
 
    fig, ax = plt.subplots()
    sns.lineplot(data=retention, x="Year", y=retention_col, marker="o", ax=ax)
    ax.set_ylabel("Retention (%)")
    ax.set_xlabel("Year")
    st.pyplot(fig)
 
# ----------------------
# SATISFACTION BY YEAR
# ----------------------
if satisfaction_col:
    st.subheader("Student Satisfaction")
 
    satisfaction = df_filtered.groupby("Year")[satisfaction_col].mean().reset_index()
 
    fig, ax = plt.subplots()
    sns.barplot(data=satisfaction, x="Year", y=satisfaction_col, ax=ax)
    ax.set_ylabel("Satisfaction (%)")
    ax.set_xlabel("Year")
    st.pyplot(fig)
 
# ----------------------
# ENROLLMENT BY TERM
# ----------------------
st.subheader("Enrollment by Term")
 
term_counts = df_filtered.groupby("Term")["Enrolled"].sum()
 
fig, ax = plt.subplots()
ax.pie(term_counts, labels=term_counts.index, autopct='%1.1f%%')
ax.set_title("Enrollment Distribution by Term")
st.pyplot(fig)
 
# ----------------------
# SPRING vs FALL COMPARISON
# ----------------------
st.subheader("Spring vs Fall Comparison")
 
if retention_col and satisfaction_col:
    term_comparison = df_filtered.groupby("Term")[[retention_col, satisfaction_col]].mean().reset_index()
 
    fig, ax = plt.subplots()
    x = range(len(term_comparison))
    width = 0.35
    ax.bar([i - width/2 for i in x], term_comparison[retention_col], width, label="Retention (%)")
    ax.bar([i + width/2 for i in x], term_comparison[satisfaction_col], width, label="Satisfaction (%)")
    ax.set_xticks(list(x))
    ax.set_xticklabels(term_comparison["Term"])
    ax.set_ylabel("Percentage")
    ax.legend()
    st.pyplot(fig)
 
# ----------------------
# INSIGHTS
# ----------------------
st.subheader("Insights")
 
if retention_col:
    avg_retention = df_filtered[retention_col].mean()
    if avg_retention > 85:
        st.success(f"High retention rate observed ({avg_retention:.1f}%).")
    else:
        st.warning(f"Retention rate could be improved ({avg_retention:.1f}%).")
 
if satisfaction_col:
    avg_satisfaction = df_filtered[satisfaction_col].mean()
    if avg_satisfaction > 80:
        st.info(f"Students show good satisfaction levels ({avg_satisfaction:.1f}%).")
    else:
        st.warning(f"Student satisfaction is relatively low ({avg_satisfaction:.1f}%).")
 
# ----------------------
# FOOTER
# ----------------------
st.markdown("---")
st.markdown("Developed by Sheila Daniela Hernandez Carrillo")
