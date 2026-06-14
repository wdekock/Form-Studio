import React, { useState, useEffect, useRef } from 'react';
import { FormViewer } from '@bpmn-io/form-js-viewer';
import { Container, Box, Typography, AppBar, Toolbar, Paper, Tab, Tabs, Button, Alert } from '@mui/material';
import FormStudioNode from '../../studio-ui/src/FormStudioNode';

export default function App() {
  const [activeTab, setActiveTab] = useState(0);
  const [instanceId] = useState("instance_01");
  const [formId] = useState("onboarding_workflow_form");
  const [runtimeSpec, setRuntimeSpec] = useState(null);
  const [userSubmissionData, setUserSubmissionData] = useState({});
  const [alertInfo, setAlertInfo] = useState(null);

  const viewerContainerRef = useRef(null);
  const viewerRef = useRef(null);

  const handleStudioSave = async (compiledBlueprint) => {
    const res = await fetch(`http://127.0.0.1:8000/api/v1/form-studio-node/save/${formId}`, {
      method: 'POST', headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(compiledBlueprint)
    });
    if (res.ok) setAlertInfo({ type: "success", text: "Studio setup written securely to FastAPI." });
  };

  const loadRuntimePayload = async () => {
    const res = await fetch(`http://127.0.0.1:8000/api/v1/form-studio-node/runtime/${formId}?instance_id=${instanceId}`);
    if (res.ok) setRuntimeSpec(await res.json());
  };

  useEffect(() => { if (activeTab === 1) loadRuntimePayload(); }, [activeTab]);

  useEffect(() => {
    if (activeTab !== 1 || !viewerContainerRef.current || !runtimeSpec) return;
    if (viewerRef.current) viewerRef.current.destroy();

    const viewer = new FormViewer({ container: viewerContainerRef.current });
    viewer.importSchema(runtimeSpec, userSubmissionData);
    viewerRef.current = viewer;

    viewer.on('changed', () => { setUserSubmissionData(viewer.getData()); });
  }, [runtimeSpec, activeTab]);

  const handleTriggerTransition = async (triggerWord) => {
    const res = await fetch(`http://127.0.0.1:8000/api/v1/form-studio-node/instance/${instanceId}/submit`, {
      method: 'POST', headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ event_trigger: triggerWord, raw_submission: userSubmissionData })
    });
    const result = await res.json();
    if (res.ok) {
      setAlertInfo({ type: "info", text: `Advanced cleanly to state: ${result.newState}` });
      loadRuntimePayload();
    } else {
      setAlertInfo({ type: "error", text: result.detail });
    }
  };

  return (
    <Box sx={{ minHeight: '100vh', bgcolor: '#f8fafc' }}>
      <AppBar position="static" color="inherit" sx={{ borderBottom: '1px solid #e2e8f0' }} elevation={0}>
        <Toolbar>
          <Typography variant="h6" sx={{ flexGrow: 1, fontWeight: 700 }}>LCAP Platform Workspace</Typography>
          <Tabs value={activeTab} onChange={(e, v) => setActiveTab(v)}>
            <Tab label="Studio Modeler Mode" />
            <Tab label="Live Runtime Simulator" />
          </Tabs>
        </Toolbar>
      </AppBar>

      <Container maxWidth="xl" sx={{ mt: 3 }}>
        {alertInfo && <Alert severity={alertInfo.type} sx={{ mb: 2 }} onClose={() => setAlertInfo(null)}>{alertInfo.text}</Alert>}

        {activeTab === 0 ? (
          <FormStudioNode onSave={handleStudioSave} />
        ) : (
          <Paper sx={{ p: 3 }} variant="outlined">
            <Box display="flex" justifyContent="space-between" alignItems="center" sx={{ mb: 3 }}>
              <Box>
                <Typography variant="h6">Execution Frame</Typography>
                <Typography variant="caption" color="textSecondary">Active Server State Node: <strong>{runtimeSpec?.currentState}</strong></Typography>
              </Box>
              <Box display="flex" gap={1}>
                <Button variant="outlined" color="primary" onClick={() => handleTriggerTransition("submit")}>Trigger 'Submit' Event</Button>
                <Button variant="outlined" color="secondary" onClick={() => handleTriggerTransition("approve")}>Trigger 'Approve' Event</Button>
              </Box>
            </Box>
            <Box ref={viewerContainerRef} className="fjs-container" sx={{ p: 2, bgcolor: '#ffffff', borderRadius: 1, border: '1px solid #e2e8f0' }} />
          </Paper>
        )}
      </Container>
    </Box>
  );
}
