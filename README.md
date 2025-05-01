# Cyber Threat Detection System

This project is a web application that monitors a specified website for cyber threats and displays detected threats in real-time.

## Features

- Start and stop monitoring a website for cyber threats.
- Simulated threat detection with random threat generation.
- Real-time threat detection log displayed in the frontend.
- Responsive and professional UI built with React and Material-UI.
- Backend API built with Flask.

## Getting Started

### Prerequisites

- Python 3.x
- Node.js and npm

### Backend Setup

1. Navigate to the `backend` directory:
   ```bash
   cd backend
   ```

2. Create and activate a virtual environment (optional but recommended):
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install backend dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Run the backend server:
   ```bash
   python app.py
   ```

   The backend server will start on `http://0.0.0.0:5001`.

### Frontend Setup

1. Navigate to the `frontend` directory:
   ```bash
   cd frontend
   ```

2. Install frontend dependencies:
   ```bash
   npm install
   ```

3. Run the frontend development server:
   ```bash
   npm start
   ```

   The frontend will be available at `http://localhost:3000`.

### Usage

- Open the frontend in your browser.
- Enter the website URL you want to monitor.
- Click "Start Monitoring" to begin threat detection.
- Detected threats will appear in the threat detection log.
- Click "Stop Monitoring" to stop the monitoring process.

### Notes on Threat Simulation

- The backend simulates threat detection only for specific malicious URLs:
  - https://urlhaus.abuse.ch/static/malware/2023/02/15/abcdef1234567890.exe
  - http://secure-login-paypal.com/account-update
  - https://urlhaus.abuse.ch/static/malware/2023/01/01/1a2b3c4d5e6f7g8h9i0j.exe
  - http://phishing-example.com/login
  - http://fakebank.phishingsite.com
- For these URLs, 30 different threat types are simulated and refreshed every 12 seconds.
- For safe URLs (including a whitelist of common safe domains), the UI will show a message indicating the URL is safe and no threats are detected.

## License

This project is licensed under the MIT License.

## Author

Abishek
