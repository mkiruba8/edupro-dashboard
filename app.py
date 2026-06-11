import streamlit as st
import pandas as pd
import plotly.express as px

# -----------------------------------
# PAGE CONFIG
# -----------------------------------

st.set_page_config(
    page_title="EduPro Dashboard",
    page_icon="🎓",
    layout="wide"
)

st.title("🎓 EduPro Learner Analytics Dashboard")

# -----------------------------------
# LOAD DATA
# -----------------------------------

@st.cache_data
def load_data():

    users = pd.read_csv(
        "EduPro Online Platform.xlsx - Users.csv"
    )

    courses = pd.read_csv(
        "EduPro Online Platform.xlsx - Courses.csv"
    )

    transactions = pd.read_csv(
        "EduPro Online Platform.xlsx - Transactions.csv"
    )

    return users, courses, transactions


users, courses, transactions = load_data()

# -----------------------------------
# MERGE TABLES
# -----------------------------------

df = transactions.merge(
    users,
    on="UserID"
)

df = df.merge(
    courses,
    on="CourseID"
)

# -----------------------------------
# CREATE AGE GROUPS
# -----------------------------------

bins = [0, 18, 25, 35, 45, 100]

labels = [
    "<18",
    "18-25",
    "26-35",
    "36-45",
    "45+"
]

df["AgeGroup"] = pd.cut(
    df["Age"],
    bins=bins,
    labels=labels
)

# -----------------------------------
# SIDEBAR FILTERS
# -----------------------------------

st.sidebar.header("Filters")

selected_gender = st.sidebar.multiselect(
    "Gender",
    options=df["Gender"].unique(),
    default=df["Gender"].unique()
)

selected_category = st.sidebar.multiselect(
    "Course Category",
    options=df["CourseCategory"].unique(),
    default=df["CourseCategory"].unique()
)

selected_level = st.sidebar.multiselect(
    "Course Level",
    options=df["CourseLevel"].unique(),
    default=df["CourseLevel"].unique()
)

filtered_df = df[
    (df["Gender"].isin(selected_gender))
    &
    (df["CourseCategory"].isin(selected_category))
    &
    (df["CourseLevel"].isin(selected_level))
]

# -----------------------------------
# KPIs
# -----------------------------------

total_learners = filtered_df["UserID"].nunique()

total_enrollments = len(filtered_df)

avg_courses = round(
    filtered_df.groupby("UserID")
    .size()
    .mean(),
    2
)

top_category = (
    filtered_df["CourseCategory"]
    .value_counts()
    .idxmax()
)

c1, c2, c3, c4 = st.columns(4)

c1.metric(
    "Total Learners",
    total_learners
)

c2.metric(
    "Total Enrollments",
    total_enrollments
)

c3.metric(
    "Avg Courses/User",
    avg_courses
)

c4.metric(
    "Top Category",
    top_category
)

st.markdown("---")

# -----------------------------------
# AGE DISTRIBUTION
# -----------------------------------

st.subheader("Age Distribution")

fig_age = px.histogram(
    filtered_df,
    x="Age",
    nbins=20
)

st.plotly_chart(
    fig_age,
    use_container_width=True
)

# -----------------------------------
# GENDER DISTRIBUTION
# -----------------------------------

st.subheader("Gender Distribution")

gender_data = (
    filtered_df["Gender"]
    .value_counts()
    .reset_index()
)

gender_data.columns = [
    "Gender",
    "Count"
]

fig_gender = px.pie(
    gender_data,
    names="Gender",
    values="Count"
)

st.plotly_chart(
    fig_gender,
    use_container_width=True
)

# -----------------------------------
# CATEGORY POPULARITY
# -----------------------------------

st.subheader("Course Category Popularity")

category_data = (
    filtered_df.groupby("CourseCategory")
    .size()
    .reset_index(name="Enrollments")
)

fig_category = px.bar(
    category_data,
    x="CourseCategory",
    y="Enrollments"
)

st.plotly_chart(
    fig_category,
    use_container_width=True
)

# -----------------------------------
# COURSE LEVEL DISTRIBUTION
# -----------------------------------

st.subheader("Course Level Distribution")

level_data = (
    filtered_df.groupby("CourseLevel")
    .size()
    .reset_index(name="Enrollments")
)

fig_level = px.bar(
    level_data,
    x="CourseLevel",
    y="Enrollments"
)

st.plotly_chart(
    fig_level,
    use_container_width=True
)

# -----------------------------------
# AGE GROUP ENROLLMENTS
# -----------------------------------

st.subheader("Enrollments by Age Group")

age_group_data = (
    filtered_df.groupby("AgeGroup")
    .size()
    .reset_index(name="Enrollments")
)

fig_age_group = px.bar(
    age_group_data,
    x="AgeGroup",
    y="Enrollments"
)

st.plotly_chart(
    fig_age_group,
    use_container_width=True
)

# -----------------------------------
# TOP ACTIVE USERS
# -----------------------------------

st.subheader("Top 10 Active Learners")

top_users = (
    filtered_df.groupby(
        ["UserID", "UserName"]
    )
    .size()
    .reset_index(name="Enrollments")
    .sort_values(
        by="Enrollments",
        ascending=False
    )
    .head(10)
)

st.dataframe(
    top_users,
    use_container_width=True
)

# -----------------------------------
# RAW DATA
# -----------------------------------

with st.expander("View Data"):

    st.dataframe(
        filtered_df,
        use_container_width=True
    )