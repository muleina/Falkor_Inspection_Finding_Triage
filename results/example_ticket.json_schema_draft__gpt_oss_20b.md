```python
from __future__ import annotations

import re
from typing import Optional

from pydantic import BaseModel, Field, root_validator, validator


class ScoreRationale(BaseModel):
    """
    Represents a score (1–10) together with a textual rationale.
    """

    score: int = Field(..., description="Integer score in the inclusive range 1–10.")
    rationale: str = Field(..., description="Non‑empty explanation for the score.")

    @validator("score")
    def _score_in_range(cls, v: int) -> int:
        if not 1 <= v <= 10:
            raise ValueError("score must be between 1 and 10 inclusive")
        return v

    @validator("rationale")
    def _rationale_non_empty(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("rationale must not be empty or whitespace")
        return v


class Ticket(BaseModel):
    """
    Pydantic model for a single triage ticket.
    """

    ticket_id: str = Field(
        ...,
        description="Ticket identifier, e.g. 'TKT-1005'.",
        regex=r"^TKT-\d{4}$",
    )
    finding_id: str = Field(
        ...,
        description="Finding identifier, e.g. 'F-1005'.",
        regex=r"^F-\d{4}$",
    )
    equipment_id: str = Field(
        ...,
        description="Identifier of the equipment that was inspected.",
    )
    summary: str = Field(
        ...,
        description="Concise description of the issue (≤ 300 characters).",
    )
    likelihood_of_failure: ScoreRationale = Field(
        ...,
        description="Assessment of how likely the item will fail.",
    )
    impact_of_failure: ScoreRationale = Field(
        ...,
        description="Assessment of the consequence if the item fails.",
    )
    urgency: ScoreRationale = Field(
        ...,
        description="How soon a human must act.",
    )
    recommended_action: str = Field(
        ...,
        description="Specific action to be taken (≤ 300 characters).",
    )
    review_required: bool = Field(
        ...,
        description="Whether a human must approve the ticket before queueing.",
    )
    review_reason: Optional[str] = Field(
        None,
        description="Explanation for the review requirement, required if review_required is True.",
    )

    @validator("summary")
    def _summary_length(cls, v: str) -> str:
        if len(v) > 300:
            raise ValueError("summary must not exceed 300 characters")
        return v

    @validator("recommended_action")
    def _action_length(cls, v: str) -> str:
        if len(v) > 300:
            raise ValueError("recommended_action must not exceed 300 characters")
        return v

    @root_validator
    def _review_logic(cls, values):
        review_required = values.get("review_required")
        review_reason = values.get("review_reason")

        if review_required:
            if not review_reason or not review_reason.strip():
                raise ValueError(
                    "review_reason must be provided and non‑empty when review_required is True"
                )
        else:
            if review_reason is not None:
                raise ValueError(
                    "review_reason must be omitted or None when review_required is False"
                )
        return values
```