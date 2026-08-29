```python
from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel, Field, field_validator, model_validator

class ScoreRationale(BaseModel):
    """Represents a score and its supporting evidence."""
    score: int = Field(..., ge=1, le=10, description="Score between 1 and 10")
    rationale: str = Field(..., min_length=1, description="Evidence used for the score")

class Ticket(BaseModel):
    """Schema for a single maintenance ticket generated from an inspection finding."""
    ticket_id: str = Field(..., pattern=r"^TKT-\d{4}$", description="Unique ticket ID in TKT-#### format")
    finding_id: str = Field(..., pattern=r"^F-\d{4}$", description="Reference to the original finding ID")
    equipment_id: str = Field(..., description="Reference to the equipment registry ID")
    summary: str = Field(..., max_length=300, description="Concise summary of the issue and its significance")
    likelihood_of_failure: ScoreRationale
    impact_of_failure: ScoreRationale
    urgency: ScoreRationale
    recommended_action: str = Field(..., max_length=300, description="Specific activity to resolve the finding")
    review_required: bool = Field(..., description="Whether human approval is required")
    review_reason: Optional[str] = Field(None, description="Reason for review, required if review_required is True")

    @model_validator(mode="after")
    def validate_review_reason(self) -> "Ticket":
        """Ensures review_reason is provided if review_required is True."""
        if self.review_required and not self.review_reason:
            raise ValueError("review_reason is required when review_required is True")
        return self

    @field_validator("recommended_action")
    @classmethod
    def validate_action_specificity(cls, v: str) -> str:
        """Prevents generic 'investigate further' actions as per requirements."""
        forbidden_phrases = ["investigate further", "look into", "check further"]
        if any(phrase in v.lower() for phrase in forbidden_phrases):
            raise ValueError("recommended_action must be a specific activity; 'investigate further' is insufficient")
        return v

class TicketsResponse(BaseModel):
    """Root object for the tickets.json output file."""
    generated_at: str = Field(..., description="ISO-8601 timestamp of generation")
    tickets_generated: int = Field(..., ge=0)
    tickets: List[Ticket]

    @model_validator(mode="after")
    def validate_ticket_count(self) -> "TicketsResponse":
        """Ensures the reported count matches the actual number of tickets in the list."""
        if self.tickets_generated != len(self.tickets):
            raise ValueError(
                f"tickets_generated ({self.tickets_generated}) does not match "
                f"actual ticket count ({len(self.tickets)})"
            )
        return self

    @field_validator("generated_at")
    @classmethod
    def validate_iso_timestamp(cls, v: str) -> str:
        """Validates that the timestamp is a valid ISO-8601 string."""
        try:
            datetime.fromisoformat(v.replace("Z", "+00:00"))
        except ValueError:
            raise ValueError("generated_at must be a valid ISO-8601 timestamp")
        return v
```