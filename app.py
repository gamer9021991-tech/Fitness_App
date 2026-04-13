import pandas as pd
import streamlit as st
import joblib

st.title("Personalized Fitness Recommendation App")
st.write("Enter user information to get a recommended workout type and estimated calories burned.")

# Load trained model
model = joblib.load("fitness_model.pkl")

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

# Sidebar inputs
st.sidebar.header("User Inputs")

age = st.sidebar.number_input("Age", min_value=10, max_value=100, value=30)
gender = st.sidebar.selectbox("Gender", ["Male", "Female"])
weight_lbs = st.sidebar.number_input("Weight (lbs)", min_value=66.0, max_value=650.0, value=180.0)
height_feet = st.sidebar.number_input("Height - Feet", min_value=2, max_value=8, value=5)
height_inches = st.sidebar.number_input("Height - Inches", min_value=0, max_value=11, value=9)
freq = st.sidebar.number_input("Workout Frequency (days/week)", min_value=1, max_value=7, value=3)
exp = st.sidebar.selectbox(
    "Experience Level",
    [1, 2, 3],
    format_func=lambda x: {1: "Beginner", 2: "Intermediate", 3: "Advanced"}[x]
)
duration = st.sidebar.number_input(
    "Session Duration (hours)",
    min_value=0.25,
    max_value=4.0,
    value=1.0,
    step=0.25
)

# Convert units
weight_kg = weight_lbs * 0.45359237
total_inches = (height_feet * 12) + height_inches
height_m = total_inches * 0.0254
bmi = weight_kg / (height_m ** 2)

# Build prediction input
user_df = pd.DataFrame([{
    "age": age,
    "gender": gender,
    "weight_kg": weight_kg,
    "height_m": height_m,
    "workout_frequency_days_week": freq,
    "experience_level": exp,
    "bmi": bmi,
    "session_duration_hours": duration,
}])

user_df["recommended_workout"] = user_df.apply(recommend_workout, axis=1)

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

user_df = user_df[feature_order]

predicted_calories = int(round(model.predict(user_df)[0], 0))

recommended_workout = user_df["recommended_workout"].iloc[0]

# Output
st.subheader("Recommendation Results")
st.write(f"**Entered Weight:** {weight_lbs:.1f} lbs")
st.write(f"**Entered Height:** {height_feet} ft {height_inches} in")
st.write(f"**Calculated BMI:** {bmi:.2f}")
st.write(f"**Recommended Workout Type:** {recommended_workout}")
st.write(f"**Estimated Calories Burned:** {predicted_calories}")