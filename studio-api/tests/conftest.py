"""
Pytest configuration and shared fixtures for backend tests.
"""
import pytest
from typing import Dict, Any
import sys
from pathlib import Path
import subprocess
import time
import os
import signal
import urllib.request
import urllib.error
import json

# Add studio-api to path
sys.path.insert(0, str(Path(__file__).parent.parent))


class APIClient:
    def __init__(self, base_url: str):
        self.base = base_url.rstrip("/")

    def post(self, path: str, **kwargs):
        url = f"{self.base}{path}"
        data = None
        hdrs = kwargs.get("headers", {}) or {}
        json_payload = kwargs.get("json") if "json" in kwargs else kwargs.get("json_data")
        if json_payload is not None:
            data = json.dumps(json_payload).encode("utf-8")
            hdrs["Content-Type"] = "application/json"
        elif "data" in kwargs and kwargs.get("data") is not None:
            data = kwargs.get("data")
            if isinstance(data, str):
                data = data.encode("utf-8")
        req = urllib.request.Request(url, data=data, headers=hdrs, method="POST")
        try:
            with urllib.request.urlopen(req) as resp:
                body = resp.read()
                return SimpleResponse(resp.getcode(), body)
        except urllib.error.HTTPError as e:
            return SimpleResponse(e.code, e.read())

    def get(self, path: str, headers=None):
        url = f"{self.base}{path}"
        hdrs = headers or {}
        req = urllib.request.Request(url, headers=hdrs, method="GET")
        try:
            with urllib.request.urlopen(req) as resp:
                body = resp.read()
                return SimpleResponse(resp.getcode(), body)
        except urllib.error.HTTPError as e:
            return SimpleResponse(e.code, e.read())


class SimpleResponse:
    def __init__(self, status_code: int, content: bytes):
        self.status_code = status_code
        self._content = content

    def json(self):
        try:
            return json.loads(self._content.decode("utf-8"))
        except Exception:
            return None

    def text(self):
        return self._content.decode("utf-8")


@pytest.fixture
def client():
    """Start uvicorn in a subprocess and provide a simple requests-based client.

    This avoids httpx/ASGI transport compatibility issues by running the app
    in a real HTTP server for tests.
    """
    project_dir = Path(__file__).parent.parent
    port = 8001
    env = os.environ.copy()

    proc = subprocess.Popen(
        [sys.executable, "-m", "uvicorn", "main:app", "--host", "127.0.0.1", "--port", str(port)],
        cwd=str(project_dir),
        env=env,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )

    base_url = f"http://127.0.0.1:{port}"

    # Wait for server to be ready (use urllib to avoid requests dependency)
    timeout = 10
    start = time.time()
    while True:
        try:
            urllib.request.urlopen(base_url)
            break
        except urllib.error.HTTPError:
            # HTTPError means server responded (e.g., 404) -> ready
            break
        except Exception:
            if time.time() - start > timeout:
                proc.kill()
                raise RuntimeError("uvicorn failed to start within timeout")
            time.sleep(0.1)

    client = APIClient(base_url)
    try:
        yield client
    finally:
        try:
            proc.terminate()
            proc.wait(timeout=5)
        except Exception:
            proc.kill()


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
