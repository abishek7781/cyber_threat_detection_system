import React, { useState, useEffect } from 'react';
import {
  TextField, Button, Container, Typography, Paper, Table, TableBody, TableCell,
  TableContainer, TableHead, TableRow, Chip, Box, Alert, AppBar, Toolbar,
  CssBaseline, useMediaQuery, Slide, Zoom, Grid, ThemeProvider, createTheme, Fade,
} from '@mui/material';
import { green, red, blue, grey } from '@mui/material/colors';

const theme = createTheme({
  palette: {
    primary: {
      main: '#1976d2', // Blue
    },
    secondary: {
      main: '#ff9800', // Orange
    },
    background: {
      default: '#f5f7fa',
      paper: '#ffffff',
    },
    error: {
      main: '#d32f2f',
    },
  },
  typography: {
    fontFamily: "'Roboto', 'Helvetica', 'Arial', sans-serif",
    h4: {
      fontWeight: 700,
      letterSpacing: '0.15em',
      color: '#1976d2',
    },
    h5: {
      fontWeight: 600,
      color: '#333',
    },
    button: {
      textTransform: 'none',
      fontWeight: 600,
    },
  },
  shape: {
    borderRadius: 10,
  },
  components: {
    MuiButton: {
      styleOverrides: {
        root: {
          boxShadow: '0 3px 10px rgba(255, 152, 0, 0.4)',
          transition: 'all 0.3s ease',
          '&:hover': {
            boxShadow: '0 6px 20px rgba(255, 152, 0, 0.7)',
          },
        },
      },
    },
    MuiPaper: {
      styleOverrides: {
        root: {
          boxShadow: '0 12px 24px rgba(0,0,0,0.12)',
          padding: '24px',
          borderRadius: 10,
        },
      },
    },
  },
});

function App() {
  const [website, setWebsite] = useState('');
  const [monitoringStatus, setMonitoringStatus] = useState('Idle');
  const [threatDetected, setThreatDetected] = useState(false);
  const [message, setMessage] = useState('');
  const [threatLogs, setThreatLogs] = useState([]);

  const isMobile = useMediaQuery(theme.breakpoints.down('sm'));

  const startMonitoring = async () => {
    console.log('Start Monitoring button clicked');
    if (!website) {
      setMessage('Please enter a website URL.');
      return;
    }
    setMessage('');
    try {
      const response = await fetch('http://127.0.0.1:5001/start_monitoring', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ website }),
      });
      const data = await response.json();
      console.log('Start monitoring response:', data);
      if (response.ok) {
        setMessage(data.message);
        setMonitoringStatus('Monitoring');
      } else {
        setMessage(data.error || 'Failed to start monitoring.');
      }
    } catch (error) {
      console.error('Error starting monitoring:', error);
      setMessage('Error connecting to backend.');
    }
  };

  const stopMonitoring = async () => {
    console.log('Stop Monitoring button clicked');
    try {
      const response = await fetch('http://127.0.0.1:5001/stop_monitoring', { method: 'POST' });
      console.log('Stop monitoring response:', response);
      if (response.ok) {
        setMonitoringStatus('Idle');
        setThreatDetected(false);
        setThreatLogs([]);
        setMessage('Monitoring stopped.');
      } else {
        setMessage('Failed to stop monitoring.');
      }
    } catch (error) {
      console.error('Error stopping monitoring:', error);
      setMessage('Error connecting to backend.');
    }
  };

  useEffect(() => {
    localStorage.removeItem('monitoringStatus');
    localStorage.removeItem('threatDetected');
    localStorage.removeItem('threatLogs');
    setThreatLogs([]);

    let interval = null;

      if (monitoringStatus === 'Monitoring') {
        interval = setInterval(async () => {
          try {
            const response = await fetch('http://127.0.0.1:5001/status');
            const data = await response.json();
            setMonitoringStatus(data.status);
            setThreatDetected(data.threat_detected);

            const logsResponse = await fetch('http://127.0.0.1:5001/threat_logs');
            const logsData = await logsResponse.json();
            console.log('Fetched threat logs:', logsData);
            const cleanedLogs = logsData.map(log => {
              let cleanedWebsite = log.website;
              if (cleanedWebsite.startsWith('http://')) {
                cleanedWebsite = cleanedWebsite.slice(7);
              } else if (cleanedWebsite.startsWith('https://')) {
                cleanedWebsite = cleanedWebsite.slice(8);
              }
              return { ...log, website: cleanedWebsite };
            });
            setThreatLogs(cleanedLogs);
            console.log('Updated threatLogs state:', cleanedLogs);
          } catch (error) {
            setMonitoringStatus('Error');
            setThreatDetected(false);
            setThreatLogs([]);
          }
        }, 5000);
      }

    const handleBeforeUnload = async () => {
      // Removed stop monitoring call on beforeunload to prevent premature stopping
    };
    // Removed beforeunload event listener to prevent premature stopping

    return () => {
      if (interval) clearInterval(interval);
      // Removed stop monitoring call on component unmount to prevent premature stopping
    };
  }, [monitoringStatus]);

  const getStatusColor = (status) => {
    switch (status) {
      case 'Monitoring':
        return green[600];
      case 'Idle':
        return grey[600];
      case 'Starting':
        return blue[600];
      default:
        return grey[600];
    }
  };

  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <AppBar position="static" color="primary" elevation={10} sx={{ mb: 6 }}>
        <Toolbar sx={{ justifyContent: 'center' }}>
          <Typography variant={isMobile ? 'h6' : 'h4'} component="div" sx={{ fontWeight: 'bold', letterSpacing: 6 }}>
            Cyber Threat Detection System
          </Typography>
        </Toolbar>
      </AppBar>
      <Container maxWidth="lg">
        <Grid container spacing={4} justifyContent="center" alignItems="flex-start">
          <Grid item xs={12} md={4}>
            <Paper>
              <Typography variant="h5" gutterBottom sx={{ fontWeight: 'bold', mb: 3, color: '#1976d2' }}>
                Monitor a Website
              </Typography>
              <Box
                component="form"
                onSubmit={(e) => {
                  e.preventDefault();
                  startMonitoring();
                }}
                sx={{
                  display: 'flex',
                  flexDirection: 'column',
                  gap: 2,
                }}
              >
                <TextField
                  label="Website URL"
                  variant="outlined"
                  fullWidth
                  value={website}
                  onChange={(e) => setWebsite(e.target.value)}
                  required
                />
                <Box sx={{ display: 'flex', gap: 2 }}>
                <Button variant="contained" color="secondary" type="submit" sx={{ py: 1.8, flexGrow: 1 }}>
                  Start Monitoring
                </Button>
                <Button
                  variant="outlined"
                  color="error"
                  sx={{ py: 1.8, flexGrow: 1 }}
                  onClick={stopMonitoring}
                >
                  Stop Monitoring
                </Button>
              </Box>
              </Box>
              {message && (
                <Zoom in={Boolean(message)}>
                  <Alert severity="info" sx={{ mt: 3, borderRadius: 2, fontWeight: 'medium' }}>
                    {message}
                  </Alert>
                </Zoom>
              )}
              <Box sx={{ mt: 5, textAlign: 'center' }}>
                <Typography variant="h6" component="span" sx={{ fontWeight: 'medium' }}>
                  Status:
                </Typography>
                <Chip
                  label={monitoringStatus}
                  sx={{
                    ml: 1,
                    bgcolor: threatDetected ? red[700] : getStatusColor(monitoringStatus),
                    color: 'white',
                    fontWeight: 'bold',
                    fontSize: 16,
                    px: 3,
                    py: 0.5,
                    borderRadius: 3,
                    boxShadow: '0 3px 12px rgba(0,0,0,0.3)',
                  }}
                />
                {threatDetected && (
                  <Fade in={threatDetected} timeout={600}>
                    <Alert severity="error" sx={{ mt: 3, borderRadius: 3, fontWeight: 'bold', fontSize: 16, boxShadow: '0 4px 20px rgba(0,0,0,0.3)' }}>
                      Threat Detected on the website!
                    </Alert>
                  </Fade>
                )}
              </Box>
            </Paper>
          </Grid>
          <Grid item xs={12} md={7}>
            <Paper sx={{ height: '100%', display: 'flex', flexDirection: 'column' }}>
              <Typography variant="h5" gutterBottom sx={{ fontWeight: 'bold', mb: 3, color: '#1976d2' }}>
                Threat Detection Log
              </Typography>
              {threatLogs.length === 0 ? (
                <Typography variant="body1" color="text.secondary" align="center" sx={{ fontStyle: 'italic', mt: 2 }}>
                  No threats detected yet.
                </Typography>
              ) : (
                <TableContainer
                  sx={{ flexGrow: 1, overflowY: 'auto', maxHeight: 400 }}
                  ref={(el) => {
                    if (el) {
                      el.scrollTop = el.scrollHeight;
                    }
                  }}
                >
                  <Table stickyHeader aria-label="threat detection log table">
                    <TableHead>
                      <TableRow>
                        <TableCell sx={{ fontWeight: 'bold' }}>Timestamp</TableCell>
                        <TableCell sx={{ fontWeight: 'bold' }}>Website</TableCell>
                        <TableCell sx={{ fontWeight: 'bold' }}>Threat Name</TableCell>
                        <TableCell sx={{ fontWeight: 'bold' }}>Message</TableCell>
                        <TableCell sx={{ fontWeight: 'bold' }}>Solution</TableCell>
                      </TableRow>
                    </TableHead>
                    <TableBody>
                      {threatLogs.map((log) => (
                        <TableRow key={log.id} hover sx={{ '&:hover': { backgroundColor: grey[100] } }}>
                          <TableCell>{log.timestamp}</TableCell>
                          <TableCell>{log.website}</TableCell>
                          <TableCell>{log.threat_name}</TableCell>
                          <TableCell>{log.message}</TableCell>
                          <TableCell>{log.solution}</TableCell>
                        </TableRow>
                      ))}
                    </TableBody>
                  </Table>
                </TableContainer>
              )}
            </Paper>
          </Grid>
        </Grid>
        <Box component="footer" sx={{ mt: 8, py: 3, textAlign: 'center', bgcolor: grey[200], borderRadius: 2 }}>
          <Typography variant="body2" color="text.secondary">
            &copy; {new Date().getFullYear()} Cyber Threat Detection System. All rights reserved.
          </Typography>
        </Box>
      </Container>
    </ThemeProvider>
  );
}

export default App;
