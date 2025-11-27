import streamlit as st
import pandas as pd
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

# -------------------------------------------------------------------
# Example Streamlit App for Students: Sleep Data Exploration Dashboard
# -------------------------------------------------------------------
# Make sure "Sleep_Efficiency.csv" is in the same folder as this file.

st.title("Sleep Data Exploration Demo App")

st.markdown(
    """
This is an **example Streamlit dashboard** built on a sleep dataset.

Students can:
- Explore how lifestyle factors relate to sleep efficiency
- Practice building plots with Seaborn, Matplotlib, and Plotly
- Replace the explanations with their **own findings and conclusions**
"""
)

st.subheader("1. Load and Preview the Data")

# Load data
df = pd.read_csv("Sleep_Efficiency.csv")

st.write("First few rows of the dataset:")
st.write(df.head())

st.write("Basic dataset info:")
st.write(df.describe())

# -------------------------------------------------------------------
# 2. Smoking vs Sleep Efficiency (Stacked Bar)
# -------------------------------------------------------------------
st.subheader("2. Does smoking relate to sleep efficiency?")

st.markdown(
    """
**Example Question:**  
Does smoking status appear to be related to sleep efficiency?

Below we compute a cross-tabulation between sleep efficiency and smoking status.
Students can change the binning, or try a different plot (e.g., boxplot by group).
"""
)

# Optionally bin sleep efficiency for a clearer bar plot
sleep_bins = [0, 0.6, 0.7, 0.8, 0.9, 1.0]
sleep_labels = ["<0.6", "0.6–0.7", "0.7–0.8", "0.8–0.9", "0.9–1.0"]
df["SleepEff_Bin"] = pd.cut(df["Sleep efficiency"], bins=sleep_bins, labels=sleep_labels)

cross_tab_prop = pd.crosstab(
    index=df["SleepEff_Bin"],
    columns=df["Smoking status"],
    normalize="index"
)

st.write("Proportion of smoking status within each sleep efficiency bin:")
st.dataframe(cross_tab_prop)

fig, ax = plt.subplots(figsize=(8, 5))
cross_tab_prop.plot(kind='bar', stacked=True, ax=ax)
plt.xlabel("Sleep Efficiency Bin")
plt.ylabel("Proportion")
plt.title("Sleep Efficiency vs Smoking Status (Proportions)")
st.pyplot(fig)

st.markdown(
    """
📝 **Example Interpretation (students can edit):**  
It appears that the proportion of smokers is somewhat higher in lower sleep-efficiency bins, 
suggesting smoking *may* be associated with reduced sleep quality.  
Students should check this more carefully using statistics or different visualizations.
"""
)

# -------------------------------------------------------------------
# 3. Age Group vs Sleep Efficiency (Line Plot)
# -------------------------------------------------------------------
st.subheader("3. Does age impact sleep efficiency?")

st.markdown(
    """
We group age into categories and look at the average sleep efficiency for each group.
Students can adjust the age groups or use other plots like boxplots.
"""
)

Age_Group = [
    (9, 21, 'Young'),
    (22, 34, 'Younger Adult'),
    (35, 47, 'Middle Aged'),
    (48, 69, 'Older')
]

def assign_age_group(age):
    for start, end, label in Age_Group:
        if start <= age <= end:
            return label
    return 'Unknown'

df['Age-Group'] = df['Age'].apply(assign_age_group)

fig, ax = plt.subplots()
sns.lineplot(
    data=df,
    x="Age-Group",
    y="Sleep efficiency",
    marker="o",
    estimator="mean",
    ax=ax
)
plt.xlabel("Age Group")
plt.ylabel("Average Sleep Efficiency")
plt.title("Average Sleep Efficiency by Age Group")
st.pyplot(fig)

st.markdown(
    """
📝 **Example Interpretation:**  
In this dataset, older groups appear to have slightly higher average sleep efficiency.  
Students can investigate whether this is due to lifestyle factors, sample bias, or other variables.
"""
)

# -------------------------------------------------------------------
# 4. Bedtime vs Sleep Efficiency
# -------------------------------------------------------------------
st.subheader("4. Does going to bed earlier or later affect sleep efficiency?")

st.markdown(
    """
We convert bedtime to numeric hours and plot it against sleep efficiency.
Students can experiment with different time encodings or transformations.
"""
)

# Convert bedtime and wakeup time to datetime
df["Bedtime_dt"] = pd.to_datetime(df["Bedtime"])
df["Wakeup_dt"] = pd.to_datetime(df["Wakeup time"])

# Convert to hours (0–12) and adjust so late times can be visualized
df["Bedtime_hour"] = (df["Bedtime_dt"].dt.hour % 12) + (df["Bedtime_dt"].dt.minute / 60)
df["Bedtime_hour"] = df["Bedtime_hour"].apply(lambda x: x if x < 12 else x - 12)
df["Bedtime_hour"] = df["Bedtime_hour"].apply(lambda x: x * -1 if x > 6 else x)

fig, ax = plt.subplots()
sns.lineplot(data=df, x="Bedtime_hour", y="Sleep efficiency", ax=ax)
plt.xlabel("Bedtime (transformed hours)")
plt.ylabel("Sleep Efficiency")
plt.title("Sleep Efficiency vs. Bedtime")
ax.tick_params(axis='x', labelsize=8)
st.pyplot(fig)

st.markdown(
    """
📝 **Example Interpretation:**  
There is a slight trend where earlier bedtimes correspond to higher sleep efficiency, 
but the relationship is noisy. Students can try smoothing, regression, or binning bedtimes.
"""
)

# -------------------------------------------------------------------
# 5. Exercise Frequency vs Sleep Efficiency
# -------------------------------------------------------------------
st.subheader("5. Does exercise frequency relate to sleep efficiency?")

fig, ax = plt.subplots()
sns.lineplot(data=df, x="Exercise frequency", y="Sleep efficiency", ax=ax)
plt.xlabel("Exercise Frequency")
plt.ylabel("Sleep Efficiency")
plt.title("Sleep Efficiency vs Exercise Frequency")
ax.tick_params(axis='x', labelsize=8)
st.pyplot(fig)

st.markdown(
    """
📝 **Example Interpretation:**  
The plot suggests that more frequent exercise may be associated with higher sleep efficiency.  
Students should confirm by computing correlation or comparing group means.
"""
)

# -------------------------------------------------------------------
# 6. Caffeine vs Sleep (Plotly Scatter)
# -------------------------------------------------------------------
st.subheader("6. How does caffeine consumption relate to sleep efficiency?")

fig = px.scatter(
    df,
    x="Sleep efficiency",
    y="Caffeine consumption",
    color="Gender",
    title="Caffeine Consumption vs Sleep Efficiency"
)
st.plotly_chart(fig, use_container_width=True)

st.markdown(
    """
📝 **Example Interpretation:**  
The points look quite spread out, and there is no obvious simple correlation by eye.  
Students can compute correlation coefficients or try alternative visualizations.
"""
)

# -------------------------------------------------------------------
# 7. REM Sleep vs Caffeine
# -------------------------------------------------------------------
st.subheader("7. Do people with less REM sleep drink more caffeine?")

fig = px.scatter(
    df,
    x="Caffeine consumption",
    y="REM sleep percentage",
    color="Gender",
    title="REM Sleep Percentage vs Caffeine Consumption"
)
st.plotly_chart(fig, use_container_width=True)

st.markdown(
    """
📝 **Example Interpretation:**  
Again, the relationship appears weak in this dataset.  
Students can test this formally or segment by age, gender, or other factors.
"""
)

# -------------------------------------------------------------------
# 8. Age Group vs Bedtime (Facet Histogram)
# -------------------------------------------------------------------
st.subheader("8. Is age related to bedtime?")

# Reuse Bedtime_hour from above
fig, ax = plt.subplots()
sns.histplot(data=df, x="Bedtime_hour", hue="Age-Group", multiple="stack", ax=ax)
plt.xlabel("Bedtime (transformed hours)")
plt.ylabel("Count")
plt.title("Distribution of Bedtime by Age Group")
st.pyplot(fig)

st.markdown(
    """
📝 **Example Interpretation:**  
Different age groups may have different bedtime distributions.  
Students can refine this by using separate subplots or faceting.
"""
)

# -------------------------------------------------------------------
# 9. Gender vs Sleep Efficiency and Duration
# -------------------------------------------------------------------
st.subheader("9. Does gender play a role in sleep efficiency or duration?")

fig, ax = plt.subplots()
sns.histplot(
    data=df,
    x="Sleep efficiency",
    hue="Gender",
    multiple="stack",
    ax=ax
)
plt.xlabel("Sleep Efficiency")
plt.ylabel("Count")
plt.title("Sleep Efficiency by Gender")
st.pyplot(fig)

fig, ax = plt.subplots()
sns.histplot(
    data=df,
    x="Sleep duration",
    hue="Gender",
    multiple="stack",
    ax=ax
)
plt.xlabel("Sleep Duration (hours)")
plt.ylabel("Count")
plt.title("Sleep Duration by Gender")
st.pyplot(fig)

st.markdown(
    """
📝 **Example Interpretation:**  
The distributions by gender appear fairly similar.  
Students can compute summary statistics (mean, median, variance) to quantify differences.
"""
)

# -------------------------------------------------------------------
# 10. Conclusion Section
# -------------------------------------------------------------------
st.subheader("10. Conclusion (Students Write Here)")

st.markdown(
    """
This section is intentionally left for **students** to summarize their findings.

You might answer questions like:
- Which factors seem most strongly related to sleep efficiency?
- Which relationships were weaker or surprising?
- What limitations does this dataset have?
- What further analysis would you do?

✏️ *Edit this text in the source code to write your own conclusions.*
"""
)
