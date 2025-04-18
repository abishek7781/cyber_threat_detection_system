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

## Notes

- This project simulates threat detection for demonstration purposes.
- Large files in `node_modules` are not included in the repository. Use `.gitignore` to exclude them.
- For production deployment, consider securing the API and optimizing performance.

## License

This project is licensed under the MIT License.

## Author

Abishek
