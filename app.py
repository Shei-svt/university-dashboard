import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns

# ----------------------
# PAGE CONFIG
# ----------------------
st.set_page_config(page_title="University Dashboard", layout="wide")

st.title("🎓 University Student Data Dashboard")

# ----------------------
# LOAD DATA
# ----------------------
df = pd.read_csv('university_student_data.csv')

# Clean percentage columns (if needed)
if df["Retention Rate (%)"].dtype == "object":
    df["Retention Rate (%)"] = df["Retention Rate (%)"].str.replace('%', '').astype(float)

if df["Satisfaction (%)"].dtype == "object":
    df["Satisfaction (%)"] = df["Satisfaction (%)"].str.replace('%', '').astype(float)

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

col1.metric("Total Enrolled", int(df_filtered["Enrollment"].sum()))
col2.metric("Avg Retention (%)", round(df_filtered["Retention Rate (%)"].mean(), 1))
col3.metric("Avg Satisfaction (%)", round(df_filtered["Satisfaction (%)"].mean(), 1))

# ----------------------
# RETENTION TREND
# ----------------------
st.subheader("Retention Rate Trend")

retention = df_filtered.groupby("Year")["Retention Rate (%)"].mean().reset_index()

fig, ax = plt.subplots()
sns.lineplot(data=retention, x="Year", y="Retention Rate (%)", marker="o", ax=ax)
ax.set_ylabel("Retention (%)")
ax.set_xlabel("Year")
st.pyplot(fig)

# ----------------------
# SATISFACTION BY YEAR
# ----------------------
st.subheader("Student Satisfaction")

satisfaction = df_filtered.groupby("Year")["Satisfaction (%)"].mean().reset_index()

fig, ax = plt.subplots()
sns.barplot(data=satisfaction, x="Year", y="Satisfaction (%)", ax=ax)
ax.set_ylabel("Satisfaction (%)")
ax.set_xlabel("Year")
st.pyplot(fig)

# ----------------------
# ENROLLMENT BY TERM
# ----------------------
st.subheader("Enrollment by Term")

term_counts = df_filtered["Term"].value_counts()

fig, ax = plt.subplots()
ax.pie(term_counts, labels=term_counts.index, autopct='%1.1f%%')
ax.set_title("Enrollment Distribution")
st.pyplot(fig)

# ----------------------
# INSIGHTS
# ----------------------
st.subheader("Insights")

avg_retention = df_filtered["Retention Rate (%)"].mean()
avg_satisfaction = df_filtered["Satisfaction (%)"].mean()

if avg_retention > 85:
    st.success(f"High retention rate observed ({avg_retention:.1f}%).")
else:
    st.warning(f"Retention rate could be improved ({avg_retention:.1f}%).")

if avg_satisfaction > 80:
    st.info(f"Students show good satisfaction levels ({avg_satisfaction:.1f}%).")
else:
    st.warning(f"Student satisfaction is relatively low ({avg_satisfaction:.1f}%).")

# ----------------------
# FOOTER
# ----------------------
st.markdown("---")
st.markdown("Developed by Sheila Daniela Hernandez Carrillo")
