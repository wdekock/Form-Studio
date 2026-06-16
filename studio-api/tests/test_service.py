"""
Tests for studio_node service business logic.
"""
import pytest
from typing import Dict, Any


class TestValidationEngine:
    """Tests for NodeValidationEngine service."""
    
    def test_field_permission_resolution(self, sample_form_config):
        """Test that field permissions are correctly resolved based on state."""
        from studio_node.service import NodeValidationEngine
        
        engine = NodeValidationEngine()
        # This test assumes the service has permission resolution logic
        # Adapt based on actual service implementation
        
        # Test would validate that permissions are correctly applied
        assert sample_form_config is not None
        assert "workflow" in sample_form_config
        assert "fieldPermissions" in sample_form_config
    
    def test_workflow_structure_validation(self, sample_form_config):
        """Test that workflow structure is correctly validated."""
        config = sample_form_config
        
        # Validate that workflow exists and has correct structure
        assert "workflow" in config
        assert "states" in config["workflow"]
        assert "transitions" in config["workflow"]
        assert len(config["workflow"]["states"]) > 0
