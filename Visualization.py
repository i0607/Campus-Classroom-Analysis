import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load the cleaned dataset
df = pd.read_excel("cleaned_data.xlsx")

# Display the first few rows
print(df.head())

# Distribution of Classroom Sizes
plt.figure(figsize=(8, 5))
sns.histplot(df["n_chairs"], bins=10, kde=True, color="blue")
plt.title("Distribution of Classroom Sizes (Number of Chairs)")
plt.xlabel("Number of Chairs")
plt.ylabel("Frequency")


# Number of Classrooms Per Floor
plt.figure(figsize=(8, 5))
sns.countplot(y=df["floor"], order=df["floor"].value_counts().index, palette="viridis")
plt.title("Number of Classrooms Per Floor")
plt.xlabel("Number of Classrooms")
plt.ylabel("Floor")


# Heatmap: Correlation Between Numeric Features
numeric_df = df.select_dtypes(include=['number'])

plt.figure(figsize=(10, 6))
sns.heatmap(numeric_df.corr(), annot=True, cmap="coolwarm", fmt=".2f", linewidths=0.5)
plt.title("Correlation Between Classroom Features")


plt.show()

