# Carbon-Ghost


**Making carbon impact visible in real time.**

Carbon Ghost is a real-time, camera-based system that visualizes the environmental impact of everyday objects using an AR-style “ghost” overlay. Instead of showing carbon footprints as numbers or reports, Carbon Ghost provides instant visual feedback to increase climate awareness and encourage sustainable choices.

---

## 🌍 Problem Statement

Carbon impact is largely invisible in everyday life. Existing carbon footprint tools rely on dashboards, charts, or reports that are difficult to understand, not real-time, and shown after actions are already completed. This makes it hard for people to connect their daily choices with environmental consequences.

---

## 💡 Solution

Carbon Ghost transforms invisible carbon impact into a visible experience. By using a live camera feed, the system analyzes objects in front of the user and displays a ghost-like visual whose size and intensity represent environmental impact.

* Low-impact objects → small, light ghost
* High-impact objects → large, dark ghost
* Humans are automatically detected and ignored for ethical use

This real-time visual feedback makes carbon awareness intuitive, immediate, and accessible to everyone.

---

## ✨ Key Features

* 📷 Real-time camera-based object analysis
* 🧠 Lightweight AI-based impact inference
* 👻 AR-style carbon ghost visualization
* 🧍 Automatic human detection and exclusion
* ⚡ Real-time, low-latency performance
* ☁️ Firebase Realtime Database integration (data only)
* 🔒 Privacy-friendly (no images or video stored)
* 📈 Scalable and hackathon-ready architecture

---

## 🛠️ Technologies Used

* **Python** – Core application logic
* **OpenCV** – Camera access and image processing
* **NumPy** – Image and numerical operations
* **Firebase Realtime Database** – Event logging and backend storage
* **Firebase REST API** – Communication between local app and cloud

---

## 🧩 Architecture Overview

* All computer vision and AR visualization run **on-device** for real-time performance and privacy.
* Firebase is used **only for data logging**, such as object type and timestamp.
* No camera frames or images are sent to the cloud.

This edge-first architecture ensures smooth performance and ethical data handling.

---

## 🔄 Process Flow

1. User opens the application
2. Camera captures live surroundings
3. System checks for human presence
4. If human detected → no carbon impact shown
5. If object detected → impact analysis performed
6. Carbon Ghost visual appears in real time
7. Impact event is logged to Firebase

---

## 🚀 Getting Started

### Prerequisites

* Python 3.8+
* macOS / Linux (camera access required)

### Installation

```bash
pip install opencv-python numpy requests
```

### Run the Application

```bash
python main.py
```

*(Replace `main.py` with your script name if different.)*

---

## 📊 Demo

* Live camera demo showing ghost visualization
* Firebase console displaying real-time event logs

---

## 🔮 Future Scope

* 📱 Mobile AR version (ARCore / ARKit)
* 🌍 Region-based carbon scoring
* 📈 User dashboards and analytics
* 🏆 Gamification for sustainable behavior
* 🏢 Deployment in campuses, offices, and public spaces

---

## 📜 License

This project is licensed under the **MIT License**. See the `LICENSE` file for details.

---

## 🙌 Acknowledgements

* OpenCV community
* Firebase by Google
* Hackathon mentors and organizers

---

## 📌 One-Line Summary

> Carbon Ghost makes invisible carbon impact visible through real-time visual feedback.
