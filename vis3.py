import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load your Excel file
df = pd.read_excel("cleaned_data.xlsx")

# Select categorical columns (usually of type 'object')
categorical_df = df.select_dtypes(include='object')

# Set the style for the plots
sns.set(style="whitegrid")

# Plot each categorical feature
for col in categorical_df.columns:
    plt.figure(figsize=(8, 5))
    sns.countplot(data=df, x=col, palette='pastel', order=df[col].value_counts().index)
    plt.title(f'Distribution of {col}')
    plt.xlabel(col)
    plt.ylabel("Count")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()
