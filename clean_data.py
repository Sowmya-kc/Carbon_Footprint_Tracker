#Data Cleaning & Preprocessing


import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder
import warnings
warnings.filterwarnings('ignore')

print("="*60)
print("  CARBON EMISSION DATA CLEANING")
print("="*60)

# ─── LOAD RAW DATA ────────────────────────────────────────────────────────────

df = pd.read_csv('data/Carbon Emission.csv')
print(f"\n📥 Loaded dataset: {df.shape[0]} rows × {df.shape[1]} columns")

# ─── STEP 1: Handle Missing Values ────────────────────────────────────────────

print("\n🔍 Step 1: Handling Missing Values")
print(f"   'Vehicle Type' has {df['Vehicle Type'].isnull().sum()} missing values")

# People with walk/bicycle or public transport don't have a vehicle type
df['Vehicle Type'] = df['Vehicle Type'].fillna('none')
print(f"   ✅ Filled missing 'Vehicle Type' with 'none'")

# Verify no missing values remain
assert df.isnull().sum().sum() == 0, "Still have missing values!"
print(f"   ✅ Total missing values: {df.isnull().sum().sum()}")

# ─── STEP 2: Drop Complex Columns ─────────────────────────────────────────────

print("\n🗑️  Step 2: Dropping Complex Columns")
# These columns are lists stored as strings - too complex for simple ML
# They also don't add much predictive power
drop_cols = ['Recycling', 'Cooking_With']
df = df.drop(columns=drop_cols)
print(f"   ✅ Dropped: {drop_cols}")
print(f"   Remaining columns: {df.shape[1]}")

# ─── STEP 3: Encode Categorical Variables ─────────────────────────────────────

print("\n🔤 Step 3: Encoding Categorical Variables")

# Identify categorical columns
categorical_cols = df.select_dtypes(include='object').columns.tolist()
print(f"   Found {len(categorical_cols)} categorical columns:")
for col in categorical_cols:
    print(f"      • {col:<30} ({df[col].nunique()} unique values)")

# Label encode each categorical column
label_encoders = {}
for col in categorical_cols:
    le = LabelEncoder()
    df[col] = le.fit_transform(df[col].astype(str))
    label_encoders[col] = le
    print(f"   ✅ Encoded '{col}': {list(le.classes_)[:5]}...")

# ─── STEP 4: Feature Engineering ──────────────────────────────────────────────

print("\n⚙️  Step 4: Feature Engineering")

# Create interaction features (these often improve ML performance)
df['transport_distance_interaction'] = df['Transport'] * df['Vehicle Monthly Distance Km']
df['energy_efficiency_heating'] = df['Energy efficiency'] * df['Heating Energy Source']
print(f"   ✅ Created 2 interaction features")

# ─── STEP 5: Remove Outliers (Optional but recommended) ──────────────────────

print("\n📉 Step 5: Handling Outliers")
Q1 = df['CarbonEmission'].quantile(0.25)
Q3 = df['CarbonEmission'].quantile(0.75)
IQR = Q3 - Q1
lower_bound = Q1 - 3 * IQR  # Using 3*IQR instead of 1.5 to be less aggressive
upper_bound = Q3 + 3 * IQR

outliers_before = df.shape[0]
df = df[(df['CarbonEmission'] >= lower_bound) & (df['CarbonEmission'] <= upper_bound)]
outliers_removed = outliers_before - df.shape[0]
print(f"   Outliers removed: {outliers_removed} ({outliers_removed/outliers_before*100:.1f}%)")
print(f"   Remaining rows: {df.shape[0]}")

# ─── STEP 6: Normalize Column Names ───────────────────────────────────────────

print("\n✏️  Step 6: Standardizing Column Names")
# Make column names Python-friendly (no spaces, lowercase)
df.columns = df.columns.str.lower().str.replace(' ', '_').str.replace('/', '_')
print(f"   ✅ Column names standardized")

# ─── STEP 7: Reorder Columns (target last) ───────────────────────────────────

print("\n📋 Step 7: Organizing Columns")
target_col = 'carbonemission'
feature_cols = [col for col in df.columns if col != target_col]
df = df[feature_cols + [target_col]]
print(f"   ✅ Target column '{target_col}' moved to end")

# ─── SAVE CLEANED DATA ────────────────────────────────────────────────────────

output_path = 'data/carbon_data_cleaned.csv'
df.to_csv(output_path, index=False)

print(f"\n{'='*60}")
print("  CLEANING COMPLETE! ✅")
print(f"{'='*60}")
print(f"\n📊 Final Dataset:")
print(f"   Rows:     {df.shape[0]:,}")
print(f"   Columns:  {df.shape[1]}")
print(f"   Features: {len(feature_cols)}")
print(f"   Target:   {target_col}")
print(f"\n💾 Saved to: {output_path}")

print(f"\n📈 Target Variable Stats (CarbonEmission):")
print(f"   Min:    {df[target_col].min():.0f} kg CO₂")
print(f"   Max:    {df[target_col].max():.0f} kg CO₂")
print(f"   Mean:   {df[target_col].mean():.0f} kg CO₂")
print(f"   Median: {df[target_col].median():.0f} kg CO₂")
print(f"   Std:    {df[target_col].std():.0f} kg CO₂")

print(f"\n🔍 Sample of cleaned data:")
print(df.head(3).to_string())

print(f"\n{'='*60}")
print("  Next Step → Run: python train_models.py")
print(f"{'='*60}")

# Save encoder mappings for reference
import json
encoder_map = {}
for col, le in label_encoders.items():
    encoder_map[col] = {str(i): label for i, label in enumerate(le.classes_)}

with open('data/label_encoders.json', 'w') as f:
    json.dump(encoder_map, f, indent=2)
print(f"\n📝 Label encoder mappings saved to: data/label_encoders.json")