"""
Tests for studio_node schemas and validation.
"""
import pytest
from pydantic import ValidationError
from studio_node.schemas import (
    StudioConfigurationPayload,
    FormSchemaData,
    WorkflowStateMachine,
    TransitionRule
)


class TestFormSchemaData:
    """Tests for FormSchemaData validation."""
    
    def test_valid_form_schema(self):
        """Test creating a valid form schema."""
        schema = FormSchemaData(
            type="form",
            id="form_1",
            components=[
                {"id": "field_1", "type": "textfield", "label": "Name"}
            ]
        )
        
        assert schema.id == "form_1"
        assert schema.type == "form"
        assert len(schema.components) == 1
    
    def test_form_schema_with_minimal_fields(self):
        """Test form schema with only required fields."""
        schema = FormSchemaData(id="form_1")
        
        assert schema.id == "form_1"
        assert schema.type == "default"
        assert schema.components == []
    
    def test_form_schema_invalid_missing_id(self):
        """Test that form schema requires id field."""
        with pytest.raises(ValidationError):
            FormSchemaData()


class TestTransitionRule:
    """Tests for TransitionRule validation."""
    
    def test_valid_transition_rule(self):
        """Test creating a valid transition rule using aliases."""
        # Use the aliased field names (from/to)
        rule = TransitionRule(
            **{
                "from": "DRAFT",
                "to": "SUBMITTED",
                "trigger": "submit"
            }
        )
        
        assert rule.source_state == "DRAFT"
        assert rule.target_state == "SUBMITTED"
        assert rule.trigger == "submit"


class TestWorkflowStateMachine:
    """Tests for WorkflowStateMachine validation."""
    
    def test_valid_workflow_state_machine(self):
        """Test creating a valid workflow state machine."""
        machine = WorkflowStateMachine(
            states=["DRAFT", "SUBMITTED", "APPROVED"],
            transitions=[
                {"from": "DRAFT", "to": "SUBMITTED", "trigger": "submit"},
                {"from": "SUBMITTED", "to": "APPROVED", "trigger": "approve"}
            ]
        )
        
        assert len(machine.states) == 3
        assert len(machine.transitions) == 2
        assert machine.states[0] == "DRAFT"
    
    def test_workflow_state_machine_empty_transitions(self):
        """Test workflow state machine with no transitions."""
        machine = WorkflowStateMachine(
            states=["DRAFT"],
            transitions=[]
        )
        
        assert len(machine.states) == 1
        assert len(machine.transitions) == 0


class TestStudioConfigurationPayload:
    """Tests for StudioConfigurationPayload validation."""
    
    def test_valid_configuration_payload(self):
        """Test creating a valid configuration payload."""
        payload = StudioConfigurationPayload(
            formSchema=FormSchemaData(
                type="form",
                id="form_1",
                components=[
                    {"id": "field_1", "type": "textfield"}
                ]
            ),
            workflow=WorkflowStateMachine(
                states=["DRAFT", "SUBMITTED"],
                transitions=[
                    {"from": "DRAFT", "to": "SUBMITTED", "trigger": "submit"}
                ]
            ),
            capabilityOwner="admin",
            fieldPermissions={
                "field_1": {
                    "DRAFT": "edit",
                    "SUBMITTED": "view"
                }
            }
        )
        
        assert payload.formSchema.id == "form_1"
        assert len(payload.formSchema.components) == 1
        assert payload.capabilityOwner == "admin"
    
    def test_payload_with_multiple_components(self):
        """Test payload with multiple components."""
        payload = StudioConfigurationPayload(
            formSchema=FormSchemaData(
                type="form",
                id="complex_form",
                components=[
                    {"id": "field_1", "type": "textfield", "label": "Name"},
                    {"id": "field_2", "type": "email", "label": "Email"},
                    {"id": "field_3", "type": "select", "label": "Status"}
                ]
            ),
            workflow=WorkflowStateMachine(
                states=["DRAFT", "SUBMITTED", "APPROVED"],
                transitions=[]
            ),
            capabilityOwner="system",
            fieldPermissions={
                "field_1": {"DRAFT": "edit"},
                "field_2": {"DRAFT": "edit"},
                "field_3": {"DRAFT": "edit"}
            }
        )
        
        assert len(payload.formSchema.components) == 3
        assert len(payload.fieldPermissions) == 3
    
    def test_payload_with_sequence_order(self):
        """Test payload with sequence order."""
        payload = StudioConfigurationPayload(
            formSchema=FormSchemaData(id="form_1"),
            workflow=WorkflowStateMachine(states=["DRAFT"], transitions=[]),
            capabilityOwner="admin",
            sequenceOrder=5
        )
        
        assert payload.sequenceOrder == 5
    
    def test_payload_default_sequence_order(self):
        """Test that sequence order defaults to 1."""
        payload = StudioConfigurationPayload(
            formSchema=FormSchemaData(id="form_1"),
            workflow=WorkflowStateMachine(states=["DRAFT"], transitions=[]),
            capabilityOwner="admin"
        )
        
        assert payload.sequenceOrder == 1
    
    def test_payload_to_dict(self):
        """Test converting payload to dictionary."""
        payload = StudioConfigurationPayload(
            formSchema=FormSchemaData(id="form_1"),
            workflow=WorkflowStateMachine(states=["DRAFT"], transitions=[]),
            capabilityOwner="admin"
        )
        
        payload_dict = payload.model_dump()
        assert isinstance(payload_dict, dict)
        assert "formSchema" in payload_dict
        assert "workflow" in payload_dict
        assert "capabilityOwner" in payload_dict
        assert "fieldPermissions" in payload_dict
