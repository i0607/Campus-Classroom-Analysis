import pandas as pd
import numpy as np 
import re
import matplotlib.pyplot as plt
import seaborn as sns

# Load the dataset
file_path = "Data Science Classroom Data.xlsx"  
df = pd.read_excel(file_path, sheet_name="Classroom Data")

# Step 1: Cleaning column names (remove spaces & fix names)
df.columns = df.columns.str.strip()  

# Step 2: Rename columns for consistency
column_renames = {
    "Ligting": "Lighting",
    "Cleaning service": "Cleaning Service",  
    "Interior Deign": "Interior Design",
    "Uage Timing": "Usage Timing",
    "m_entr_distance": "Main Entrance Distance",
    "wifi_connec": "WiFi Connection"
}
df.rename(columns=column_renames, inplace=True)

# Defining numerical columns for later use in duplicate handling
numerical_cols = ["n_chairs", "n_aircon", "n_windows", "Lighting", "socket", "Nbr of cameras", "Nbr of doors"]
numeric_int_cols = ["n_chairs", "Nbr of cameras", "Nbr of doors", "n_aircon", "n_windows", "socket"]

# Step 3: Handling non-numeric values in columns that should be numeric
# Clean n_aircon first to handle cases like "2 (just for hot weather)"
if "n_aircon" in df.columns:
    df["n_aircon"] = df["n_aircon"].astype(str).str.strip()
    # Extract just the numbers
    df["n_aircon"] = df["n_aircon"].str.extract(r'(\d+)').fillna('')
    # Convert to numeric
    df["n_aircon"] = pd.to_numeric(df["n_aircon"], errors='coerce')


numeric_cols_to_clean = ["n_chairs", "Nbr of cameras", "Nbr of doors", 
                         "n_windows", "socket", "Lighting"]

for col in numeric_cols_to_clean:
    if col in df.columns:
        # Convert to string first to handle any non-string values
        df[col] = df[col].astype(str).str.strip()
        # Extract just the numbers using regex
        df[col] = df[col].str.extract(r'(\d+(?:\.\d+)?)').fillna('')
        # Convert to numeric
        df[col] = pd.to_numeric(df[col], errors='coerce')


# Fill numerical values with mean/median
df["n_chairs"] = df["n_chairs"].fillna(df["n_chairs"].median())
df["Nbr of cameras"] = df["Nbr of cameras"].fillna(df["Nbr of cameras"].median())
df["Nbr of doors"] = df["Nbr of doors"].fillna(df["Nbr of doors"].median())
df["n_aircon"] = df["n_aircon"].fillna(df["n_aircon"].median())
df["socket"] = df["socket"].fillna(df["socket"].median())
df["n_windows"] = df["n_windows"].fillna(df["n_windows"].median())

# Fill categorical values with mode
categorical_cols = ["Cleaning Service", "WiFi Connection", "Seats disposition", 
                   "Interior Design", "maintenance", "Cyberpower", "Main Entrance Distance", "Noise Level"]
for col in categorical_cols:
    if col in df.columns: 
        df[col] = df[col].fillna(df[col].mode()[0] if not df[col].mode().empty else "Unknown")

# Step 4: Convert data types
# Convert numerical columns to integers
for col in numeric_int_cols:
    if col in df.columns:
        df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0).astype(int)

# Convert yes/no/TRUE/FALSE to boolean values consistently
boolean_cols = ["has_blinds", "has_smartboard", "has_computer", "Exit banner"]
boolean_mapping = {
    "yes": True, "no": False, "Yes": True, "NO": False, "No": False, 
    "TRUE": True, "FALSE": False, "YES": True, "True": True, "False": False
}

for col in boolean_cols:
    if col in df.columns:
        df[col] = df[col].map(boolean_mapping)
        # Fill any remaining NaN values with the most common value (mode)
        most_common = df[col].mode()[0] if not df[col].mode().empty else False
        df[col] = df[col].fillna(most_common)

# ✅ Floor Column Formatting ✅
if "floor" in df.columns:
    df["floor"] = df["floor"].astype(str).str.lower().str.strip() 

    # Standardize floor names
    floor_mapping = {
        "first": "1 floor",
        "second": "2 floor",
        "third": "3 floor",
        "ground floor": "0 floor",
        "1st": "1 floor",
        "2nd": "2 floor",
        "2nd floor": "2 floor",
        "2 nd": "2 floor",
        "3rd": "3 floor",
        "0": "0 floor",
        "-1": "-1 floor"
    }

    # Replace variations
    df["floor"] = df["floor"].replace(floor_mapping)

    # Ensure all numeric floors have the word "floor"
    df["floor"] = df["floor"].apply(lambda x: f"{x} floor" if x.lstrip('-').isdigit() else x)

    # Remove any accidental dots or extra symbols
    df["floor"] = df["floor"].str.replace(r"\.", "", regex=True)

    # Ensure a single space between number and 'floor'
    df["floor"] = df["floor"].str.replace(r"(\d+)-?\s*floor", r"\1 floor", regex=True)
    
    # Create a numeric floor field for analysis
    df["floor_number"] = df["floor"].str.extract(r"(-?\d+)").astype(float)

# ✅ Classroom Column Formatting ✅
if "classroom" in df.columns: 
    df["classroom"] = df["classroom"].astype(str).str.upper()  
    
    # Remove all special characters and spaces 
    df["classroom"] = df["classroom"].apply(lambda x: re.sub(r"[^A-Z0-9]", "", x))
    
# ✅ Lighting Column Formatting ✅
if "Lighting" in df.columns: 
    df["Lighting"] = df["Lighting"].astype(str)
    
    # Extract only the first number found in the string
    df["Lighting"] = df["Lighting"].apply(lambda x: re.search(r"\d+", x).group() if re.search(r"\d+", x) else "")

    # Convert to numeric, setting non-numeric values to NaN
    df["Lighting"] = pd.to_numeric(df["Lighting"], errors="coerce")
    
    # Fill missing values with median
    df["Lighting"] = df["Lighting"].fillna(df["Lighting"].median())

# ✅ Noise Level Standardization ✅
if "Noise Level" in df.columns:  
    df["Noise Level"] = df["Noise Level"].astype(str).str.lower().str.strip()  

    # Extract only 'high', 'low', or 'moderate' from the text
    noise_pattern = r"\b(high|low|moderate)\b"
    df["Noise Level"] = df["Noise Level"].apply(
        lambda x: re.search(noise_pattern, x).group().capitalize() if re.search(noise_pattern, x) else ""
    )
    
    # Fill any remaining empty values with mode
    noise_mode = df["Noise Level"].mode()[0] if not df["Noise Level"].mode().empty else "Moderate"
    df["Noise Level"] = df["Noise Level"].replace("", noise_mode)

# ✅ Standardize the area column ✅
if "area" in df.columns:
    df["area"] = df["area"].astype(str).str.lower().str.strip()  # Normalize text

    # Extract numerical values from area
    df["area_numeric"] = df["area"].str.extract(r"(\d+\.?\d*)")[0]
    # Convert to numeric and handle any conversion errors
    df["area_numeric"] = pd.to_numeric(df["area_numeric"], errors="coerce")
    
    # Fill any missing values with the median area
    median_area = df["area_numeric"].median()
    df["area_numeric"] = df["area_numeric"].fillna(median_area)
    
    # Check for outliers and potentially erroneous entries in area
   
    df["area_zscore"] = np.abs((df["area_numeric"] - df["area_numeric"].mean()) / df["area_numeric"].std())
    
    # Mark potential outliers (z-score > 3) for investigation
    outliers = df[df["area_zscore"] > 3].copy()
    
    # For area-to-chairs ratio outliers, estimate corrected area
    df["chairs_area_ratio"] = df["n_chairs"] / df["area_numeric"]
    median_ratio = df["chairs_area_ratio"].median()
    
   
    small_area_many_chairs = df[(df["area_numeric"] < 10) & (df["n_chairs"] > 50)]
    for idx, row in small_area_many_chairs.iterrows():
        corrected_area = row["n_chairs"] / median_ratio
        df.at[idx, "area_numeric"] = corrected_area
    
    # Format area consistently with 2 decimal places and "sqm"
    df["area"] = df["area_numeric"].apply(lambda x: f"{x:.2f} sqm" if pd.notna(x) else "")
    
    # Drop temporary columns used for calculations
    df.drop(columns=["area_zscore", "chairs_area_ratio"], inplace=True)

# ✅ Standardize Wi-Fi Connection ✅
if "WiFi Connection" in df.columns:
    df["WiFi Connection"] = df["WiFi Connection"].astype(str).str.lower().str.strip()
    
    # Map similar values to standard categories
    wifi_mapping = {
        "good": "Good",
        "poor": "Poor",
        "low": "Poor",
        "non exising": "Poor",
        "non existing": "Poor"
    }
    
    for key, value in wifi_mapping.items():
        df["WiFi Connection"] = df["WiFi Connection"].replace(key, value)
    
    # Capitalize first letter for consistency
    df["WiFi Connection"] = df["WiFi Connection"].str.capitalize()

# ✅ Main Entrance Distance Standardization ✅
if "Main Entrance Distance" in df.columns:
    df["Main Entrance Distance"] = df["Main Entrance Distance"].astype(str).str.lower().str.strip()
    
    # Map to standardized categories
    distance_mapping = {
        "short": "Short",
        "medium": "Medium",
        "long": "Long",
        "very short": "Very Short"
    }
    
    for key, value in distance_mapping.items():
        df["Main Entrance Distance"] = df["Main Entrance Distance"].replace(key, value)
    
    # Capitalize for consistency
    df["Main Entrance Distance"] = df["Main Entrance Distance"].str.capitalize()

# ====================================
# Handling Duplicate Classrooms
# ====================================

print("\n✅ Starting Duplicate Classroom Handling...")

df_with_duplicates = df.copy()

# Check for duplicate classrooms
if "classroom" in df.columns:
    # Identify duplicate classrooms
    duplicate_classrooms = df["classroom"].value_counts()
    duplicate_classrooms = duplicate_classrooms[duplicate_classrooms > 1].index.tolist()
    
    print(f"Found {len(duplicate_classrooms)} classrooms with duplicate entries.")
    
    # Create a new DataFrame to store the consolidated rows
    consolidated_df = pd.DataFrame(columns=df.columns)
    
    # Define columns to exclude (personal identifiers) - only for consolidated records
    exclude_columns = ["name", "surname", "ID", "student_id", "person_id", "full_name"]
    
    # Process each duplicate classroom
    for classroom in duplicate_classrooms:
        # Get all rows for this classroom
        duplicate_rows = df[df["classroom"] == classroom]
        
        # Create a new consolidated row
        consolidated_row = {}
        
        # Process each column
        for column in df.columns:
            # Skip personal identifier columns ONLY for consolidated duplicate records
            if column.lower() in [col.lower() for col in exclude_columns]:
                consolidated_row[column] = None 
                continue
                
            if column == "classroom":
              
                consolidated_row[column] = classroom
            elif column in numerical_cols:
                # For numerical columns, take the average, rounded appropriately
                if column in numeric_int_cols:
                    # For count-based integers, take the ceiling of the average (round up)
                    consolidated_row[column] = int(np.ceil(duplicate_rows[column].mean()))
                else:
                    # For other numerical values, take the mean
                    consolidated_row[column] = round(duplicate_rows[column].mean(), 2)
            elif column == "area_numeric":
                # Handle area_numeric separately
                consolidated_row[column] = round(duplicate_rows[column].mean(), 2)
            elif column == "floor":
                # Take the most common floor
                consolidated_row[column] = duplicate_rows[column].mode()[0]
                # Also update floor_number if it exists
                if "floor_number" in df.columns:
                    consolidated_row["floor_number"] = duplicate_rows["floor_number"].mode()[0]
            elif column in boolean_cols:
                # For boolean columns, use True if any row has True
                consolidated_row[column] = duplicate_rows[column].any()
            elif column == "area":
                # Use the newly calculated area_numeric for consistency
                if "area_numeric" in consolidated_row:
                    area_value = consolidated_row["area_numeric"]
                else:
                    area_value = round(duplicate_rows["area_numeric"].mean(), 2)
                consolidated_row[column] = f"{area_value:.2f} sqm"
            else:
                # For other categorical columns, take the most frequent value
                non_null_values = duplicate_rows[column].dropna()
                if len(non_null_values) > 0:
                    consolidated_row[column] = non_null_values.mode()[0]
                else:
                    consolidated_row[column] = None
        
        
        consolidated_df = pd.concat([consolidated_df, pd.DataFrame([consolidated_row])], ignore_index=True)
        
    # Creating a clean version of the dataframe with duplicates removed and consolidation applied
    
    df_clean = df[~df["classroom"].isin(duplicate_classrooms)]
    
    # adding the consolidated rows
    df_clean = pd.concat([df_clean, consolidated_df], ignore_index=True)
    
    # Save a record of the original duplicate entries for reference
    duplicates_file_path = "duplicate_entries.xlsx"
    df_with_duplicates[df_with_duplicates["classroom"].isin(duplicate_classrooms)].to_excel(duplicates_file_path, index=False)
    print(f"Saved original duplicate entries to '{duplicates_file_path}' for reference")
    
    # Replace the main dataframe with the cleaned version
    df = df_clean.copy()
    
    # Sort by classroom for easier reference
    df = df.sort_values(by="classroom").reset_index(drop=True)
    
    # Save the consolidated dataset
    consolidated_file_path = "consolidated_cleaned_data.xlsx"
    df.to_excel(consolidated_file_path, index=False)
    print(f"✅ Duplicate handling complete! Consolidated file saved as '{consolidated_file_path}'")
    print(f"✅ Updated existing cleaned data files with consolidated version")
else:
    print("⚠️ 'classroom' column not found - skipping duplicate handling")

# Step 5: Save the cleaned dataset
cleaned_file_path = "cleaned_data.xlsx"
df.to_excel(cleaned_file_path, index=False)
df.to_csv("cleaned_data.csv", index=False)
print(f"✅ Data cleaning complete! Cleaned file saved as '{cleaned_file_path}'")

# ====================================
# 2.2 Statistical Analysis
# ====================================

print("\n✅ Starting Statistical Analysis...")


if "area_numeric" in df.columns and "area_numeric" not in numerical_cols:
    numerical_cols.append("area_numeric")

# Calculate central tendency measures for numerical columns
central_tendency = pd.DataFrame()

for col in numerical_cols:
    if col in df.columns:
        central_tendency.loc["Mean", col] = df[col].mean()
        central_tendency.loc["Median", col] = df[col].median()
        central_tendency.loc["Std Dev", col] = df[col].std()
        central_tendency.loc["Min", col] = df[col].min()
        central_tendency.loc["25%", col] = df[col].quantile(0.25)
        central_tendency.loc["75%", col] = df[col].quantile(0.75)
        central_tendency.loc["Max", col] = df[col].max()
        central_tendency.loc["Range", col] = df[col].max() - df[col].min()

# Saving central tendency measures
central_tendency.to_excel("numerical_statistics.xlsx")
print("✅ Central tendency calculations complete")

# Correlation analysis for numerical features
if len(numerical_cols) > 1:
    
    existing_num_cols = [col for col in numerical_cols if col in df.columns]
    correlation_matrix = df[existing_num_cols].corr()
    correlation_matrix.to_excel("correlation_matrix.xlsx")
    
    # Creating a heatmap for correlations
    plt.figure(figsize=(10, 8))
    sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', fmt=".2f")
    plt.title("Correlation Matrix of Numerical Features")
    plt.tight_layout()
    plt.savefig("correlation_heatmap.png")
    print("✅ Correlation analysis complete")

# Updating categorical columns list to include any boolean columns
categorical_analysis_cols = ["floor", "Noise Level", "WiFi Connection", "Main Entrance Distance"] + boolean_cols

# Creating value counts for each categorical column
categorical_stats = {}
for col in categorical_analysis_cols:
    if col in df.columns:
        value_counts = df[col].value_counts().reset_index()
        value_counts.columns = [col, 'Count']
        categorical_stats[col] = value_counts
        
        # Create bar charts for categorical variables
        plt.figure(figsize=(10, 6))
        sns.barplot(x=col, y='Count', data=value_counts)
        plt.title(f"Distribution of {col}")
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.savefig(f"{col}_distribution.png")

# Creating a comprehensive report of all analyses
with open("classroom_data_analysis_report.txt", "w") as f:
    f.write("CLASSROOM DATA ANALYSIS REPORT\n")
    f.write("============================\n\n")
    
    # Dataset overview
    f.write("1. Dataset Overview\n")
    f.write("-----------------\n")
    f.write(f"Number of classrooms: {len(df)}\n")
    f.write(f"Number of features: {len(df.columns)}\n\n")
    
    # Numerical statistics
    f.write("2. Statistical Analysis of Numerical Features\n")
    f.write("------------------------------------------\n")
    f.write(central_tendency.to_string())
    f.write("\n\n")
    
    # Categorical value counts
    f.write("3. Analysis of Categorical Features\n")
    f.write("--------------------------------\n")
    for col, counts in categorical_stats.items():
        f.write(f"\n{col} Distribution:\n")
        f.write(counts.to_string(index=False))
        f.write("\n")
    
    # Correlations of interest
    f.write("\n4. Notable Correlations\n")
    f.write("----------------------\n")
    # Highlight strong correlations (absolute value > 0.5)
    existing_num_cols = [col for col in numerical_cols if col in df.columns]
    correlation_matrix = df[existing_num_cols].corr()
    strong_correlations = correlation_matrix.unstack().sort_values(ascending=False)
    strong_correlations = strong_correlations[(strong_correlations < 1.0) & (abs(strong_correlations) > 0.5)]
    f.write(strong_correlations.to_string())
    
    # Floor-specific analysis
    f.write("\n\n5. Floor-specific Analysis\n")
    f.write("------------------------\n")
    floor_stats = df.groupby("floor")[existing_num_cols].mean()
    f.write("Average values by floor:\n")
    f.write(floor_stats.to_string())
    
    # Add duplicate analysis information
    if "classroom" in df.columns and len(duplicate_classrooms) > 0:
        f.write("\n\n6. Duplicate Classroom Analysis\n")
        f.write("-----------------------------\n")
        f.write(f"Number of classrooms with multiple entries: {len(duplicate_classrooms)}\n")
        f.write("Duplicate classrooms: " + ", ".join(duplicate_classrooms))

print("✅ Statistical analysis complete! All results saved to files.")