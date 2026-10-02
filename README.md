Multimodal Tactile & Spatial Sensor Fusion Pipeline
A dual-brain multimodal data pipeline that fuses 5DT tactile-glove kinematics and MediaPipe spatial tracking into a neuro-symbolic Unity dashboard.

🧠 System Architecture
This project solves a strict hardware/software architectural constraint: the proprietary fglove.dll requires a legacy 32-bit Python environment, while modern AI like MediaPipe requires a 64-bit environment. To prevent crashes, the pipeline isolates the hardware streams into two separate asynchronous Python transmitters and bridges them over local UDP ports to a unified C# receiver in Unity.

Node 1 (32-bit Python): Extracts 5-finger float arrays from the 5DT Glove via USB. Broadcasts on UDP Port 5xxx. 5DT glove isn't allowing 64-bit modules.
Node 2 (64-bit Python): Extracts wrist X, Y, Z spatial coordinates using OpenCV/MediaPipe. Broadcasts on UDP Port 5xxx.
Node 3 (Unity Engine): A dual-threaded C# script ingests both streams simultaneously without frame-blocking, mapping the data to a 2D scrolling waveform UI and a live 3D spatial hand model.
📁 Repository Structure
├── python_32bit_tactile/      # 32-bit environment for 5DT Glove
│   └── transmitter.py         # Broadcasts finger kinematics to Port 5xxx
├── python_64bit_spatial/      # 64-bit environment for MediaPipe
│   ├── camera_tracker.py      # Broadcasts spatial coordinates to Port 5xxx
│   └── requirements.txt       # OpenCV and MediaPipe dependencies
├── unity_dashboard/           # Unity project containing the C# Receiver
│   ├── Assets/Scripts/        # Contains GloveReceiver.cs
│   └── ...                    
└── docs/                      # Pipeline documentation and HTML flowcharts

Hardware Requirements
5DT Data Glove (USB/COM connection)
Standard RGB Webcam (1080p recommended)
Windows OS (Required for fglove.dll execution)

Installation & Execution
1. Set up the Tactile Environment (32-bit)
You must use a 32-bit installation of Python for this step.

Download the official 5DT SDK and place your fglove.dll file directly into the python_32bit_tactile directory.
Open a 32-bit terminal and run:
python python_32bit_tactile/transmitter.py
2. Set up the Spatial Environment (64-bit)
Open a separate 64-bit terminal (e.g., Anaconda).
Install the dependencies and run the tracker:
pip install -r python_64bit_spatial/requirements.txt
python python_64bit_spatial/camera_tracker.py

Launch the Unity Fusion Dashboard
Open the unity_dashboard folder in Unity Hub (Unity 2022+ recommended).
Open the Main Scene and press Play.
Hardware Calibration: Once running, stretch your fingers backward as far as possible for one second, then squeeze them into a tight fist. This calibrates the absolute minimum and maximum thresholds for the 3D hand model.
