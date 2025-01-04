import joblib
import pandas as pd
from datetime import datetime, timedelta
import time
import numpy as np
from sklearn.ensemble import RandomForestClassifier
import blynk_tst
from data_generate import SENSOR_LOG_FILE

class MotionAIController:
    def __init__(self):
        self.feature_names = ['hour', 'day_of_week', 'frequency']
        self.model = self.train_model()
        
    def train_model(self):
        try:
            return joblib.load("motion_model.pkl")
        except:
            print("Training new AI model...")
            model = RandomForestClassifier(n_estimators=100)
            
            X = pd.DataFrame([
                [8, 0, 5],     # Morning activity
                [12, 1, 3],    # Noon activity
                [18, 2, 4],    # Evening activity
                [2, 3, 10],    # Late night activity
                [3, 4, 8],     # Early morning activity
                [15, 5, 15]    # Unusual afternoon activity
            ], columns=self.feature_names)
            
            y = np.array([1, 1, 1, 0, 0, 0])
            model.fit(X, y)
            joblib.dump(model, "motion_model.pkl")
            return model
    
    def get_ai_decision(self, hour, day_of_week, frequency):
        features = pd.DataFrame([[hour, day_of_week, frequency]], 
                              columns=self.feature_names)
        return self.model.predict(features)[0]

def ai_controller():
    ai = MotionAIController()
    print("AI Motion Controller initialized")
    
    while True:
        try:
            recent_data = pd.read_csv(SENSOR_LOG_FILE)
            recent_data['timestamp'] = pd.to_datetime(recent_data['timestamp'])
            
            # Only consider readings under 10cm
            recent_data = recent_data[recent_data['distance'] <= 10]
            
            cutoff_time = datetime.now() - timedelta(minutes=10)
            recent_data = recent_data[recent_data['timestamp'] > cutoff_time]
            
            now = datetime.now()
            
            for sensor_id in [1, 2]:
                sensor_data = recent_data[recent_data['sensor_id'] == sensor_id]
                
                if not sensor_data.empty:
                    frequency = len(sensor_data)
                    
                    decision = ai.get_ai_decision(
                        hour=now.hour,
                        day_of_week=now.weekday(),
                        frequency=frequency
                    )
                    
                    if decision == 0:  # Unexpected motion
                        print(f"Unexpected motion detected on sensor {sensor_id}")
                        value = ['1']  # Create list with single value
                        if sensor_id == 1:
                            blynk_tst.v1_write_handler(value)
                        else:
                            blynk_tst.v2_write_handler(value)
            
            time.sleep(5)
            
        except Exception as e:
            print(f"Error in AI controller: {e}")
            time.sleep(1)

if __name__ == "__main__":
    ai_controller()