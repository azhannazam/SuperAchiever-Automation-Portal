# 🚀 SuperE Digitalization & Automation Portal

This system automates the processing of **Report 316** from Etiqa, manages the **Daily Submissions** database, and provides a live **Contest Dashboard** for agents and admins.

## 🛠 Features
- **Automated Filtering:** Instantly extracts SuperE data from the master Etiqa Excel report.
- **Smart Alerts:** Automatically identifies cases pending for 3 or 7 days and notifies the admin.
- **Live Leaderboards:** Displays rankings for NAIS, Etiqa Contests, and New Agent Bonuses.
- **WhatsApp Integration:** Generates one-click WhatsApp links to contact agents regarding pending cases.

---

## 📂 Project Structure
- `app/`: Contains the core logic (Bot, Database, Alerts, UI).
- `data/`: Stores the SQLite database and raw report history.
- `config.py`: System-wide settings.
- `.env`: Private credentials (Email/Passwords).

---

## 🚀 How to Run the System

### 1. Setup Environment
Ensure you have Python installed. Install the required libraries:
```bash
pip install -r requirements.txt