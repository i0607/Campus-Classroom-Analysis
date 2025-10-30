import pandas as pd

# Load the original and cleaned datasets
original_file = "Data Science Classroom Data.xlsx"
cleaned_file = "cleaned_data.xlsx"

df_original = pd.read_excel(original_file, sheet_name="Classroom Data")
df_cleaned = pd.read_excel(cleaned_file)

# 🛠 Step 1: Standardize Column Names (Trim Spaces)
df_original.columns = df_original.columns.str.strip()
df_cleaned.columns = df_cleaned.columns.str.strip()

# 🛠 Step 2: Ensure Both DataFrames Have the Same Columns
common_columns = df_original.columns.intersection(df_cleaned.columns)  # Find common columns
df_original = df_original[common_columns]  # Keep only matching columns
df_cleaned = df_cleaned[common_columns]  # Keep only matching columns

# 🛠 Step 3: Reset Indexes to Align Data Properly
df_original.reset_index(drop=True, inplace=True)
df_cleaned.reset_index(drop=True, inplace=True)

# 🟢 Now Compare
diff = (df_original != df_cleaned).sum()
print("\n🔍 Columns with Modified Values:\n", diff[diff > 0])
print("Columns only in Original:", set(df_original.columns) - set(df_cleaned.columns))
print("Columns only in Cleaned:", set(df_cleaned.columns) - set(df_original.columns))
