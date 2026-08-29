Below is a production‑ready Pydantic model that mirrors the columns of **`equipment_registry.csv`**.  Each field is typed according to the source description, and validators enforce the constraints expressed in the knowledge base (score ranges, allowed values, and the “Yes/No” boolean conversion).  The model is deliberately strict – unknown fields raise an error – so it can be used directly when loading the CSV rows.

```python
from __future__ import annotations

from typing import Literal, Optional

from pydantic import BaseModel, Field, validator, root_validator


class EquipmentRegistryItem(BaseModel):
    """
    Representation of a single row from `equipment_registry.csv`.

    Attributes
    ----------
    equipment_id: str
        Primary key; any non‑empty string is accepted (uniqueness must be
        enforced by the caller when loading the full file).

    equipment_type: str
        Human‑readable type description; stripped of surrounding whitespace.

    service_description: str
        Free‑form description of the service performed by the equipment.

    criticality_score: int
        Integer 1‑10 (inclusive).  Higher values indicate higher criticality.

    reliability_score: int
        Integer 1‑10 (inclusive).  Higher values indicate higher reliability.
        The score runs opposite to “likelihood of failure”, but the model only
        validates the numeric range.

    safety_critical_element: bool
        Original CSV stores “Yes” / “No”.  The validator normalises any
        case‑insensitive variant to a boolean.

    redundancy: Literal[
        "None",
        "N+1 (TAG)",
        "Voted 2oo3",
        "Duplicated (TAG)",
        "Yes (bypass available)",
    ]
        Allowed redundancy descriptors as listed in the domain knowledge.

    engineer_comment: Optional[str] = None
        Optional free‑text notes; may be omitted or empty.
    """

    equipment_id: str = Field(..., description="Primary key for the equipment")
    equipment_type: str = Field(..., description="Descriptive equipment type")
    service_description: str = Field(..., description="Service description")
    criticality_score: int = Field(
        ...,
        ge=1,
        le=10,
        description="Criticality score (1 = least critical, 10 = most critical)",
    )
    reliability_score: int = Field(
        ...,
        ge=1,
        le=10,
        description="Reliability score (1 = frequently fails, 10 = highly reliable)",
    )
    safety_critical_element: bool = Field(
        ...,
        description="True if the equipment is a Safety Critical Element (SCE)",
    )
    redundancy: Literal[
        "None",
        "N+1 (TAG)",
        "Voted 2oo3",
        "Duplicated (TAG)",
        "Yes (bypass available)",
    ] = Field(..., description="Redundancy configuration")
    engineer_comment: Optional[str] = Field(
        None, description="Unstructured notes from the engineer"
    )

    @validator("equipment_id")
    def _equipment_id_must_not_be_blank(cls, v: str) -> str:
        v = v.strip()
        if not v:
            raise ValueError("equipment_id cannot be blank")
        return v

    @validator("equipment_type", "service_description", pre=True, always=True)
    def _strip_strings(cls, v: str) -> str:
        return v.strip()

    @validator("safety_critical_element", pre=True)
    def _parse_yes_no(cls, v: str | bool) -> bool:
        """
        Accepts a case‑insensitive “Yes” / “No” string or a native boolean.
        Anything else is rejected.
        """
        if isinstance(v, bool):
            return v
        val = str(v).strip().lower()
        if val == "yes":
            return True
        if val == "no":
            return False
        raise ValueError("safety_critical_element must be 'Yes' or 'No' (case‑insensitive)")

    @validator("redundancy")
    def _validate_redundancy(cls, v: str) -> str:
        """
        The CSV free‑text field is limited to the five values that appear in the
        domain knowledge.  The validator guarantees exact matching (including
        spacing and case) to avoid silent typos.
        """
        allowed = {
            "None",
            "N+1 (TAG)",
            "Voted 2oo3",
            "Duplicated (TAG)",
            "Yes (bypass available)",
        }
        if v not in allowed:
            raise ValueError(f"redundancy must be one of {sorted(allowed)}")
        return v

    class Config:
        # Reject any unexpected columns that might have slipped into the CSV.
        extra = "forbid"
        anystr_strip_whitespace = True
        allow_mutation = False
```