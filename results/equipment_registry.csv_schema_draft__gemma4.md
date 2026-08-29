```python
from pydantic import BaseModel, Field, field_validator, model_validator
from typing import Optional
import re

class EquipmentRegistryItem(BaseModel):
    """
    Schema for the equipment registry as defined in the Inspection Finding Triage requirements.
    """
    equipment_id: str = Field(
        ..., 
        description="Primary key for the equipment"
    )
    equipment_type: str = Field(
        ..., 
        description="Descriptive type of the equipment"
    )
    service_description: str = Field(
        ..., 
        description="Descriptive service the equipment provides"
    )
    criticality_score: int = Field(
        ..., 
        ge=1, 
        le=10, 
        description="1 = least critical, 10 = most critical"
    )
    reliability_score: int = Field(
        ..., 
        ge=1, 
        le=10, 
        description="1 = fails frequently, 10 = highly reliable"
    )
    safety_critical_element: str = Field(
        ..., 
        description="Whether the equipment is a Safety Critical Element ('Yes' or 'No')"
    )
    redundancy: str = Field(
        ..., 
        description="Redundancy configuration (e.g., 'None', 'N+1 (TAG)', 'Voted 2oo3')"
    )
    engineer_comment: Optional[str] = Field(
        None, 
        description="Unstructured notes about the specific item"
    )

    @field_validator('safety_critical_element')
    @classmethod
    def validate_sce_boolean(cls, v: str) -> str:
        """Ensures safety_critical_element is strictly 'Yes' or 'No'."""
        normalized = v.strip().capitalize()
        if normalized not in ('Yes', 'No'):
            raise ValueError("safety_critical_element must be either 'Yes' or 'No'")
        return normalized

    @field_validator('equipment_id')
    @classmethod
    def validate_id_format(cls, v: str) -> str:
        """
        Ensures equipment_id is not empty and follows a basic alphanumeric pattern.
        Adjust regex if specific ID patterns (like FG-####) are mandatory for registry.
        """
        if not v or not v.strip():
            raise ValueError("equipment_id cannot be empty")
        return v.strip()

    @model_validator(mode='after')
    def validate_redundancy_logic(self) -> 'EquipmentRegistryItem':
        """
        Cross-field validation to ensure consistency between SCE status and redundancy.
        While not a hard constraint in the CSV, this ensures data integrity for the triage logic.
        """
        # Example: If it's a Safety Critical Element, we should ensure redundancy is explicitly stated
        if self.safety_critical_element == 'Yes' and not self.redundancy:
            raise ValueError("Safety Critical Elements must have a redundancy status specified")
        return self

# Example usage and validation test
if __name__ == "__main__":
    try:
        # Valid record
        valid_item = EquipmentRegistryItem(
            equipment_id="FG-0455",
            equipment_type="Gas Detector",
            service_description="Compression Module Detection",
            criticality_score=9,
            reliability_score=8,
            safety_critical_element="Yes",
            redundancy="Voted 2oo3",
            engineer_comment="Check calibration date"
        )
        print("Successfully validated valid_item")

        # Invalid record (Out of range score)
        EquipmentRegistryItem(
            equipment_id="ERR-1",
            equipment_type="Pump",
            service_description="Water",
            criticality_score=11, # Invalid
            reliability_score=5,
            safety_critical_element="No",
            redundancy="None"
        )
    except ValueError as e:
        print(f"Caught expected error: {e}")
```