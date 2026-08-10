# Design & Implementation of Facial Recognition Attendance System

### تصميم وتنفيذ نظام تسجيل الحضور باستخدام التعرف على الوجوه

> **Student / Client:** Bidaa Abbas Alwan
> **Supervisor:** Mustafa Hameed Abdul-Sada

## 📋 Project Overview

Automated classroom attendance system using face recognition (face_recognition library) with face encoding database, Excel export for attendance logs, and Arduino LCD integration.

## 🛠️ Technologies Used

- Python
- Face Recognition
- OpenCV
- Pickle
- Tkinter
- Excel (XlsxWriter)
- Arduino + LCD
- PySerial

## ✨ Key Features

- ✅ Face enrollment (100 frames per person for accuracy)
- ✅ Real-time multi-face recognition with name overlay
- ✅ Automated attendance marking with timestamps
- ✅ Excel/CSV attendance report export
- ✅ Welcome greeting / voice prompts (pyttsx3) + Arduino LCD
- ✅ Customizable full-screen GUI with background

## 📁 Repository Structure

```
bedaa/
├── src/              # Source code (Python / Arduino .ino)
├── app/              # Desktop / web application
├── models/           # Trained ML models, weights, encodings
├── data/             # Datasets, pickled encodings, databases
├── hardware/         # Arduino sketches (.ino), schematics
├── docs/             # Research papers, Word documents (.docx)
└── assets/           # Images, diagrams, screenshots
```

## 🏗️ Hardware / System Block Diagram

*(Refer to docs folder for detailed schematics, pinouts, and wiring diagrams in the project Word document)*

## 🚀 Setup & Installation

### Python Projects
```bash
# 1. Create virtual environment
python -m venv .venv
.venv\Scripts\activate      # Windows

# 2. Install dependencies
pip install -r requirements.txt   # or installreq.py for automated installs

# 3. Run the application
python app.py
```

### Arduino Projects
1. Install **Arduino IDE** (2.x recommended)
2. Install required libraries via Library Manager (project-specific)
3. Open the `.ino` sketch from `hardware/` folder
4. Select correct board & COM port → Upload

## 🧑‍🎓 Project Context

This project is part of a series of **academic graduation / personal portfolio projects** (Computer Techniques Engineering, 2024-2025). Full research papers, circuit diagrams, and documentation are included in the respective `docs/` directories.
---

## 📝 Copyright & Ownership

**© 2026 Alaa Ahmed Ajeel (علاء أحمد عجيل) - All Rights Reserved**

> **Author & Designer:** Alaa Ahmed Ajeel
> **GitHub:** [@alaajake](https://github.com/alaajake)

This project was fully **developed, written, designed, and implemented** by **Alaa Ahmed Ajeel** as part of academic graduation projects and personal research work.

Customized working copies of these projects have been delivered to clients/students, while this original source code repository remains the property of the author under full copyright protection.

**Unauthorized copying, modification, distribution, or commercial use of this code, via any medium, is strictly prohibited without prior written permission from the author.**
