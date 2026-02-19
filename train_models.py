"""
Machine Learning Model Training - Carbon Emission Dataset
"""

import pandas as pd
import numpy as np
import joblib
import os
import time
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LinearRegression
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor
from sklearn.cluster import KMeans
from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error
import xgboost as xgb
import warnings
warnings.filterwarnings('ignore')

os.makedirs('models', exist_ok=True)

# ─── LOAD CLEANED DATA ────────────────────────────────────────────────────────

print("=" * 55)
print("  CARBON FOOTPRINT ML TRAINING PIPELINE")
print("=" * 55)

df = pd.read_csv('data/carbon_data_cleaned.csv')

# All columns except the target
FEATURES = [col for col in df.columns if col != 'carbonemission']
TARGET = 'carbonemission'

X = df[FEATURES]
y = df[TARGET]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

print(f"\n📊 Dataset    : {len(df)} samples")
print(f"   Training   : {len(X_train)} samples")
print(f"   Testing    : {len(X_test)} samples")
print(f"   Features   : {len(FEATURES)}")

# ─── HELPER: EVALUATE MODEL ───────────────────────────────────────────────────

def evaluate(name, model, X_tr, X_te, y_tr, y_te):
    t0 = time.time()
    model.fit(X_tr, y_tr)
    train_time = time.time() - t0

    y_pred = model.predict(X_te)
    r2   = r2_score(y_te, y_pred)
    mse  = mean_squared_error(y_te, y_pred)
    rmse = np.sqrt(mse)  # Calculate RMSE manually
    mae  = mean_absolute_error(y_te, y_pred)

    cv_scores = cross_val_score(model, X_tr, y_tr, cv=5, scoring='r2', n_jobs=-1)

    print(f"\n{'─'*50}")
    print(f"  {name}")
    print(f"{'─'*50}")
    print(f"  R² Score        : {r2:.4f}   ({r2*100:.1f}% variance explained)")
    print(f"  RMSE            : {rmse:.1f} kg CO₂")
    print(f"  MAE             : {mae:.1f} kg CO₂")
    print(f"  CV R² (5-fold)  : {cv_scores.mean():.4f} ± {cv_scores.std():.4f}")
    print(f"  Training time   : {train_time:.3f}s")

    return {
        'model': model, 'name': name,
        'r2': r2, 'rmse': rmse, 'mae': mae,
        'cv_r2': cv_scores.mean(), 'cv_std': cv_scores.std(),
        'train_time': train_time, 'y_pred': y_pred
    }

# ─── TRAIN ALL 4 MODELS ───────────────────────────────────────────────────────

print("\n🤖 Training models...\n")

results = []

results.append(evaluate(
    "1. Linear Regression (Baseline)",
    LinearRegression(),
    X_train, X_test, y_train, y_test
))

results.append(evaluate(
    "2. Decision Tree Regressor",
    DecisionTreeRegressor(max_depth=10, min_samples_split=20, random_state=42),
    X_train, X_test, y_train, y_test
))

results.append(evaluate(
    "3. Random Forest Regressor  ⭐ (Best Expected)",
    RandomForestRegressor(n_estimators=200, max_depth=15,
                          min_samples_split=10, n_jobs=-1, random_state=42),
    X_train, X_test, y_train, y_test
))

results.append(evaluate(
    "4. XGBoost Regressor  🚀 (Challenger)",
    xgb.XGBRegressor(n_estimators=300, learning_rate=0.05, max_depth=7,
                     subsample=0.8, colsample_bytree=0.8,
                     random_state=42, verbosity=0),
    X_train, X_test, y_train, y_test
))

# ─── COMPARISON TABLE ─────────────────────────────────────────────────────────

print(f"\n\n{'='*55}")
print("  MODEL COMPARISON TABLE")
print(f"{'='*55}")
print(f"  {'Model':<35} {'R²':>6}  {'RMSE':>8}  {'CV R²':>8}")
print(f"  {'-'*35} {'──────':>6}  {'──────':>8}  {'──────':>8}")
for r in results:
    star = " ✅" if r['r2'] == max(x['r2'] for x in results) else ""
    print(f"  {r['name'][:35]:<35} {r['r2']:>6.4f}  {r['rmse']:>8.1f}  {r['cv_r2']:>8.4f}{star}")

# ─── BEST MODEL ───────────────────────────────────────────────────────────────

best = max(results, key=lambda x: x['r2'])
print(f"\n🏆 Best Model: {best['name']}")
print(f"   R² = {best['r2']:.4f} | RMSE = {best['rmse']:.1f} kg | CV R² = {best['cv_r2']:.4f}")

# Re-train best on full data for max accuracy
rf_final = RandomForestRegressor(n_estimators=200, max_depth=15,
                                  min_samples_split=10, n_jobs=-1, random_state=42)
rf_final.fit(X, y)

# ─── FEATURE IMPORTANCE ───────────────────────────────────────────────────────

feat_importance = pd.DataFrame({
    'feature': FEATURES,
    'importance': rf_final.feature_importances_
}).sort_values('importance', ascending=False)

print(f"\n\n{'='*55}")
print("  FEATURE IMPORTANCE (Random Forest)")
print(f"{'='*55}")
for _, row in feat_importance.head(15).iterrows():
    bar = '█' * int(row['importance'] * 50)
    print(f"  {row['feature']:<35} {row['importance']*100:>5.1f}%  {bar}")

# ─── K-MEANS CLUSTERING ───────────────────────────────────────────────────────

print(f"\n\n{'='*55}")
print("  K-MEANS USER SEGMENTATION (k=3)")
print(f"{'='*55}")

# Scale features for KMeans
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

kmeans = KMeans(n_clusters=3, random_state=42, n_init=10)
clusters = kmeans.fit_predict(X_scaled)

# Label clusters by mean CO₂
cluster_means = pd.Series(y).groupby(clusters).mean().sort_values()
cluster_label_map = {
    cluster_means.index[0]: 'Low Emitter',
    cluster_means.index[1]: 'Medium Emitter',
    cluster_means.index[2]: 'High Emitter'
}

print(f"\n  Cluster segments:")
for c, label in cluster_label_map.items():
    mask = clusters == c
    co2_vals = y[mask]
    icon = '🟢' if 'Low' in label else ('🟡' if 'Medium' in label else '🔴')
    print(f"  {icon} {label:<18} | n={mask.sum():>4} | "
          f"Avg CO₂: {co2_vals.mean():>7,.0f} kg | "
          f"Range: {co2_vals.min():.0f}–{co2_vals.max():.0f} kg")

# ─── SAVE ALL MODELS ──────────────────────────────────────────────────────────

print(f"\n\n{'='*55}")
print("  SAVING MODELS")
print(f"{'='*55}")

joblib.dump(rf_final, 'models/random_forest.pkl')
joblib.dump(best['model'] if best['name'] != results[2]['name'] else rf_final,
            'models/best_model.pkl')
joblib.dump(kmeans, 'models/kmeans.pkl')
joblib.dump(scaler, 'models/scaler.pkl')
joblib.dump(results[3]['model'], 'models/xgboost.pkl')

# Save feature names and label map
import json
with open('models/feature_names.json', 'w') as f:
    json.dump(FEATURES, f)
with open('models/cluster_label_map.json', 'w') as f:
    json.dump({str(k): v for k, v in cluster_label_map.items()}, f)
feat_importance.to_csv('models/feature_importance.csv', index=False)

print(f"  ✅ models/random_forest.pkl")
print(f"  ✅ models/best_model.pkl")
print(f"  ✅ models/kmeans.pkl")
print(f"  ✅ models/scaler.pkl")
print(f"  ✅ models/xgboost.pkl")
print(f"  ✅ models/feature_importance.csv")
print(f"  ✅ models/cluster_label_map.json")

print(f"\n{'='*55}")
print("  TRAINING COMPLETE! ✅")
print(f"{'='*55}")
print("\nNext step → Run:  streamlit run app.py")