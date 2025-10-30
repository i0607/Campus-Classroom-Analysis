import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load the cleaned dataset
df = pd.read_excel("cleaned_data.xlsx")

# Select numeric data for heatmap
numeric_df = df.select_dtypes(include=['number'])

# Create a single figure with subplots
fig, axes = plt.subplots(2, 2, figsize=(15, 10))
fig.suptitle("Classroom Data Visualizations", fontsize=16)

# Distribution of Classroom Sizes (Histogram)
sns.histplot(df["n_chairs"], bins=10, kde=True, color="blue", ax=axes[0, 0])
axes[0, 0].set_title("Distribution of Classroom Sizes")
axes[0, 0].set_xlabel("Number of Chairs")
axes[0, 0].set_ylabel("Frequency")

# Number of Classrooms Per Floor (Countplot)
sns.countplot(y=df["floor"], order=df["floor"].value_counts().index, palette="viridis", ax=axes[0, 1])
axes[0, 1].set_title("Number of Classrooms Per Floor")
axes[0, 1].set_xlabel("Number of Classrooms")
axes[0, 1].set_ylabel("Floor")

# Heatmap: Correlation Between Numeric Features
sns.heatmap(numeric_df.corr(), annot=True, cmap="coolwarm", fmt=".2f", linewidths=0.5, ax=axes[1, 0])
axes[1, 0].set_title("Correlation Between Classroom Features")

# Hide the empty subplot (axes[1,1]) if you're using a 2x2 layout
axes[1, 1].axis('off')

# Adjust layout
plt.tight_layout(rect=[0, 0.03, 1, 0.95])  # leave space for the suptitle
plt.show()
