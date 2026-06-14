from fastapi import HTTPException, status
from typing import Dict, Any, List

class NodeValidationEngine:
    @staticmethod
    def validate_submission_against_state(
        current_state: str,
        submitted_data: Dict[str, Any],
        historical_data: Dict[str, Any],
        matrix_rules: Dict[str, Dict[str, str]],
        form_components: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        Validates an abstract unstructured JSON data payload based strictly on the 
        active process state configuration rules.
        """
        validated_payload = {}
        blueprint_fields = {comp["id"]: comp for comp in form_components}

        for field_id, field_meta in blueprint_fields.items():
            rule = matrix_rules.get(field_id, {}).get(current_state, "edit")
            new_value = submitted_data.get(field_id)
            old_value = historical_data.get(field_id)

            if rule == "hide":
                if new_value is not None:
                    raise HTTPException(
                        status_code=status.HTTP_403_FORBIDDEN,
                        detail=f"Security Violation: Modification of hidden field '{field_id}' blocked."
                    )
                validated_payload[field_id] = old_value  # Preserve history safely

            elif rule == "view":
                if new_value != old_value:
                    raise HTTPException(
                        status_code=status.HTTP_403_FORBIDDEN,
                        detail=f"Security Violation: Read-only field breach at element '{field_id}'."
                    )
                validated_payload[field_id] = old_value

            elif rule == "edit":
                if field_meta.get("required") and new_value is None:
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail=f"Validation Failure: Mandatory field '{field_id}' missing."
                    )
                validated_payload[field_id] = new_value

        return validated_payload
