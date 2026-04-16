import os
import pandas as pd
import streamlit as st
import joblib

st.title("Personalized Workout Type Recommendation App")
st.write("Enter user information to get a recommended workout type, an estimated calorie burn, and a suggested workout plan.")


# Load trained model

model_path = os.path.join(os.path.dirname(__file__), "fitness_model.pkl")
model = joblib.load(model_path)


# Recommendation logic

def recommend_workout(row):
    weight_gap_kg = row["weight_kg"] - row["goal_weight_kg"]

    # If user wants to lose a noticeable amount of weight
    if weight_gap_kg >= 4.5:  # about 10 lbs
        if row["experience_level"] >= 3:
            return "HIIT"
        return "Cardio"

    # If user wants to gain noticeable weight / muscle
    elif weight_gap_kg <= -2.3:  # about 5 lbs
        return "Strength"

    # If close to goal weight, use BMI and experience
    else:
        if row["bmi"] >= 30:
            return "Cardio"
        elif row["experience_level"] == 1:
            return "Strength"
        elif row["experience_level"] >= 3:
            return "HIIT"
        else:
            return "Yoga"


# Workout plan logic

def get_workout_plan(workout_type, experience_level, duration_hours):
    duration_minutes = int(duration_hours * 60)

    if workout_type == "Cardio":
        if duration_minutes <= 20:
            plan = [
                "5 minutes warm-up walk",
                "10 minutes brisk walking",
                "5 minutes cool-down walk"
            ]
            return plan, 20

        elif duration_minutes <= 40:
            plan = [
                "5 minutes warm-up walk",
                "20 minutes brisk walking or light cycling",
                "10 minutes incline walk or steady cycling",
                "5 minutes cool-down"
            ]
            return plan, 40

        elif duration_minutes <= 60:
            plan = [
                "5 minutes warm-up walk",
                "20 minutes brisk walking",
                "20 minutes cycling or elliptical",
                "10 minutes incline walk",
                "5 minutes cool-down"
            ]
            return plan, 60

        elif duration_minutes <= 90:
            plan = [
                "5 minutes warm-up walk",
                "25 minutes brisk walking",
                "25 minutes cycling or elliptical",
                "20 minutes incline walk",
                "10 minutes rowing or stair climber",
                "5 minutes cool-down"
            ]
            return plan, 90

        else:
            plan = [
                "5 minutes warm-up walk",
                "30 minutes brisk walking",
                "30 minutes cycling or elliptical",
                "20 minutes incline walk",
                "20 minutes rowing or stair climber",
                "10 minutes moderate steady-state cardio of choice",
                "5 minutes cool-down"
            ]
            return plan, 120

    elif workout_type == "Strength":
        if duration_minutes <= 30:
            if experience_level == 1:
                plan = [
                    "3 x 10 bodyweight squats",
                    "3 x 8 push-ups or incline push-ups",
                    "3 x 10 dumbbell rows",
                    "3 x 20-second plank"
                ]
            else:
                plan = [
                    "3 x 10 goblet squats",
                    "3 x 10 dumbbell bench press",
                    "3 x 10 dumbbell rows",
                    "3 x 30-second plank"
                ]
            return plan, 30

        elif duration_minutes <= 60:
            plan = [
                "4 x 8 squats",
                "4 x 8 dumbbell or barbell bench press",
                "4 x 10 rows",
                "3 x 10 shoulder press",
                "3 x 45-second plank",
                "5-10 minutes cool-down stretching"
            ]
            return plan, 60

        elif duration_minutes <= 90:
            plan = [
                "4 x 8 squats",
                "4 x 8 bench press",
                "4 x 10 rows",
                "3 x 10 shoulder press",
                "3 x 10 Romanian deadlifts",
                "3 x 12 lunges",
                "3 x 45-second plank",
                "10 minutes cool-down stretching"
            ]
            return plan, 90

        else:
            plan = [
                "5 minutes dynamic warm-up",
                "4 x 8 squats",
                "4 x 8 bench press",
                "4 x 10 rows",
                "4 x 10 shoulder press",
                "3 x 10 Romanian deadlifts",
                "3 x 12 lunges",
                "3 x 12 bicep curls",
                "3 x 12 tricep extensions",
                "3 x 60-second plank",
                "10-15 minutes cool-down stretching"
            ]
            return plan, 120

    elif workout_type == "HIIT":
        if duration_minutes <= 20:
            plan = [
                "20 seconds jumping jacks / 40 seconds rest x 6 rounds",
                "20 seconds bodyweight squats / 40 seconds rest x 6 rounds",
                "5 minutes cool-down"
            ]
            return plan, 20

        elif duration_minutes <= 30:
            plan = [
                "30 seconds burpees / 30 seconds rest x 8 rounds",
                "30 seconds mountain climbers / 30 seconds rest x 8 rounds",
                "5 minutes cool-down"
            ]
            return plan, 30

        elif duration_minutes <= 45:
            plan = [
                "30 seconds burpees / 30 seconds rest x 10 rounds",
                "30 seconds jump squats / 30 seconds rest x 10 rounds",
                "30 seconds mountain climbers / 30 seconds rest x 10 rounds",
                "5 minutes cool-down"
            ]
            return plan, 45

        elif duration_minutes <= 60:
            plan = [
                "40 seconds burpees / 20 seconds rest x 10 rounds",
                "40 seconds jump squats / 20 seconds rest x 10 rounds",
                "40 seconds mountain climbers / 20 seconds rest x 10 rounds",
                "30 seconds plank jacks / 30 seconds rest x 8 rounds",
                "5-10 minutes cool-down"
            ]
            return plan, 60

        else:
            plan = [
                "40 seconds burpees / 20 seconds rest x 12 rounds",
                "40 seconds jump squats / 20 seconds rest x 12 rounds",
                "40 seconds mountain climbers / 20 seconds rest x 12 rounds",
                "40 seconds high knees / 20 seconds rest x 12 rounds",
                "30 seconds plank jacks / 30 seconds rest x 10 rounds",
                "10 minutes cool-down"
            ]
            return plan, 75

    elif workout_type == "Yoga":
        if duration_minutes <= 20:
            plan = [
                "5 minutes breathing and mobility warm-up",
                "10 minutes beginner yoga flow",
                "5 minutes stretching"
            ]
            return plan, 20

        elif duration_minutes <= 40:
            plan = [
                "5 minutes breathing and mobility warm-up",
                "15 minutes sun salutation flow",
                "10 minutes balance and flexibility poses",
                "5 minutes cool-down stretching"
            ]
            return plan, 40

        elif duration_minutes <= 60:
            plan = [
                "10 minutes breathing and mobility warm-up",
                "20 minutes full-body yoga flow",
                "15 minutes flexibility and balance work",
                "10 minutes cool-down stretching"
            ]
            return plan, 60

        elif duration_minutes <= 90:
            plan = [
                "10 minutes breathing and mobility warm-up",
                "25 minutes full-body yoga flow",
                "20 minutes flexibility work",
                "20 minutes balance and stability poses",
                "10 minutes cool-down stretching"
            ]
            return plan, 90

        else:
            plan = [
                "10 minutes breathing and mobility warm-up",
                "30 minutes full-body yoga flow",
                "25 minutes flexibility work",
                "25 minutes balance and stability poses",
                "20 minutes deep stretching and recovery",
                "10 minutes cool-down breathing"
            ]
            return plan, 120

    return ["No workout plan available."], 0


# Goal interpretation logic

def get_goal_direction(current_weight_lbs, goal_weight_lbs):
    weight_diff = current_weight_lbs - goal_weight_lbs

    if weight_diff > 5:
        return f"Lose approximately {abs(weight_diff):.1f} lbs"
    elif weight_diff < -5:
        return f"Gain approximately {abs(weight_diff):.1f} lbs"
    else:
        return "Maintain current weight"


# Sidebar inputs

unit_system = st.sidebar.radio(
    "Unit System",
    ["Standard", "Metric"],
    index=0
)

st.sidebar.header("User Inputs")

age = st.sidebar.number_input("Age", min_value=10, max_value=100, value=30)
gender = st.sidebar.selectbox("Gender", ["Male", "Female"])

if unit_system == "Standard":
    weight_lbs = st.sidebar.number_input("Current Weight (lbs)", min_value=66.0, max_value=650.0, value=180.0)
    goal_weight_lbs = st.sidebar.number_input("Goal Weight (lbs)", min_value=66.0, max_value=650.0, value=160.0)
    height_feet = st.sidebar.number_input("Height - Feet", min_value=2, max_value=8, value=5)
    height_inches = st.sidebar.number_input("Height - Inches", min_value=0, max_value=11, value=9)

    weight_kg = weight_lbs * 0.45359237
    goal_weight_kg = goal_weight_lbs * 0.45359237
    total_inches = (height_feet * 12) + height_inches
    height_m = total_inches * 0.0254

else:
    weight_kg = st.sidebar.number_input("Current Weight (kg)", min_value=30.0, max_value=300.0, value=80.0)
    goal_weight_kg = st.sidebar.number_input("Goal Weight (kg)", min_value=30.0, max_value=300.0, value=72.5)
    height_m = st.sidebar.number_input("Height (meters)", min_value=1.0, max_value=2.5, value=1.75)

    weight_lbs = weight_kg / 0.45359237
    goal_weight_lbs = goal_weight_kg / 0.45359237
    total_inches = height_m / 0.0254
    height_feet = int(total_inches // 12)
    height_inches = int(round(total_inches % 12))

    if height_inches == 12:
        height_feet += 1
        height_inches = 0

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


# Calculate BMI

bmi = weight_kg / (height_m ** 2)

if bmi < 10 or bmi > 60:
    st.warning("Input values may be unrealistic. Please double-check.")

goal_direction = get_goal_direction(weight_lbs, goal_weight_lbs)
weight_difference_lbs = weight_lbs - goal_weight_lbs
weight_difference_kg = weight_kg - goal_weight_kg


# Build prediction input

user_df = pd.DataFrame([{
    "age": age,
    "gender": gender,
    "weight_kg": weight_kg,
    "goal_weight_kg": goal_weight_kg,
    "height_m": height_m,
    "workout_frequency_days_week": freq,
    "experience_level": exp,
    "bmi": bmi,
    "session_duration_hours": duration,
}])

user_df["recommended_workout"] = user_df.apply(recommend_workout, axis=1)

recommended_workout = user_df["recommended_workout"].iloc[0]

# Only pass model features the trained model expects

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

model_input_df = user_df[feature_order]

predicted_calories = int(round(model.predict(model_input_df)[0], 0))


# Generate actual workout plan

workout_plan, planned_minutes = get_workout_plan(recommended_workout, exp, duration)


# Output

st.markdown("---")
st.subheader("Recommendation Results")
st.markdown("---")

if unit_system == "Standard":
    st.write(f"**Current Weight:** {weight_lbs:.1f} lbs")
    st.write(f"**Goal Weight:** {goal_weight_lbs:.1f} lbs")
    st.write(f"**Weight Difference:** {weight_difference_lbs:.1f} lbs")
    st.write(f"**Entered Height:** {height_feet} ft {height_inches} in")
else:
    st.write(f"**Current Weight:** {weight_kg:.1f} kg")
    st.write(f"**Goal Weight:** {goal_weight_kg:.1f} kg")
    st.write(f"**Weight Difference:** {weight_difference_kg:.1f} kg")
    st.write(f"**Entered Height:** {height_m:.2f} m")

st.write(f"**Goal Direction:** {goal_direction}")
st.write(f"**Calculated BMI:** {bmi:.2f}")
st.write(f"**Recommended Workout Type:** {recommended_workout}")
st.write(f"**Estimated Calories Burned:** {predicted_calories}")
st.write(f"**Requested Workout Length:** {int(duration * 60)} minutes")
st.write(f"**Planned Workout Length:** {planned_minutes} minutes")

st.subheader("Suggested Workout Plan for Your Selected Session Length")
for exercise in workout_plan:
    st.markdown(f"- {exercise}")
