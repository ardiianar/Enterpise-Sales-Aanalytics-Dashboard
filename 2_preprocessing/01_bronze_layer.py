# ==============================================================================
# MODULE 2: PREPROCESSING - BRONZE LAYER
# Purpose: Clean column names and prepare raw data for storage
# ==============================================================================

import re

def clean_column_name(col_name):
    """
    Clean column names by:
    - Stripping whitespace
    - Converting to lowercase
    - Replacing special characters with underscores
    
    Args:
        col_name (str): Original column name
    
    Returns:
        str: Cleaned column name
    """
    col_name = col_name.strip()  # Remove leading/trailing spaces
    col_name = col_name.lower()  # Convert to lowercase
    col_name = re.sub(r'[ ,;{}()\n\t=]+', '_', col_name)  # Replace special chars
    return col_name

# Load raw data from previous step
df_raw = spark.table("bronze_temp")  # Assumes data loaded in previous notebook

# Clean all column names
df_cleaned = df_raw.toDF(*[clean_column_name(c) for c in df_raw.columns])

print("=" * 70)
print("COLUMN NAMES CLEANED")
print("=" * 70)
print("New column names:")
for col in df_cleaned.columns:
    print(f"  - {col}")

# Save to Bronze Layer (raw cleaned data)
df_cleaned.write.format("delta") \
    .mode("overwrite") \
    .saveAsTable("workspace.default.bronze_ecommerce")

print(f"\n✓ Bronze layer saved: {df_cleaned.count()} records")
