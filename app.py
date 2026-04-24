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

    # Goal-based logic
    if weight_gap_kg >= 4.5:
        if row["experience_level"] >= 3:
            return "HIIT"
        return "Cardio"

    elif weight_gap_kg <= -2.3:
        return "Strength"

    # Default logic
    if row["bmi"] >= 30:
        return "Cardio"
    elif row["experience_level"] == 1:
        return "Strength"
    elif row["experience_level"] >= 3:
        return "HIIT"
    else:
        return "Yoga"


# Target heart rate logic
def get_target_heart_rate(age, workout_type):
    max_heart_rate = 220 - age

    if workout_type == "Yoga":
        low_percent = 0.50
        high_percent = 0.60
    elif workout_type == "Strength":
        low_percent = 0.60
        high_percent = 0.70
    elif workout_type == "Cardio":
        low_percent = 0.65
        high_percent = 0.80
    elif workout_type == "HIIT":
        low_percent = 0.80
        high_percent = 0.90
    else:
        low_percent = 0.50
        high_percent = 0.70

    low_target = int(max_heart_rate * low_percent)
    high_target = int(max_heart_rate * high_percent)

    return low_target, high_target


# Calorie target logic
def get_calorie_target(age, gender, weight_kg, height_m, workout_frequency, weight_difference_lbs):
    height_cm = height_m * 100

    # Mifflin-St Jeor BMR estimate
    if gender == "Male":
        bmr = (10 * weight_kg) + (6.25 * height_cm) - (5 * age) + 5
    else:
        bmr = (10 * weight_kg) + (6.25 * height_cm) - (5 * age) - 161

    # Activity multiplier based on workout frequency
    if workout_frequency <= 1:
        activity_multiplier = 1.2
    elif workout_frequency <= 3:
        activity_multiplier = 1.375
    elif workout_frequency <= 5:
        activity_multiplier = 1.55
    else:
        activity_multiplier = 1.725

    maintenance_calories = bmr * activity_multiplier

    # Adjust based on goal
    if weight_difference_lbs > 5:
        calorie_target = maintenance_calories - 500
        goal_type = "Weight loss"
    elif weight_difference_lbs < -5:
        calorie_target = maintenance_calories + 300
        goal_type = "Weight gain"
    else:
        calorie_target = maintenance_calories
        goal_type = "Maintenance"

    return int(round(maintenance_calories)), int(round(calorie_target)), goal_type

# estimated timeline to hit goal
def get_goal_timeline(weight_difference_lbs, goal_type, maintenance_calories, calorie_target, predicted_calories, workout_frequency):
    pounds_to_change = abs(weight_difference_lbs)

    if pounds_to_change <= 5:
        return "Already near goal", 0, 0

    daily_food_difference = maintenance_calories - calorie_target

    weekly_food_difference = daily_food_difference * 7
    weekly_workout_difference = predicted_calories * workout_frequency

    if goal_type == "Weight loss":
        weekly_calorie_difference = weekly_food_difference + weekly_workout_difference
    elif goal_type == "Weight gain":
        weekly_calorie_difference = abs(weekly_food_difference) - weekly_workout_difference
    else:
        return "Maintenance goal", 0, 0

    if weekly_calorie_difference <= 0:
        return "Goal timeline cannot be estimated with the current calorie target and workout plan", 0, weekly_calorie_difference

    total_calories_needed = pounds_to_change * 3500
    estimated_weeks = total_calories_needed / weekly_calorie_difference
    estimated_months = estimated_weeks / 4.345

    timeline_text = f"Approximately {estimated_weeks:.1f} weeks ({estimated_months:.1f} months)"

    return timeline_text, estimated_weeks, weekly_calorie_difference

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


# BMI classification logic

def get_bmi_category(bmi):
    if bmi < 18.5:
        return "Underweight"
    elif bmi < 25:
        return "Normal weight"
    elif bmi < 30:
        return "Overweight"
    else:
        return "Obese"


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
    weight_lbs = st.sidebar.number_input("Current Weight (lbs)", min_value=66, max_value=650, value=180, step=1)
    goal_weight_lbs = st.sidebar.number_input("Goal Weight (lbs)", min_value=66, max_value=650, value=160, step=1)
    height_feet = st.sidebar.number_input("Height - Feet", min_value=2, max_value=8, value=5, step=1)
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


# Calculate BMI and goal information

bmi = weight_kg / (height_m ** 2)
goal_bmi = goal_weight_kg / (height_m ** 2)

bmi_category = get_bmi_category(bmi)
goal_bmi_category = get_bmi_category(goal_bmi)

if bmi < 10 or bmi > 60:
    st.warning("Input values may be unrealistic. Please double-check.")

goal_direction = get_goal_direction(weight_lbs, goal_weight_lbs)
weight_difference_lbs = weight_lbs - goal_weight_lbs
weight_difference_kg = weight_kg - goal_weight_kg

maintenance_calories, calorie_target, goal_type = get_calorie_target(
    age,
    gender,
    weight_kg,
    height_m,
    freq,
    weight_difference_lbs
)


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

target_hr_low, target_hr_high = get_target_heart_rate(age, recommended_workout)

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

goal_timeline, estimated_weeks, weekly_calorie_difference = get_goal_timeline(
    weight_difference_lbs,
    goal_type,
    maintenance_calories,
    calorie_target,
    predicted_calories,
    freq
)

weekly_weight_change = weekly_calorie_difference / 3500

# Generate actual workout plan

workout_plan, planned_minutes = get_workout_plan(recommended_workout, exp, duration)


# Output

st.markdown("---")
st.subheader("Recommendation Results")
st.markdown("---")

if unit_system == "Standard":
    st.write(f"**Current Weight:** {int(weight_lbs)} lbs")
    st.write(f"**Goal Weight:** {int(goal_weight_lbs)} lbs")
    st.write(f"**Goal vs Current Weight Gap:** {weight_difference_lbs} lbs")
    st.write(f"**Entered Height:** {height_feet} ft {height_inches} in")
else:
    st.write(f"**Current Weight:** {weight_kg:.1f} kg")
    st.write(f"**Goal Weight:** {goal_weight_kg:.1f} kg")
    st.write(f"**Goal vs Current Weight Gap:** {weight_difference_kg:.1f} kg")
    st.write(f"**Entered Height:** {height_m:.2f} m")

st.write(f"**Goal Type:** {goal_type}")
st.write(f"**Calculated BMI:** {bmi:.2f} ({bmi_category})")
st.write(f"**BMI at Goal Weight:** {goal_bmi:.2f} ({goal_bmi_category})")
st.write(f"**Recommended Workout Type:** {recommended_workout}")
st.write(f"**Target Heart Rate Range:** {target_hr_low}-{target_hr_high} BPM")
st.write(f"**Estimated Calories Burned:** {predicted_calories}")
st.write(f"**Estimated Maintenance Calories:** {maintenance_calories} calories/day")
st.write(f"**Recommended Daily Calorie Intake:** {calorie_target} calories/day")
st.caption("Calorie intake is an estimate based on user inputs and should not replace medical advice.")
if goal_type == "Weight loss":
    st.write(f"**Estimated Weekly Weight Loss:** {weekly_weight_change:.2f} lbs/week")
elif goal_type == "Weight gain":
    st.write(f"**Estimated Weekly Weight Gain:** {weekly_weight_change:.2f} lbs/week")
st.write(f"**Estimated Timeline to Goal Weight:** {goal_timeline}")
st.write(f"**Requested Workout Length:** {int(duration * 60)} minutes")
st.write(f"**Planned Workout Length:** {planned_minutes} minutes")


st.subheader("Suggested Workout Plan for Your Selected Session Length")
for exercise in workout_plan:
    st.markdown(f"- {exercise}")