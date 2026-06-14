import React, { useEffect, useRef, useState } from 'react';
import PropTypes from 'prop-types';
import { Grid, Box, Paper, Button, Tabs, Tab, Card } from '@mui/material';
import { FormEditor } from '@bpmn-io/form-js-editor';
import StateCanvasNode from './StateCanvasNode';
import MatrixPanel from './MatrixPanel';
import '@bpmn-io/form-js/dist/assets/form-js.css';
import '@bpmn-io/form-js/dist/assets/form-js-editor.css';

export default function FormStudioNode({ onSave }) {
  const [currentTab, setCurrentTab] = useState(0);
  const containerRef = useRef(null);
  const editorRef = useRef(null);

  const [formSchema, setFormSchema] = useState({ type: 'default', components: [] });
  const [workflow, setWorkflow] = useState({ states: ['DRAFT'], transitions: [] });
  const [metadata, setMetadata] = useState({ capabilityOwner: 'Admin', sequenceOrder: 1 });
  const [permissions, setPermissions] = useState({});

  useEffect(() => {
    if (currentTab !== 0 || !containerRef.current) return;
    const editor = new FormEditor({ container: containerRef.current });
    editor.importSchema(formSchema);
    editorRef.current = editor;

    editor.on('changed', () => {
      const freshSchema = editor.getSchema();
      setFormSchema(freshSchema);
      
      // 🔄 Proactive Sync: Clean up matrix keys when items vanish from layout canvas
      const validIds = new Set(freshSchema.components.map(c => c.id));
      setPermissions(prev => {
        const structuralCopy = { ...prev };
        Object.keys(structuralCopy).forEach(key => { if(!validIds.has(key)) delete structuralCopy[key]; });
        return structuralCopy;
      });
    });

    return () => editor.destroy();
  }, [currentTab]);

  return (
    <Card sx={{ p: 2 }}>
      <Box display="flex" justifyContent="space-between" sx={{ borderBottom: 1, borderColor: 'divider', mb: 2 }}>
        <Tabs value={currentTab} onChange={(e, v) => setCurrentTab(v)}>
          <Tab label="1. Form Canvas" />
          <Tab label="2. Workflow States" />
          <Tab label="3. Matrix Configuration" />
        </Tabs>
        <Button variant="contained" onClick={() => onSave({ formSchema, workflow, ...metadata, fieldPermissions: permissions })} color="success">Commit Schema Configuration</Button>
      </Box>

      {currentTab === 0 && (
        <Paper variant="outlined" sx={{ p: 1, height: '70vh' }}>
          <Box ref={containerRef} className="fjs-container" sx={{ height: '100%', overflow: 'auto' }} />
        </Paper>
      )}
      {currentTab === 1 && <StateCanvasNode onWorkflowChanged={(flow) => setWorkflow(flow)} />}
      {currentTab === 2 && (
        <MatrixPanel
          formFields={formSchema.components.map(c => ({ id: c.id, label: c.label || c.id }))}
          processTasks={workflow.states}
          metadata={metadata}
          permissions={permissions}
          onMetadataChange={(k, v) => setMetadata(p => ({ ...p, [k]: v }))}
          onPermissionChange={(fid, tid, val) => setPermissions(p => ({ ...p, [fid]: { ...(p[fid] || {}), [tid]: val } }))}
        />
      )}
    </Card>
  );
}

FormStudioNode.propTypes = { onSave: PropTypes.func.isRequired };
