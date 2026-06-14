from pydantic import BaseModel, Field
from typing import List, Dict, Any

class TransitionRule(BaseModel):
    source_state: str = Field(alias="from")
    target_state: str = Field(alias="to")
    trigger: str

class WorkflowStateMachine(BaseModel):
    states: List[str]
    transitions: List[TransitionRule]

class FormSchemaData(BaseModel):
    type: str = "default"
    id: str
    components: List[Dict[str, Any]] = []

class StudioConfigurationPayload(BaseModel):
    formSchema: FormSchemaData
    workflow: WorkflowStateMachine
    capabilityOwner: str = Field(..., min_length=1)
    sequenceOrder: int = Field(default=1, ge=1)
    fieldPermissions: Dict[str, Dict[str, str]] = {} # { field_id: { STATE: access_level } }
