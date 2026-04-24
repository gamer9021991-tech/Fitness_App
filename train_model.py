import os
import pandas as pd
import joblib
from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, r2_score


# File paths

script_dir = os.path.dirname(os.path.abspath(__file__))

data1_path = os.path.join(script_dir, "cleaned_gym_data_1.xlsx")
data2_path = os.path.join(script_dir, "cleaned_gym_data_2.xlsx")
data3_path = os.path.join(script_dir, "cleaned_gym_data_3.xlsx")

model_path = os.path.join(script_dir, "fitness_model.pkl")

# Recommendation logic

def recommend_workout(row):
    if row["bmi"] >= 30:
        return "Cardio"
    elif row["experience_level"] == 1:
        return "Strength"
    elif row["experience_level"] >= 3:
        return "HIIT"
    else:
        return "Yoga"

# Required model columns

model_columns = [
    "age",
    "gender",
    "weight_kg",
    "height_m",
    "workout_frequency_days_week",
    "experience_level",
    "bmi",
    "session_duration_hours",
    "calories_burned",
]

feature_order = [
    "age",
    "gender",
    "weight_kg",
    "height_m",
    "workout_frequency_days_week",
    "experience_level",
    "bmi",
    "session_duration_hours",
    "recommended_workout",
]

# Load Dataset 1

df1 = pd.read_excel(data1_path)

df1 = df1.drop(columns=["bmi_calc"], errors="ignore")

df1 = df1[
    [
        "age",
        "gender",
        "weight_kg",
        "height_m",
        "workout_frequency_days_week",
        "experience_level",
        "bmi",
        "session_duration_hours",
        "calories_burned",
    ]
].copy()

# Load Dataset 2

df2 = pd.read_excel(data2_path)

df2 = df2.rename(columns={
    "Age": "age",
    "Gender": "gender",
    "Actual Weight": "weight_kg",
    "Duration": "duration_minutes",
    "Heart Rate": "heart_rate",
    "BMI": "bmi",
    "Calories Burn": "calories_burned",
    "height_in": "height_in",
    "Exercise Intensity": "exercise_intensity",
})

df2["height_m"] = df2["height_in"] * 0.0254
df2["session_duration_hours"] = df2["duration_minutes"] / 60.0

df2["workout_frequency_days_week"] = 3

df2["experience_level"] = df2["exercise_intensity"].apply(
    lambda x: 1 if x <= 2 else 2 if x <= 4 else 3
)

df2 = df2[
    [
        "age",
        "gender",
        "weight_kg",
        "height_m",
        "workout_frequency_days_week",
        "experience_level",
        "bmi",
        "session_duration_hours",
        "calories_burned",
    ]
].copy()

# Load Dataset 3

df3 = pd.read_excel(data3_path)

df3 = df3.rename(columns={
    "BMI": "bmi",
    "heart rate (BPM)": "heart_rate",
    "intensity_level": "intensity_level",
})

# Use height_m if available, otherwise calculate from height_cm
if "height_m" not in df3.columns:
    df3["height_m"] = df3["height_cm"] / 100

# Dataset 3 does not have session duration, so use a reasonable default
df3["session_duration_hours"] = 1.0

# Convert intensity level into experience level
df3["experience_level"] = df3["intensity_level"].astype(str).str.upper().map({
    "LOW": 1,
    "MODERATE": 2,
    "MEDIUM": 2,
    "HIGH": 3,
})

# If any intensity values do not map, assume intermediate
df3["experience_level"] = df3["experience_level"].fillna(2)

df3 = df3[
    [
        "age",
        "gender",
        "weight_kg",
        "height_m",
        "workout_frequency_days_week",
        "experience_level",
        "bmi",
        "session_duration_hours",
        "calories_burned",
    ]
].copy()

# Combine datasets

df = pd.concat([df1, df2, df3], ignore_index=True)

# Standardize gender text
df["gender"] = df["gender"].astype(str).str.strip().str.title()

# Convert numeric columns
numeric_columns = [
    "age",
    "weight_kg",
    "height_m",
    "workout_frequency_days_week",
    "experience_level",
    "bmi",
    "session_duration_hours",
    "calories_burned",
]

for col in numeric_columns:
    df[col] = pd.to_numeric(df[col], errors="coerce")

# Drop missing rows
df = df.dropna(subset=model_columns)

# Add recommended workout
df["recommended_workout"] = df.apply(recommend_workout, axis=1)

# Features and target

X = df[feature_order]
y = df["calories_burned"]

categorical_features = ["gender", "recommended_workout"]
numeric_features = [col for col in X.columns if col not in categorical_features]

# Preprocessing and model

preprocessor = ColumnTransformer(
    transformers=[
        ("cat", OneHotEncoder(handle_unknown="ignore"), categorical_features),
        ("num", "passthrough", numeric_features),
    ]
)

model = Pipeline([
    ("preprocessor", preprocessor),
    ("regressor", RandomForestRegressor(n_estimators=100, random_state=42)),
])

# Train/test split

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)

# Train model

model.fit(X_train, y_train)

# Evaluate

y_pred = model.predict(X_test)

mae = mean_absolute_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

print("Model evaluation on combined datasets")
print(f"Dataset 1 rows used: {len(df1)}")
print(f"Dataset 2 rows used: {len(df2)}")
print(f"Dataset 3 rows used: {len(df3)}")
print(f"Combined rows used after cleanup: {len(df)}")
print(f"MAE: {mae:.2f}")
print(f"R2: {r2:.3f}")

print("\nFeature columns used:")
print(X.columns.tolist())

# Save model

joblib.dump(model, model_path)

print(f"\nModel saved as: {model_path}")