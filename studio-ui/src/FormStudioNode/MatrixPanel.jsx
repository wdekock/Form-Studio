import React from 'react';
import PropTypes from 'prop-types';
import { Box, Paper, Typography, TextField, Divider, Table, Button, TableBody, TableCell, TableContainer, TableHead, TableRow, MenuItem, Select, ButtonGroup } from '@mui/material';

export default function MatrixPanel({ formFields, processTasks, metadata, permissions, onMetadataChange, onPermissionChange }) {
  return (
    <Paper sx={{ p: 3, height: '75vh', overflowY: 'auto' }} variant="outlined">
      <Typography variant="h6" sx={{ fontWeight: 600 }}>State Visibility Matrix</Typography>
      <Divider sx={{ my: 2 }} />
      <Box display="flex" flexDirection="column" gap={2} sx={{ mb: 4 }}>
        <TextField label="Capability Owner" size="small" value={metadata.capabilityOwner} onChange={(e) => onMetadataChange('capabilityOwner', e.target.value)} />
        <TextField label="Sequence Order" type="number" size="small" value={metadata.sequenceOrder} onChange={(e) => onMetadataChange('sequenceOrder', parseInt(e.target.value, 10) || 1)} />
      </Box>
      <TableContainer component={Paper} variant="outlined">
        <Table size="small">
          <TableHead>
            <TableRow>
              <TableCell><strong>Field (ID)</strong></TableCell>
              {processTasks.map(t => <TableCell key={t} align="center"><strong>{t}</strong></TableCell>)}
            </TableRow>
            <TableRow>
              <TableCell sx={{ bgcolor: '#f1f5f9', fontSize: '0.75rem' }}>Bulk Column Action:</TableCell>
              {processTasks.map(t => (
                <TableCell key={t} align="center" sx={{ bgcolor: '#f1f5f9', py: 0.5 }}>
                  <ButtonGroup size="small" variant="text">
                    <Button onClick={() => formFields.forEach(f => onPermissionChange(f.id, t, 'edit'))}>Edit</Button>
                    <Button onClick={() => formFields.forEach(f => onPermissionChange(f.id, t, 'view'))}>Read</Button>
                    <Button onClick={() => formFields.forEach(f => onPermissionChange(f.id, t, 'hide'))}>Hide</Button>
                  </ButtonGroup>
                </TableCell>
              ))}
            </TableRow>
          </TableHead>
          <TableBody>
            {formFields.map(field => (
              <TableRow key={field.id} hover>
                <TableCell>{field.label}</TableCell>
                {processTasks.map(task => (
                  <TableCell key={task} align="center">
                    <Select value={permissions[field.id]?.[task] || 'edit'} onChange={(e) => onPermissionChange(field.id, task, e.target.value)} size="small" sx={{ fontSize: '0.75rem' }}>
                      <MenuItem value="edit">Edit</MenuItem>
                      <MenuItem value="view">View Only</MenuItem>
                      <MenuItem value="hide">Hidden</MenuItem>
                    </Select>
                  </TableCell>
                ))}
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </TableContainer>
    </Paper>
  );
}

MatrixPanel.propTypes = { formFields: PropTypes.array.isRequired, processTasks: PropTypes.array.isRequired, metadata: PropTypes.object.isRequired, permissions: PropTypes.object.isRequired, onMetadataChange: PropTypes.func.isRequired, onPermissionChange: PropTypes.func.isRequired };
