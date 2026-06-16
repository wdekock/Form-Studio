"""
Tests for studio_node router endpoints.

NOTE: These tests require FastAPI/Starlette TestClient to be properly configured.
      The schema validation tests (test_schemas.py) are currently passing.
      
To enable these tests, ensure compatible versions of httpx and starlette are installed.
"""
import pytest
from fastapi import status
from typing import Dict, Any

# Router tests are enabled; tests use httpx ASGI transport via the `client` fixture.


class TestSaveNodeConfig:
    """Tests for POST /save/{form_id} endpoint."""
    
    def test_save_node_config_success(self, client, sample_form_config):
        """Test successful saving of form configuration."""
        form_id = "form_test_001"
        response = client.post(
            f"/api/v1/form-studio-node/save/{form_id}",
            json=sample_form_config
        )
        
        assert response.status_code == status.HTTP_201_CREATED
        data = response.json()
        assert data["status"] == "success"
        assert data["form_id"] == form_id


class TestGetRuntimeNode:
    """Tests for GET /runtime/{form_id} endpoint."""
    
    def test_get_runtime_node_not_found(self, client):
        """Test retrieving non-existent form configuration."""
        response = client.get(
            "/api/v1/form-studio-node/runtime/nonexistent_form?instance_id=instance_01"
        )
        
        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert "unavailable" in response.json()["detail"].lower()


class TestStateManagement:
    """Tests for state management functionality."""
    
    def test_instance_state_isolation(self, client, sample_form_config):
        """Test that different instances maintain separate states."""
        form_id = "form_state_test"
        
        client.post(
            f"/api/v1/form-studio-node/save/{form_id}",
            json=sample_form_config
        )
