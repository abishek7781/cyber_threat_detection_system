import React, { useEffect, useState } from 'react';

function App() {
  const [logs, setLogs] = useState([]);
  const [threatDetected, setThreatDetected] = useState(false);
  const [monitoring, setMonitoring] = useState(false);

  useEffect(() => {
    const eventSource = new EventSource('http://localhost:5001/stream');

    eventSource.onmessage = (event) => {
      try {
        const data = JSON.parse(event.data);
        console.log("Received SSE data:", data);
        if (Array.isArray(data)) {
          setLogs(data);
          setThreatDetected(data.length > 0);
          // Check if safe site message is present
          const safeMessage = data.find(log => log.threat_name === "Safe Site");
          if (safeMessage) {
            console.log("Safe site message found:", safeMessage.message);
            alert(safeMessage.message);
          }
        } else {
          console.warn('SSE data is not an array:', data);
          setThreatDetected(false);
        }
      } catch (error) {
        console.error('Error parsing SSE data:', error);
        setThreatDetected(false);
      }
    };

    eventSource.onerror = (error) => {
      console.error('SSE error:', error);
      eventSource.close();
    };

    return () => {
      eventSource.close();
    };
  }, []);

  // Download logs as JSON file
  const downloadLogs = () => {
    const element = document.createElement('a');
    const file = new Blob([JSON.stringify(logs, null, 2)], { type: 'application/json' });
    element.href = URL.createObjectURL(file);
    element.download = 'threat_logs.json';
    document.body.appendChild(element);
    element.click();
    document.body.removeChild(element);
  };

  return (
    <div style={{ padding: '20px', fontFamily: 'Arial, sans-serif' }}>
      <h2>Threat Log</h2>
      <div style={{ border: '1px solid #ccc', padding: '10px', height: '400px', overflowY: 'scroll', backgroundColor: '#f9f9f9' }}>
        {monitoring && !threatDetected ? (
          <p>Site is safe. No threats detected.</p>
        ) : logs.length === 0 ? (
          <p>No logs available</p>
        ) : (
          logs.map(log => (
            <div key={log.id} style={{ marginBottom: '15px', paddingBottom: '10px', borderBottom: '1px solid #ddd' }}>
              <div><strong>Time:</strong> {log.timestamp}</div>
              <div><strong>Threat:</strong> {log.threat_name}</div>
              <div><strong>Location:</strong> {log.threat_location || log.website || 'N/A'}</div>
              <div><strong>Message:</strong> {log.message}</div>
              <div><strong>Solution:</strong> {log.solution}</div>
              <div><strong>Severity:</strong> {log.severity || 'N/A'}</div>
            </div>
          ))
        )}
      </div>
      <button onClick={downloadLogs} style={{ marginTop: '10px', padding: '8px 16px', cursor: 'pointer' }}>
        Download Logs
      </button>
    </div>
  );
}

export default App;
