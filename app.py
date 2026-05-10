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
# CLEAN DATA
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

dept_cols = ['Engineering Enrolled', 'Business Enrolled', 'Arts Enrolled', 'Science Enrolled']
dept_labels = ['Engineering', 'Business', 'Arts', 'Science']
selected_depts = st.sidebar.multiselect(
    "Select Department",
    options=dept_labels,
    default=dept_labels
)

df_filtered = df[
    (df["Year"].isin(year)) &
    (df["Term"].isin(term))
]

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
    st.subheader("Retention Rate Trend Over Time")
    retention = df_filtered.groupby("Year")[retention_col].mean().reset_index()

    fig, ax = plt.subplots(figsize=(8, 4))
    sns.lineplot(data=retention, x="Year", y=retention_col, marker="o", color="steelblue", ax=ax)
    ax.set_ylabel("Retention (%)")
    ax.set_xlabel("Year")
    st.pyplot(fig)

# ----------------------
# SATISFACTION BY YEAR
# ----------------------
if satisfaction_col:
    st.subheader("Student Satisfaction by Year")
    satisfaction = df_filtered.groupby("Year")[satisfaction_col].mean().reset_index()

    fig, ax = plt.subplots(figsize=(8, 4))
    sns.barplot(data=satisfaction, x="Year", y=satisfaction_col, palette="Blues_d", ax=ax)
    ax.set_ylabel("Satisfaction (%)")
    ax.set_xlabel("Year")
    st.pyplot(fig)

# ----------------------
# SPRING VS FALL COMPARISON
# ----------------------
st.subheader("Spring vs Fall Comparison")

if retention_col and satisfaction_col:
    term_comparison = df_filtered.groupby("Term")[[retention_col, satisfaction_col]].mean().reset_index()

    fig, axes = plt.subplots(1, 2, figsize=(12, 4))

    sns.barplot(data=term_comparison, x="Term", y=retention_col, palette="Set1", ax=axes[0])
    axes[0].set_title("Retention Rate: Spring vs Fall")
    axes[0].set_ylabel("Retention Rate (%)")

    sns.barplot(data=term_comparison, x="Term", y=satisfaction_col, palette="Set1", ax=axes[1])
    axes[1].set_title("Student Satisfaction: Spring vs Fall")
    axes[1].set_ylabel("Satisfaction (%)")

    plt.tight_layout()
    st.pyplot(fig)

# ----------------------
# ENROLLMENT BY TERM (PIE)
# ----------------------
st.subheader("Enrollment Distribution by Term")

term_counts = df_filtered.groupby("Term")["Enrolled"].sum()

fig, ax = plt.subplots()
ax.pie(term_counts, labels=term_counts.index, autopct='%1.1f%%')
ax.set_title("Enrollment Distribution")
st.pyplot(fig)

# ----------------------
# ENROLLMENT BY DEPARTMENT
# ----------------------
st.subheader("Enrollment by Department")

selected_dept_cols = [c for c, l in zip(dept_cols, dept_labels) if l in selected_depts]

if selected_dept_cols:
    dept_totals = df_filtered[selected_dept_cols].sum().reset_index()
    dept_totals.columns = ['Department', 'Total Enrolled']
    dept_totals['Department'] = dept_totals['Department'].str.replace(' Enrolled', '')

    fig, ax = plt.subplots(figsize=(7, 4))
    sns.barplot(data=dept_totals, x="Department", y="Total Enrolled", palette="muted", ax=ax)
    ax.set_ylabel("Total Enrolled")
    ax.set_xlabel("Department")
    plt.tight_layout()
    st.pyplot(fig)
else:
    st.info("Select at least one department to display this chart.")

# ----------------------
# KEY FINDINGS
# ----------------------
st.subheader("Key Findings")

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

st.markdown(
    "> **Actionable insight:** If retention is lower in a specific term or department, "
    "the university could implement targeted early-warning systems and tutoring programs "
    "to intervene before students drop out."
)

# ----------------------
# FOOTER
# ----------------------
st.markdown("---")
st.markdown("Developed by Sheila Daniela Hernandez Carrillo")
