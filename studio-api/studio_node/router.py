from fastapi import APIRouter, HTTPException, status, Body, Depends
from .schemas import StudioConfigurationPayload
from .service import NodeValidationEngine
from typing import Dict, Any

studio_router = APIRouter(prefix="/form-studio-node", tags=["Form Studio Node API"])

# Global In-Memory Storage Blocks (Acting as DB Repositories)
DATABANK: Dict[str, Any] = {}
INSTANCE_STATES: Dict[str, str] = {"instance_01": "DRAFT"}
INSTANCE_DATA_STORE: Dict[str, Dict[str, Any]] = {"instance_01": {}}

@studio_router.post("/save/{form_id}", status_code=status.HTTP_201_CREATED)
async def save_node_config(form_id: str, payload: StudioConfigurationPayload):
    try:
        DATABANK[form_id] = payload.model_dump()
        return {"status": "success", "form_id": form_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@studio_router.get("/runtime/{form_id}")
async def get_runtime_node(form_id: str, instance_id: str):
    config = DATABANK.get(form_id)
    if not config:
        raise HTTPException(status_code=404, detail="Configuration profile unavailable.")

    # 🔒 Server-Side State Resolution (Never trust client context parameters)
    current_state = INSTANCE_STATES.get(instance_id, "DRAFT")
    raw_components = config["formSchema"]["components"]
    permissions = config["fieldPermissions"]
    
    processed_components = []
    for comp in raw_components:
        comp_id = comp.get("id")
        state_rule = permissions.get(comp_id, {}).get(current_state, "edit")

        if state_rule == "hide":
            continue  # Stripped securely at endpoint boundary layer
        elif state_rule == "view":
            comp["disabled"] = True
        elif state_rule == "edit":
            comp["disabled"] = False

        processed_components.append(comp)

    return {
        "type": config["formSchema"]["type"],
        "id": config["formSchema"]["id"],
        "currentState": current_state,
        "components": processed_components,
        "capabilityOwner": config["capabilityOwner"],
        "sequenceOrder": config["sequenceOrder"]
    }

@studio_router.post("/instance/{instance_id}/submit")
async def execute_task_submission(
    instance_id: str,
    form_id: str,
    event_trigger: str = Body(..., embed=True),
    raw_submission: Dict[str, Any] = Body(..., embed=True)
):
    config = DATABANK.get(form_id)
    if not config:
        raise HTTPException(status_code=404, detail="Studio config blueprint profile missing.")

    current_state = INSTANCE_STATES.get(instance_id, "DRAFT")
    transitions = config["workflow"]["transitions"]

    # Evaluate Inbound State Machine Routing Mechanics
    destination_state = None
    for route in transitions:
        if route["source_state"] == current_state and route["trigger"] == event_trigger.lower():
            destination_state = route["target_state"]
            break

    if not destination_state:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid Transition: Trigger event '{event_trigger}' is illegal out of state '{current_state}'."
        )

    # Clean, validate, and extract raw input parameters using rule engines
    historical_snapshot = INSTANCE_DATA_STORE.get(instance_id, {})
    sanitized_document = NodeValidationEngine.validate_submission_against_state(
        current_state=current_state,
        submitted_data=raw_submission,
        historical_data=historical_snapshot,
        matrix_rules=config["fieldPermissions"],
        form_components=config["formSchema"]["components"]
    )

    # Persist and advance state token registers cleanly
    INSTANCE_DATA_STORE[instance_id] = sanitized_document
    INSTANCE_STATES[instance_id] = destination_state

    return {
        "status": "advanced",
        "newState": destination_state,
        "saved_document": sanitized_document
    }
