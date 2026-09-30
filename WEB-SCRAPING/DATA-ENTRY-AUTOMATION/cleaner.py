import pandas as pd
import openpyxl
from openpyxl.styles import PatternFill, Font, Alignment, Border, Side

# 1. LOAD RAW DATASET (250 MB)
print("1. Loading raw dataset...")
df = pd.read_csv('data/raw_data_business_licenses.csv', low_memory=False)

# 2. GENERATE SMALL RAW DATA SAMPLE (100 rows) FOR GITHUB
print("2. Generating raw data sample for repository...")
df.head(100).to_csv('data/raw_data_sample.csv', index=False)

# 3. DATA CLEANING PIPELINE
print("3. Executing data cleaning pipeline...")

# A. Drop columns with over 80% missing values
missing_percent = df.isnull().sum() / len(df)
df = df[missing_percent[missing_percent < 0.8].index]

# B. Drop unwanted GIS and coordinate metadata columns
unwanted_cols = ['the_geom', 'the_geom_webmercator', 'geocode_x', 'geocode_y', 'gdb_geomattr_data']
df = df.drop(columns=[col for col in unwanted_cols if col in df.columns], errors='ignore')

# C. Remove duplicate rows
df = df.drop_duplicates()

# D. Standardize date formats (YYYY-MM-DD)
date_cols = ['initialissuedate', 'mostrecentissuedate', 'expirationdate', 'inactivedate', 'effectivedate']
for col in date_cols:
    if col in df.columns:
        df[col] = pd.to_datetime(df[col], errors='coerce').dt.strftime('%Y-%m-%d')

# E. Fix numeric float IDs to clean integer values
int_cols = ['addressobjectid', 'numberofid', 'council_district']
for col in int_cols:
    if col in df.columns:
        df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0).astype('int64')

# F. Standardize text values to Title Case
text_cols = ['address', 'legalname', 'business_name', 'opa_owner']
for col in text_cols:
    if col in df.columns:
        df[col] = df[col].astype(str).str.strip().str.title()

# 4. EXPORT FORMATTED CLEAN SAMPLE TO EXCEL (First 1,000 rows for lightweight deliverable)
print("4. Applying Excel formatting and exporting sample deliverable...")
df_sample = df.head(1000)
output_file = 'data/cleaned_data_sample.xlsx'

with pd.ExcelWriter(output_file, engine='openpyxl') as writer:
    df_sample.to_excel(writer, index=False, sheet_name='Cleaned Data')
    worksheet = writer.sheets['Cleaned Data']
    
    # Styling definitions
    header_fill = PatternFill(start_color='1F4E78', end_color='1F4E78', fill_type='solid') # Dark Corporate Blue
    header_font = Font(name='Segoe UI', size=11, bold=True, color='FFFFFF') # Bold White Text
    data_font = Font(name='Segoe UI', size=10)
    thin_border = Border(
        left=Side(style='thin', color='D9D9D9'),
        right=Side(style='thin', color='D9D9D9'),
        top=Side(style='thin', color='D9D9D9'),
        bottom=Side(style='thin', color='D9D9D9')
    )
    
    # Format Header Row
    for cell in worksheet[1]:
        cell.fill = header_fill
        cell.font = header_font
        cell.alignment = Alignment(horizontal='center', vertical='center', wrap_text=True)
    
    # Format Data Cells & Dynamic Auto-Fit Column Widths
    for col in worksheet.columns:
        max_len = 0
        col_letter = col[0].column_letter
        for cell in col:
            cell.font = data_font
            cell.border = thin_border
            val_str = str(cell.value or '')
            if len(val_str) > max_len:
                max_len = len(val_str)
        worksheet.column_dimensions[col_letter].width = max(max_len + 4, 12)

print(f"[SUCCESS] Data cleaning completed! Cleaned sample saved to: {output_file}")