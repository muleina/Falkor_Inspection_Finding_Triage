```python
from __future__ import annotations

import re
from datetime import date
from typing import Literal

from pydantic import BaseModel, Field, validator


class InspectionFinding(BaseModel):
    """
    Pydantic schema representing a row from ``data/inspection_findings.csv``.
    All fields are required and validated against the constraints
    described in the project brief.
    """

    finding_id: str = Field(
        ...,
        description="Unique identifier, format ``F-####`` where #### is a four‑digit number.",
        examples=["F-1005"],
    )
    reported_date: date = Field(
        ...,
        description="Date the finding was reported, ISO‑8601 (YYYY‑MM‑DD).",
        examples=["2023-07-15"],
    )
    equipment_id: str = Field(
        ...,
        description="Foreign key to the equipment registry.",
        examples=["FG-0455"],
    )
    equipment_type: str = Field(
        ...,
        min_length=1,
        description="Denormalised equipment type from the registry.",
    )
    inspection_type: Literal[
        "Routine Operator Round",
        "Function Test",
        "Corrosion Survey",
        "Statutory Inspection",
        "Condition Monitoring",
        "Structural Survey",
        "Shutdown Inspection",
    ] = Field(
        ...,
        description="Category of the inspection that generated the finding.",
    )
    inspection_method: str = Field(
        ...,
        min_length=1,
        description="Method used to detect the finding (e.g., visual, ultrasonic).",
    )
    finding_description: str = Field(
        ...,
        min_length=1,
        description="Free‑text description written by the reporter.",
    )
    reported_by: str = Field(
        ...,
        min_length=1,
        description="Name of the person who reported the finding.",
    )
    reporter_role: str = Field(
        ...,
        min_length=1,
        description="Job title of the reporter.",
    )

    # --------------------------------------------------------------------- #
    # Validators – enforce deterministic, machine‑checkable rules
    # --------------------------------------------------------------------- #

    @validator("finding_id")
    def check_finding_id(cls, v: str) -> str:
        """
        Must match the pattern ``F-####`` where ``####`` is exactly four digits.
        """
        if not re.fullmatch(r"F-\d{4}", v):
            raise ValueError("finding_id must be in the form 'F-####' (four digits).")
        return v

    @validator("equipment_id")
    def check_equipment_id(cls, v: str) -> str:
        """
        The brief does not prescribe a strict pattern; we only require a non‑empty
        alphanumeric string (allowing hyphens/underscores).
        """
        if not re.fullmatch(r"[A-Za-z0-9_-]+", v):
            raise ValueError("equipment_id must be alphanumeric (hyphens/underscores allowed).")
        return v

    @validator("inspection_method")
    def method_not_blank(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("inspection_method cannot be blank.")
        return v

    @validator("finding_description")
    def description_not_blank(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("finding_description cannot be blank.")
        return v

    @validator("reported_by")
    def reporter_name_not_blank(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("reported_by cannot be blank.")
        return v

    @validator("reporter_role")
    def reporter_role_not_blank(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("reporter_role cannot be blank.")
        return v

    @validator("equipment_type")
    def equipment_type_not_blank(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("equipment_type cannot be blank.")
        return v
```