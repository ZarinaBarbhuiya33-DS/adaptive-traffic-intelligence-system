# 🚦 Adaptive Multi-Level Urban Traffic Intelligence System

**Woxsen University Capstone Project**  
**Lead Developer:** Zarina  

An advanced AI-driven traffic management prototype that shifts urban congestion control from reactive to proactive. By combining Graph Attention Networks (GAT) and Long Short-Term Memory (LSTM) networks, this system forecasts 15-60 minute bottleneck risks and allocates traffic signal phases using a Max-Pressure algorithm constrained by Jain’s Fairness Index.

---

## 🧠 Core Architecture
*   **Micro-Simulation Engine (SUMO):** Generates physical traffic dynamics and intersection state vectors via the TraCI API.
*   **Predictive AI (PyTorch):** A GAT-LSTM neural network ensemble that extracts spatial road network dependencies and temporal traffic flow sequences to map future gridlock probabilities.
*   **Fairness Controller:** Replaces standard throughput-optimizing algorithms with a Jain's Fairness Index penalizer to actively prevent secondary-lane starvation.
*   **Command Center UI (Streamlit & PyDeck):** A 3D geospatial dashboard for live telemetry, real-time risk mapping, and autonomous phase control visualization.

## 📁 Repository Structure
```text
traffic-intelligence-system/
├── sumo_network/
│   ├── osm.net.xml           # Hyderabad road network geometry
│   └── osm.rou.xml           # Vehicle routes and traffic demand flow
├── src/
│   └── presentation.py       # Live Streamlit Command Center application
├── GAT_LSTM_Training.ipynb   # PyTorch model training and architecture math
├── requirements.txt          # Python environment dependencies
└── README.md
