```python
from __future__ import annotations

import re
from typing import Optional

from pydantic import BaseModel, Field, validator


class EquipmentRegistryEntry(BaseModel):
    """
    Pydantic model representing a single row from equipment_registry.csv.
    """

    equipment_id: str = Field(
        ...,
        description="Primary key, e.g., FG-0455",
    )
    equipment_type: str = Field(
        ...,
        description="Descriptive type of the equipment",
    )
    service_description: str = Field(
        ...,
        description="Descriptive service description",
    )
    criticality_score: int = Field(
        ...,
        description="1–10, 10 = most critical",
    )
    reliability_score: int = Field(
        ...,
        description="1–10, 10 = highly reliable (opposite direction to likelihood)",
    )
    safety_critical_element: str = Field(
        ...,
        description='Yes or No',
    )
    redundancy: str = Field(
        ...,
        description="Redundancy description",
    )
    engineer_comment: Optional[str] = Field(
        None,
        description="Unstructured notes about the specific item",
    )

    @validator("equipment_id")
    def _validate_equipment_id(cls, v: str) -> str:
        if not v or not isinstance(v, str):
            raise ValueError("equipment_id must be a non‑empty string")
        # Expected pattern: two uppercase letters, a dash, and four digits
        if not re.match(r"^[A-Z]{2}-\d{4}$", v):
            raise ValueError("equipment_id must match pattern XX-0000")
        return v

    @validator("equipment_type", "service_description")
    def _validate_non_empty_str(cls, v: str, field) -> str:
        if not v or not isinstance(v, str) or not v.strip():
            raise ValueError(f"{field.name} must be a non‑empty string")
        return v

    @validator("criticality_score", "reliability_score")
    def _validate_score(cls, v: int, field) -> int:
        if not isinstance(v, int) or not (1 <= v <= 10):
            raise ValueError(f"{field.name} must be an integer between 1 and 10")
        return v

    @validator("safety_critical_element")
    def _validate_safety_critical_element(cls, v: str) -> str:
        if v not in {"Yes", "No"}:
            raise ValueError('safety_critical_element must be "Yes" or "No"')
        return v

    @validator("redundancy")
    def _validate_redundancy(cls, v: str) -> str:
        allowed = {
            "None",
            "N+1 (TAG)",
            "Voted 2oo3",
            "Duplicated (TAG)",
            "Yes (bypass available)",
        }
        if v not in allowed:
            raise ValueError(
                f"redundancy must be one of {sorted(allowed)}"
            )
        return v

    @validator("engineer_comment", always=True)
    def _validate_engineer_comment(cls, v: Optional[str]) -> Optional[str]:
        if v is not None and not isinstance(v, str):
            raise ValueError("engineer_comment must be a string if provided")
        return v

    class Config:
        orm_mode = True
```