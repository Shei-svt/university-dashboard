import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns

# ----------------------
# PAGE CONFIGURATION
# ----------------------
st.set_page_config(page_title="University Dashboard", layout="wide")

st.title("University Student Data Dashboard")

# ----------------------
# LOAD DATA
# ----------------------
df = pd.read_csv("university_student_data.csv")

# ----------------------
# SIDEBAR FILTERS
# ----------------------
st.sidebar.header("Filters")

selected_years = st.sidebar.multiselect(
    "Select Year",
    options=df["Year"].unique(),
    default=df["Year"].unique()
)

selected_terms = st.sidebar.multiselect(
    "Select Term",
    options=df["Term"].unique(),
    default=df["Term"].unique()
)

# Apply filters
df_filtered = df[
    (df["Year"].isin(selected_years)) &
    (df["Term"].isin(selected_terms))
]

# ----------------------
# KPIs
# ----------------------
st.subheader("Key Metrics")

col1, col2, col3 = st.columns(3)

col1.metric("Total Enrolled", int(df_filtered["Enrolled"].sum()))
col2.metric("Avg Retention (%)", round(df_filtered["Retention Rate (%)"].mean(), 2))
col3.metric("Avg Satisfaction (%)", round(df_filtered["Student Satisfaction (%)"].mean(), 2))

# ----------------------
# RETENTION TREND
# ----------------------
st.subheader("Retention Rate Trend")

df_retention = (
    df_filtered.groupby("Year")["Retention Rate (%)"]
    .mean()
    .reset_index()
)

fig1, ax1 = plt.subplots()
sns.lineplot(
    data=df_retention,
    x="Year",
    y="Retention Rate (%)",
    marker="o",
    ax=ax1
)

ax1.set_title("Retention Rate Over Time")
ax1.set_ylabel("Retention (%)")

st.pyplot(fig1)

# ----------------------
# STUDENT SATISFACTION
# ----------------------
st.subheader("Student Satisfaction")

df_satisfaction = (
    df_filtered.groupby("Year")["Student Satisfaction (%)"]
    .mean()
    .reset_index()
)

fig2, ax2 = plt.subplots()
sns.barplot(
    data=df_satisfaction,
    x="Year",
    y="Student Satisfaction (%)",
    ax=ax2
)

ax2.set_title("Average Satisfaction by Year")
ax2.set_ylabel("Satisfaction (%)")

st.pyplot(fig2)

# ----------------------
# ENROLLMENT BY TERM
# ----------------------
st.subheader("Enrollment by Term")

df_term = (
    df_filtered.groupby("Term")["Enrolled"]
    .mean()
    .reset_index()
)

fig3, ax3 = plt.subplots()
sns.barplot(
    data=df_term,
    x="Term",
    y="Enrolled",
    ax=ax3
)

ax3.set_title("Average Enrollment by Term")

st.pyplot(fig3)