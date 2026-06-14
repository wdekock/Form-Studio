import React, { useState, useCallback, useEffect } from 'react';
import PropTypes from 'prop-types';
import { ReactFlow, MiniMap, Controls, Background, useNodesState, useEdgesState, addEdge } from '@xyflow/react';
import { Box, Button, TextField, Paper, Typography } from '@mui/material';
import ButtonEdge from './ButtonEdge';
import '@xyflow/react/dist/style.css';

const initialNodes = [{ id: 'DRAFT', data: { label: 'DRAFT' }, position: { x: 150, y: 150 } }];
const edgeTypes = { customButton: ButtonEdge };

export default function StateCanvasNode({ onWorkflowChanged }) {
  const [nodes, setNodes, onNodesChange] = useNodesState(initialNodes);
  const [edges, setEdges, onEdgesChange] = useEdgesState([]);
  const [newStateName, setNewStateName] = useState('');

  const onConnect = useCallback((params) => {
    setEdges((eds) => addEdge({ ...params, id: `edge-${Date.now()}`, label: 'click to name', type: 'customButton', animated: true }, eds));
  }, [setEdges]);

  useEffect(() => {
    onWorkflowChanged({
      states: nodes.map(n => n.id),
      transitions: edges.map(e => ({ from: e.source, to: e.target, trigger: e.label || '' }))
    });
  }, [nodes, edges, onWorkflowChanged]);

  return (
    <Box sx={{ display: 'flex', flexDirection: 'column', height: '70vh', gap: 2 }}>
      <Paper variant="outlined" sx={{ p: 2, display: 'flex', gap: 2, alignItems: 'center', bgcolor: '#fafafa' }}>
        <TextField label="State Identifier" size="small" value={newStateName} onChange={(e) => setNewStateName(e.target.value)} />
        <Button variant="contained" onClick={() => {
          if (!newStateName) return;
          const cleanId = newStateName.toUpperCase().replace(/\s+/g, '_');
          setNodes((nds) => nds.concat({ id: cleanId, data: { label: cleanId.replace(/_/g, ' ') }, position: { x: 200, y: 200 }, style: { background: '#ffffff', border: '2px solid #1976d2', borderRadius: '6px', padding: '12px 24px', fontWeight: 'bold' } }));
          setNewStateName('');
        }}>Add State</Button>
      </Paper>
      <Box sx={{ flexGrow: 1, border: '1px solid #e0e0e0', borderRadius: 1 }}>
        <ReactFlow nodes={nodes} edges={edges} onNodesChange={onNodesChange} onEdgesChange={onEdgesChange} onConnect={onConnect} edgeTypes={edgeTypes} fitView>
          <Controls /><MiniMap /><Background variant="dots" gap={16} />
        </ReactFlow>
      </Box>
    </Box>
  );
}

StateCanvasNode.propTypes = { onWorkflowChanged: PropTypes.func.isRequired };
