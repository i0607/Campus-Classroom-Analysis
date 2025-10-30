# Classroom Data Analysis Project

A comprehensive Python-based data analysis pipeline for cleaning, processing, and visualizing classroom facility data. This project provides automated tools for handling messy educational facility data and generating actionable insights.


**Overview**

This project analyzes classroom data to provide insights into facility characteristics, resource distribution, and infrastructure quality. It handles common data quality issues such as:
- Inconsistent formatting
- Missing values
- Duplicate entries
- Outlier detection
- Mixed data types

 **Features**

### Data Processing (`data_processing.py`)
-Intelligent Data Cleaning**: Automatically fixes typos, standardizes formats, and handles inconsistent entries
-Duplicate Management**: Detects and consolidates duplicate classroom entries
-Outlier Detection**: Identifies and corrects anomalous area measurements using statistical methods
-Missing Value Imputation**: Uses median/mean for numeric data and mode for categorical data
-Statistical Analysis**: Generates comprehensive descriptive statistics and correlation matrices
-Automated Reporting**: Creates detailed analysis reports with key insights

### Visualization Tools
- **Numeric Analysis (`vis2.py`)**: Correlation heatmaps, distribution plots, and floor-based analysis
- **Categorical Analysis (`vis3.py`)**: Distribution plots for all categorical features

##Prerequisites

- Python 3.7+
- Required packages:

  *pandas
  *numpy
  *matplotlib
  *seaborn
  *openpyxl


**Installation
**
1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/classroom-data-analysis.git
   cd classroom-data-analysis
   ```

2. Install required packages:
   ```bash
   pip install pandas numpy matplotlib seaborn openpyxl
   ```

3. Place your data file in the project directory:
   - File should be named: `Data Science Classroom Data.xlsx`
   - Sheet name should be: `Classroom Data`

 **Usage**

### Step 1: Run Data Processing Pipeline

```bash
python data_processing.py
```

This script will:
1. Load and clean the raw data
2. Handle duplicates and outliers
3. Perform statistical analysis
4. Generate multiple output files

### Step 2: Generate Visualizations

For numeric feature visualizations:
```bash
python vis2.py
```

For categorical feature visualizations:
```bash
python vis3.py
```

** Project Structure
**
```
classroom-data-analysis/
│
├── data_processing.py          # Main data processing pipeline
├── vis2.py                      # Numeric data visualizations
├── vis3.py                      # Categorical data visualizations
│
├── Data Science Classroom Data.xlsx  # Input data (not included)
│
└── outputs/                     # Generated files
    ├── cleaned_data.xlsx
    ├── cleaned_data.csv
    ├── consolidated_cleaned_data.xlsx
    ├── duplicate_entries.xlsx
    ├── numerical_statistics.xlsx
    ├── correlation_matrix.xlsx
    ├── correlation_heatmap.png
    ├── classroom_data_analysis_report.txt
    └── [various distribution plots]
```

**Data Pipeline
**
### 1. Data Loading
- Reads Excel file with classroom data
- Loads from specified sheet

### 2. Column Standardization
Fixes common typos and inconsistencies:
- `Ligting` → `Lighting`
- `Interior Deign` → `Interior Design`
- `Uage Timing` → `Usage Timing`
- `wifi_connec` → `WiFi Connection`
**Data Type Conversion
**
- **Numeric columns**: Extracts numbers from text (e.g., "2 units" → 2)
- **Boolean columns**: Standardizes yes/no/TRUE/FALSE to boolean
- **Categorical columns**: Normalizes text formatting

### 4. Missing Value Handling
- **Numeric**: Fills with median
- **Categorical**: Fills with mode
- **Boolean**: Fills with most common value

### 5. Standardization
Applies consistent formatting to:
- **Floor numbers**: "1st" → "1 floor"
- **Classroom codes**: Removes special characters, converts to uppercase
- **Area measurements**: Standardizes to "XX.XX sqm" format
- **Noise levels**: Extracts "High", "Low", or "Moderate"

### 6. Outlier Detection & Correction
- Calculates z-scores for area measurements
- Identifies impossible area-to-chairs ratios
- Corrects using statistical methods

### 7. Duplicate Consolidation
- Identifies classrooms with multiple entries
- Consolidates using intelligent rules:
  - **Numeric**: Averages values
  - **Categorical**: Takes most frequent value
  - **Boolean**: Uses OR logic (True if any entry is True)

### 8. Statistical Analysis
- Descriptive statistics (mean, median, std dev, quartiles)
- Correlation analysis
- Floor-specific analysis
- Distribution analysis for categorical features

## Output Files

| File | Description |
|------|-------------|
| `cleaned_data.xlsx` | Main cleaned dataset |
| `cleaned_data.csv` | CSV version of cleaned data |
| `consolidated_cleaned_data.xlsx` | Data with duplicates consolidated |
| `duplicate_entries.xlsx` | Original duplicate entries for reference |
| `numerical_statistics.xlsx` | Descriptive statistics for all numeric features |
| `correlation_matrix.xlsx` | Correlation coefficients between numeric features |
| `correlation_heatmap.png` | Visual representation of correlations |
| `classroom_data_analysis_report.txt` | Comprehensive text report with insights |
| `[feature]_distribution.png` | Distribution plots for categorical features |

**Visualizations
**
### Numeric Visualizations (vis2.py)
1. **Classroom Size Distribution**: Histogram showing frequency of different classroom capacities
2. **Classrooms per Floor**: Countplot showing distribution across building floors
3. **Correlation Heatmap**: Color-coded matrix showing relationships between numeric features

### Categorical Visualizations (vis3.py)
- Individual countplots for each categorical feature
- Automatically generated for all object-type columns
- Sorted by frequency for easy interpretation

**Key Features Analyzed
**
### Numeric Features
- Number of chairs
- Number of windows
- Number of air conditioners
- Number of sockets
- Number of cameras
- Number of doors
- Lighting units
- Area (square meters)
- Floor number

### Categorical Features
- Floor location
- WiFi connection quality
- Noise level
- Main entrance distance
- Cleaning service frequency
- Interior design
- Maintenance status
- Seats disposition

### Boolean Features
- Has blinds
- Has smartboard
- Has computer
- Exit banner present



**Notes
**
- Ensure your input Excel file matches the expected format
- The script assumes the sheet name is "Classroom Data"
- All visualizations are saved as PNG files for easy sharing
- The duplicate consolidation process preserves the original entries in a separate file

**Troubleshooting
**

**Issue**: `FileNotFoundError: Data Science Classroom Data.xlsx`
- **Solution**: Ensure the Excel file is in the same directory as the scripts

**Issue**: Missing visualizations
- **Solution**: Run `data_processing.py` before running visualization scripts

**Issue**: Import errors
- **Solution**: Install all required packages using pip
