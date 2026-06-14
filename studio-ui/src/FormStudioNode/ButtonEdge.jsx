import React from 'react';
import { BaseEdge, EdgeLabelRenderer, getSmoothStepPath, useReactFlow } from '@xyflow/react';
import { IconButton, TextField, Box } from '@mui/material';
import DeleteIcon from '@mui/icons-material/Delete';

export default function ButtonEdge({ id, sourceX, sourceY, targetX, targetY, sourcePosition, targetPosition, style = {}, markerEnd, label }) {
  const { setEdges } = useReactFlow();
  const [edgePath, labelX, labelY] = getSmoothStepPath({ sourceX, sourceY, sourcePosition, targetPosition, targetX, targetY });

  return (
    <>
      <BaseEdge path={edgePath} markerEnd={markerEnd} style={{ ...style, strokeWidth: 2.5 }} />
      <EdgeLabelRenderer>
        <Box style={{ position: 'absolute', transform: `translate(-50%, -50%) translate(${labelX}px,${labelY}px)`, fontSize: 12, pointerEvents: 'all', backgroundColor: '#ffffff', padding: '4px', borderRadius: '4px', boxShadow: '0px 2px 4px rgba(0,0,0,0.1)', display: 'flex', alignItems: 'center', gap: '4px', zIndex: 1000 }} className="nodrag nopan">
          <TextField
            variant="standard"
            size="small"
            value={label === 'click to name' ? '' : label}
            onChange={(e) => setEdges((eds) => eds.map((edge) => edge.id === id ? { ...edge, label: e.target.value.toLowerCase() } : edge))}
            placeholder="trigger event"
            inputProps={{ style: { fontSize: '0.75rem', padding: '2px' } }}
            sx={{ width: 90 }}
          />
          <IconButton size="small" color="error" onClick={(e) => { e.stopPropagation(); setEdges((eds) => eds.filter((edge) => edge.id !== id)); }}>
            <DeleteIcon fontSize="inherit" />
          </IconButton>
        </Box>
      </EdgeLabelRenderer>
    </>
  );
}
