# Coordinated Vehicle Platooning

## Overview
Coordinated Vehicle Platooning is an AI-powered system that enhances traffic efficiency by allowing vehicles to travel in an organized manner. This project consists of two main components:
- **Sender (Leader Vehicle)**: Takes input (speed & distance), predicts traffic congestion, and sends lane suggestions.
- **Receiver (Follower Vehicle)**: Receives real-time traffic data and displays lane suggestions.

The system utilizes **AI (Decision Tree)** for traffic prediction, **MQTT** for communication, and **Gradio** for a user-friendly interface.

---

## Features
✅ **Real-time AI-based traffic prediction**  
✅ **Live vehicle communication using MQTT**  
✅ **Interactive web UI (Gradio) for both sender & receiver**  
✅ **Dynamic lane suggestion for better traffic management**  

---

## Technologies Used
- **Python**
- **Gradio** (Web UI)
- **Paho-MQTT** (Communication protocol)
- **Pandas & Scikit-learn** (AI Model for traffic prediction)

---

## Installation & Setup

### 1️⃣ Install Dependencies
Run the following command to install required Python packages:
```bash
pip install gradio paho-mqtt pandas scikit-learn
```

### 2️⃣ Run the Sender (Leader) Code
Create a file **`sender.py`** and copy the following:
```python
import gradio as gr
import pandas as pd
from sklearn.tree import DecisionTreeRegressor
import paho.mqtt.client as mqtt
import json

# Train Decision Tree Model
traffic_data = pd.DataFrame({
    'speed': [10, 20, 30, 40, 50, 60, 70, 80],
    'distance': [50, 40, 35, 30, 25, 20, 15, 10],
    'traffic_level': [10, 20, 35, 50, 65, 80, 90, 100]
})

X = traffic_data[['speed', 'distance']]
y = traffic_data['traffic_level']

model = DecisionTreeRegressor()
model.fit(X, y)

# MQTT Setup
MQTT_BROKER = "test.mosquitto.org"
TOPIC_SPEED = "platoon/speed"
client = mqtt.Client()
client.connect(MQTT_BROKER, 1883, 60)

# Prediction & Sending Function
def predict_traffic(speed, distance):
    return int(model.predict([[speed, distance]])[0])

def decide_lane(congestion_level):
    return "Stay" if congestion_level < 40 else "Go Right"

def send_data(speed, distance):
    congestion_level = predict_traffic(speed, distance)
    lane_suggestion = decide_lane(congestion_level)
    
    data = {
        "speed": speed,
        "distance": distance,
        "congestion_level": congestion_level,
        "lane_suggestion": lane_suggestion
    }
    
    client.publish(TOPIC_SPEED, json.dumps(data))
    return f"📡 Sent: Speed={speed} km/h, Distance={distance} m, Traffic={congestion_level}%, Lane={lane_suggestion}"

# Gradio UI
iface = gr.Interface(
    fn=send_data,
    inputs=[gr.Number(label="Enter Speed (km/h)"), gr.Number(label="Enter Distance (m)")],
    outputs="text",
    title="🚗 Leader (Sender) - Platoon System",
    description="Enter speed and distance to send real-time data to the follower."
)

iface.launch()
```
Run it using:
```bash
python sender.py
```

### 3️⃣ Run the Receiver (Follower) Code
Create a file **`receiver.py`** and copy the following:
```python
import gradio as gr
import paho.mqtt.client as mqtt
import json

# Global variables to store received data
traffic_level = "Waiting for data..."
lane_suggestion = "Waiting for data..."

# MQTT Setup
MQTT_BROKER = "test.mosquitto.org"
TOPIC_SPEED = "platoon/speed"

def on_message(client, userdata, msg):
    global traffic_level, lane_suggestion
    data = json.loads(msg.payload)
    
    traffic_level = f"🚦 Traffic Level: {data['congestion_level']}%"
    lane_suggestion = f"🚗 Lane Suggestion: {data['lane_suggestion']}"

def get_data():
    return traffic_level, lane_suggestion

# MQTT Client Setup
client = mqtt.Client()
client.on_message = on_message
client.connect(MQTT_BROKER, 1883, 60)
client.subscribe(TOPIC_SPEED)
client.loop_start()

# Gradio UI
iface = gr.Interface(
    fn=get_data,
    inputs=[],
    outputs=["text", "text"],
    title="🚘 Follower (Receiver) - Platoon System",
    description="Displays real-time traffic congestion and lane suggestions received from the Leader.",
    live=True  # Auto-refresh data
)

iface.launch()
```
Run it using:
```bash
python receiver.py
```

---

## How It Works
1️⃣ **Leader enters speed & distance**  
2️⃣ **Traffic congestion is predicted using AI**  
3️⃣ **Lane decision (Stay/Go Right) is determined**  
4️⃣ **Data is sent via MQTT to the Follower**  
5️⃣ **Follower receives & displays the information in real-time**  

---

## Future Enhancements
🚀 **Advanced AI for more accurate traffic prediction**  
🚀 **Integration with real-time GPS & sensor data**  
🚀 **V2V communication with multiple vehicles**  

---

## Conclusion
Coordinated Vehicle Platooning enhances traffic efficiency by enabling real-time AI-driven decision-making. The use of MQTT ensures seamless communication between vehicles, while Gradio provides an easy-to-use interface.

📌 **Next Steps?** Test the system on multiple devices and integrate with real-world vehicle data! 🚗💨

