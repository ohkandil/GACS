import joblib
from datetime import datetime
from sensors.motion_sensors import arm_motion_sensor

# Load the trained model
model = joblib.load("ai_motion_model.pkl")

def get_ai_decision(frequency):
    now = datetime.now()
    hour = now.hour
    minute = now.minute
    day_of_week = now.weekday()

    # Dummy historical average for simplicity (replace with actual logic)
    historical_average = 5

    # Prepare feature vector
    features = [[hour, minute, day_of_week, frequency, historical_average]]

    # Predict (1 = Arm, 0 = Disarm)
    decision = model.predict(features)[0]
    return decision

def ai_controller():
    # Example: Frequency of motion events in the past 10 minutes
    detection_frequency = 10  # Replace with actual calculation

    # Get AI decision
    decision = get_ai_decision(detection_frequency)
    if decision == 1:
        print("AI Decision: Arm the sensor.")
        arm_motion_sensor()  # Arm the sensor
    else:
        print("AI Decision: Disarm the sensor.")
        arm_motion_sensor()  # Disarm the sensor
