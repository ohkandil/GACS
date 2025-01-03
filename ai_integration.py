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
    while True:
        try:
            # Read recent data from CSV
            with open(history_data.HISTORY_FILE, 'r') as file:
                recent_data = pd.read_csv(file)
                
            # Calculate detection frequency in last 10 minutes
            now = datetime.now()
            cutoff = now - timedelta(minutes=10)
            recent_data['timestamp'] = pd.to_datetime(recent_data['timestamp'])
            recent_events = recent_data[recent_data['timestamp'] > cutoff]
            
            # Check each sensor
            for sensor_id in [1, 2]:
                sensor_events = len(recent_events[recent_events['sensor_id'] == sensor_id])
                
                # Get AI prediction
                decision = get_ai_decision(sensor_events)
                
                # Control servos via Blynk if motion is unexpected
                if sensor_events > 0 and decision == 0:  # Unexpected motion
                    if sensor_id == 1:
                        blynk_tst.v1_write_handler(['1'])
                    else:
                        blynk_tst.v2_write_handler(['1'])
                        
            time.sleep(5)  # Check every 5 seconds
            
        except Exception as e:
            print(f"Error in AI controller: {e}")
            time.sleep(1)
