```python
from pydantic import BaseModel, Field, validator
from datetime import date
from typing import Optional
import re

class InspectionFinding(BaseModel):
    """
    Schema for data imported from inspection_findings.csv.
    Ensures data integrity for the triage system input.
    """
    finding_id: str = Field(..., description="Unique identifier in format F-####")
    reported_date: date = Field(..., description="ISO date of the report")
    equipment_id: str = Field(..., description="Foreign key into the equipment registry")
    equipment_type: str = Field(..., description="Denormalised equipment type")
    inspection_type: str = Field(..., description="Type of inspection performed")
    inspection_method: str = Field(..., description="Method used to detect the finding")
    finding_description: str = Field(..., description="Free text observation")
    reported_by: str = Field(..., description="Name of the reporter")
    reporter_role: str = Field(..., description="Job title of the reporter")

    @validator("finding_id")
    def validate_finding_id_format(cls, v):
        if not re.match(r"^F-\d{4}$", v):
            raise ValueError("finding_id must follow the format 'F-####' (e.g., F-1005)")
        return v

    @validator("inspection_type")
    def validate_inspection_type(cls, v):
        valid_types = {
            "Routine Operator Round", 
            "Function Test", 
            "Corrosion Survey", 
            "Statutory Inspection", 
            "Condition Monitoring", 
            "Structural Survey", 
            "Shutdown Inspection"
        }
        if v not in valid_types:
            raise ValueError(f"inspection_type must be one of {valid_types}")
        return v

    @validator("finding_description")
    def validate_description_not_empty(cls, v):
        if not v or len(v.strip()) == 0:
            raise ValueError("finding_description cannot be empty as it is the primary signal for triage")
        return v

# Verification against Knowledge Base requirements:
# 1. finding_id: Validated against 'F-####' pattern.
# 2. reported_date: Uses pydantic 'date' type to enforce ISO date parsing.
# 3. equipment_id: Captured as string for foreign key mapping.
# 4. inspection_type: Strictly validated against the 7 allowed types listed in the scope.
# 5. finding_description: Validated to ensure it contains text, as it is the "Primary signal".
# 6. All other columns (equipment_type, inspection_method, reported_by, reporter_role) are mapped.
```