# 🛡️ Voice Recognition-Scam Detection System (VR-SDS)

### **👨‍💻 About the Developer**
I am **See Dez-Mond**, a dedicated Information Technology student at **Universiti Utara Malaysia (UUM)**, specializing in **Software Development**. I have a deep interest in building secure, AI-driven solutions that protect users from digital threats. This project represents my Final Year Project (FYP) journey, where I combine full-stack development with real-time audio analytics to combat the growing issue of phone-based scams.

### **🚀 Project Overview**
The **VR-SDS** is an intelligent security ecosystem designed to identify and block fraudulent calls and messages before they can harm the user. Unlike traditional filters, this system uses **Voice Recognition** and **Natural Language Processing (NLP)** to analyze conversations in real-time, providing an active shield for digital communication.



### **✨ Key Features**
* **🔴 Real-Time Call Shield**: Monitors incoming audio streams in 3-second segments to detect scam patterns as they happen.
* **⚖️ Dual-Layer Verification**: Processes both audio (Voice) and text (SMS/Messages) to ensure comprehensive protection.
* **🔐 Permission-Based Security**: Implements a strict "Permission Gate" that respects user privacy by requesting access before monitoring any incoming stream.
* **📊 Admin & User Analytics**: Features specialized dashboards for monitoring system health, scam trends, and personal protection history.
* **🐳 Dockerized Infrastructure**: Fully containerized using Docker and Docker Compose for seamless deployment across different environments.

### **🛠️ Technical Stack**
* **Frontend**: Streamlit (Python-based interactive UI).
* **Backend**: Python 3.9+ with SQLAlchemy for database management.
* **Database**: MySQL 8.0 hosted via Docker containers.
* **AI/Audio**: Librosa for MFCC feature extraction and pre-trained Machine Learning models.
* **DevOps**: GitHub Actions for CI/CD and Git for Version Control (Version 1.2).

---

### **🔧 Installation & Setup Guide**
All Model and Dataset must be trained By your Own.

Follow these steps to set up the environment on your local machine:

#### **1. Prerequisites**
Ensure you have the following installed on your PC:
* **Docker Desktop**: Required to run the database and web containers.
* **Python 3.9+**: For local testing and library management.
* **Git**: To clone and manage repository versions.

#### **2. Clone the Repository**
Open your terminal and run:
```bash
git clone -b version-1.2 [https://github.com/DezmondSee/Voice-Recognition-Scam-Detection-System-VR-SDS-.git](https://github.com/DezmondSee/Voice-Recognition-Scam-Detection-System-VR-SDS-.git)
cd Voice-Recognition-Scam-Detection-System-VR-SDS-


