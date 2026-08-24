To implement the Pydantic data schema for the `example_ticket.json` structure, you should use the following implementation. This schema ensures strict type validation, character limits for summaries and actions, and the specific nested structure required for the scoring rationales.

```python
from pydantic import BaseModel, Field, validator
from typing import Optional, List
from datetime import datetime

class ScoreRationale(BaseModel):
    """Represents a score and the evidence-based reasoning behind it."""
    score: int = Field(..., ge=1, le=10, description="Integer score from 1 to 10")
    rationale: str = Field(..., description="Detailed evidence citing the input data used to derive the score")

class Ticket(BaseModel):
    """Individual maintenance ticket generated from an inspection finding."""
    ticket_id: str = Field(..., pattern=r"^TKT-\d{4}$", description="Unique ticket ID in format TKT-####")
    finding_id: str = Field(..., description="Must match a finding_id from the input CSV")
    equipment_id: str = Field(..., description="Must match an equipment_id from the registry")
    summary: str = Field(..., max_length=300, description="Concise summary of what is wrong, on what, and why it matters")
    likelihood_of_failure: ScoreRationale
    impact_of_failure: ScoreRationale
    urgency: ScoreRationale
    recommended_action: str = Field(..., max_length=300, description="Specific activity to resolve the issue; avoid generic terms like 'investigate'")
    review_required: bool = Field(..., description="Whether a human must check the ticket before it enters the work queue")
    review_reason: Optional[str] = Field(None, description="Required if review_required is True")

    @validator('review_reason')
    def check_review_reason(cls, v, values):
        if values.get('review_required') and not v:
            raise ValueError('review_reason is required when review_required is True')
        return v

class TicketResponse(BaseModel):
    """The final output wrapper for all generated tickets."""
    generated_at: str = Field(..., description="ISO-8601 timestamp of generation")
    tickets_generated: int = Field(..., description="Total count of tickets in the list")
    tickets: List[Ticket]
```

This schema satisfies all requirements from the knowledge base: it enforces the 1–10 integer range for scores, implements the maximum 300-character constraints for the `summary` and `recommended_action` fields, and includes a validator to ensure that `review_reason` is provided whenever `review_required` is set to true. The `TicketResponse` class mirrors the required JSON root structure, including the timestamp and total count.