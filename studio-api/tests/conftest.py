"""
Pytest configuration and shared fixtures for backend tests.
"""
import pytest
from typing import Dict, Any
import sys
from pathlib import Path
from starlette.testclient import TestClient

# Add studio-api to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from main import app


@pytest.fixture
def client():
    """FastAPI test client fixture."""
    return TestClient(app)


@pytest.fixture
def sample_form_config() -> Dict[str, Any]:
    """Sample form configuration payload for testing."""
    return {
        "formSchema": {
            "type": "form",
            "id": "test_form_001",
            "components": [
                {
                    "id": "field_name",
                    "type": "textfield",
                    "label": "Full Name",
                    "placeholder": "Enter your name"
                },
                {
                    "id": "field_email",
                    "type": "email",
                    "label": "Email Address",
                    "placeholder": "Enter your email"
                },
                {
                    "id": "field_status",
                    "type": "select",
                    "label": "Status",
                    "options": ["DRAFT", "SUBMITTED", "APPROVED"]
                }
            ]
        },
        "workflow": {
            "states": ["DRAFT", "SUBMITTED", "APPROVED"],
            "transitions": [
                {"from": "DRAFT", "to": "SUBMITTED", "trigger": "submit"},
                {"from": "SUBMITTED", "to": "APPROVED", "trigger": "approve"}
            ]
        },
        "capabilityOwner": "test_owner",
        "sequenceOrder": 1,
        "fieldPermissions": {
            "field_name": {
                "DRAFT": "edit",
                "SUBMITTED": "view",
                "APPROVED": "view"
            },
            "field_email": {
                "DRAFT": "edit",
                "SUBMITTED": "edit",
                "APPROVED": "view"
            },
            "field_status": {
                "DRAFT": "edit",
                "SUBMITTED": "view",
                "APPROVED": "view"
            }
        }
    }


@pytest.fixture
def sample_instance_data() -> Dict[str, Any]:
    """Sample instance data for testing."""
    return {
        "instance_id": "instance_test_001",
        "current_state": "DRAFT",
        "data": {
            "field_name": "John Doe",
            "field_email": "john@example.com",
            "field_status": "DRAFT"
        }
    }


@pytest.fixture(autouse=True)
def reset_datastore():
    """Reset in-memory datastore before each test."""
    from studio_node.router import DATABANK, INSTANCE_STATES, INSTANCE_DATA_STORE
    
    DATABANK.clear()
    INSTANCE_STATES.clear()
    INSTANCE_DATA_STORE.clear()
    
    # Add default test instance
    INSTANCE_STATES["instance_01"] = "DRAFT"
    INSTANCE_DATA_STORE["instance_01"] = {}
    
    yield
    
    # Cleanup after test
    DATABANK.clear()
    INSTANCE_STATES.clear()
    INSTANCE_DATA_STORE.clear()


@pytest.fixture
def sample_form_config() -> Dict[str, Any]:
    """Sample form configuration payload for testing."""
    return {
        "formSchema": {
            "type": "form",
            "id": "test_form_001",
            "components": [
                {
                    "id": "field_name",
                    "type": "textfield",
                    "label": "Full Name",
                    "placeholder": "Enter your name"
                },
                {
                    "id": "field_email",
                    "type": "email",
                    "label": "Email Address",
                    "placeholder": "Enter your email"
                },
                {
                    "id": "field_status",
                    "type": "select",
                    "label": "Status",
                    "options": ["DRAFT", "SUBMITTED", "APPROVED"]
                }
            ]
        },
        "workflow": {
            "states": ["DRAFT", "SUBMITTED", "APPROVED"],
            "transitions": [
                {"from": "DRAFT", "to": "SUBMITTED", "trigger": "submit"},
                {"from": "SUBMITTED", "to": "APPROVED", "trigger": "approve"}
            ]
        },
        "capabilityOwner": "test_owner",
        "sequenceOrder": 1,
        "fieldPermissions": {
            "field_name": {
                "DRAFT": "edit",
                "SUBMITTED": "view",
                "APPROVED": "view"
            },
            "field_email": {
                "DRAFT": "edit",
                "SUBMITTED": "edit",
                "APPROVED": "view"
            },
            "field_status": {
                "DRAFT": "edit",
                "SUBMITTED": "view",
                "APPROVED": "view"
            }
        }
    }


@pytest.fixture
def sample_instance_data() -> Dict[str, Any]:
    """Sample instance data for testing."""
    return {
        "instance_id": "instance_test_001",
        "current_state": "DRAFT",
        "data": {
            "field_name": "John Doe",
            "field_email": "john@example.com",
            "field_status": "DRAFT"
        }
    }


@pytest.fixture(autouse=True)
def reset_datastore():
    """Reset in-memory datastore before each test."""
    from studio_node.router import DATABANK, INSTANCE_STATES, INSTANCE_DATA_STORE
    
    DATABANK.clear()
    INSTANCE_STATES.clear()
    INSTANCE_DATA_STORE.clear()
    
    # Add default test instance
    INSTANCE_STATES["instance_01"] = "DRAFT"
    INSTANCE_DATA_STORE["instance_01"] = {}
    
    yield
    
    # Cleanup after test
    DATABANK.clear()
    INSTANCE_STATES.clear()
    INSTANCE_DATA_STORE.clear()
