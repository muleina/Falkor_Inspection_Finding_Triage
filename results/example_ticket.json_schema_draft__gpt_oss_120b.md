```python
"""Pydantic schema for a single ticket as illustrated in
reference/example_ticket.json.

The model captures every field, enforces type constraints, value ranges,
string‑length limits and cross‑field logic required by the exercise
specification.

Only standard library and *pydantic* are used – no external validation
helpers.
"""

import re
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field, validator, root_validator


# --------------------------------------------------------------------------- #
# Helper regular‑expressions that encode the identifier formats required by
# the specification.
# --------------------------------------------------------------------------- #
_TKT_ID_RE = re.compile(r"^TKT-\d{4}$")
_FINDING_ID_RE = re.compile(r"^F-\d{4}$")


def _check_regex(value: str, pattern: re.Pattern, field_name: str) -> str:
    """Utility used by multiple validators."""
    if not pattern.fullmatch(value):
        raise ValueError(f"{field_name!s} must match pattern {pattern.pattern}")
    return value


# --------------------------------------------------------------------------- #
# Sub‑models that appear repeatedly in the ticket structure.
# --------------------------------------------------------------------------- #
class ScoredRationale(BaseModel):
    """A score (1‑10) together with a free‑text rationale."""

    score: int = Field(..., ge=1, le=10, description="Score must be between 1 and 10.")
    rationale: str = Field(
        ...,
        min_length=1,
        description="Human‑readable justification for the score.",
    )

    @validator("rationale")
    def _rationale_not_blank(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("rationale must contain non‑whitespace characters")
        return v


# --------------------------------------------------------------------------- #
# Main ticket model.
# --------------------------------------------------------------------------- #
class Ticket(BaseModel):
    """
    Representation of a single maintenance ticket derived from an inspection finding.

    All constraints described in the brief and in the example JSON are enforced:

    * identifier formats (`ticket_id`, `finding_id`);
    * string‑length limits for ``summary`` and ``recommended_action`` (≤ 300 chars);
    * score ranges (1‑10) for likelihood, impact and urgency;
    * conditional requirement that ``review_reason`` is present when
      ``review_required`` is true.
    """

    ticket_id: str = Field(..., description="Identifier in the form TKT-####")
    finding_id: str = Field(..., description="Identifier in the form F-####")
    equipment_id: str = Field(..., description="Foreign‑key to equipment registry")
    summary: str = Field(..., max_length=300, description="≤ 300 characters")
    likelihood_of_failure: ScoredRationale
    impact_of_failure: ScoredRationale
    urgency: ScoredRationale
    recommended_action: str = Field(..., max_length=300, description="≤ 300 characters")
    review_required: bool = Field(..., description="Whether human review is needed")
    review_reason: Optional[str] = Field(
        None,
        description=(
            "Reason for review; must be provided when ``review_required`` is true. "
            "May be null otherwise."
        ),
    )

    # ------------------------------------------------------------------- #
    # Field‑level validators
    # ------------------------------------------------------------------- #
    @validator("ticket_id")
    def _ticket_id_format(cls, v: str) -> str:
        return _check_regex(v, _TKT_ID_RE, "ticket_id")

    @validator("finding_id")
    def _finding_id_format(cls, v: str) -> str:
        return _check_regex(v, _FINDING_ID_RE, "finding_id")

    @validator("summary", "recommended_action")
    def _trim_whitespace(cls, v: str) -> str:
        """Strip surrounding whitespace – important for length checks."""
        return v.strip()

    # ------------------------------------------------------------------- #
    # Cross‑field validation
    # ------------------------------------------------------------------- #
    @root_validator
    def _review_consistency(cls, values):
        """
        Ensure that ``review_reason`` is supplied (non‑null and non‑empty) when
        ``review_required`` is True, and that it is absent (None) otherwise.
        """
        required = values.get("review_required")
        reason = values.get("review_reason")

        if required:
            if reason is None or not str(reason).strip():
                raise ValueError(
                    "review_reason must be a non‑empty string when review_required is true"
                )
        else:
            # Normalise to None when a reason is supplied but not required.
            if reason is not None:
                values["review_reason"] = None
        return values

    # ------------------------------------------------------------------- #
    # Model configuration – make validation strict and JSON‑serialisable.
    # ------------------------------------------------------------------- #
    class Config:
        anystr_strip_whitespace = True
        json_encoders = {datetime: lambda v: v.isoformat()}
        schema_extra = {
            "example": {
                "ticket_id": "TKT-1005",
                "finding_id": "F-1005",
                "equipment_id": "FG-0455",
                "summary": "Gas detector FG-0455 failed to respond to test gas on two separate cylinders and is functionally dead, leaving the compression module 2oo3 detection group running on two heads with no remaining margin.",
                "likelihood_of_failure": {
                    "score": 10,
                    "rationale": "Not a prediction. The head has already failed its functional test twice with independent test gas while the other two heads responded normally, so the failure is confirmed rather than probable."
                },
                "impact_of_failure": {
                    "score": 7,
                    "rationale": "An SCE protecting a module with high hydrocarbon inventory and ignition sources, but the 2oo3 voting arrangement means gas detection is degraded rather than defeated. A second head loss would defeat it."
                },
                "urgency": {
                    "score": 9,
                    "rationale": "High likelihood and high impact already place this near the top, and the protection‑layer rule escalates it regardless: a failed SCE detector is an impairment from the moment it is known."
                },
                "recommended_action": "Raise an impairment entry for the compression module gas detection group, replace the FG-0455 head, and confirm the remaining two heads respond to test gas before standing the impairment down.",
                "review_required": True,
                "review_reason": "Any ticket touching a Safety Critical Element is routed to a human before it enters the work queue."
            }
        }
```

**Explanation of the validation logic**

* **Identifier format** – regular‑expression checks guarantee the exact “TKT‑####” and “F‑####” patterns required by the brief.  
* **Length limits** – `max_length=300` on `summary` and `recommended_action` enforce the ≤ 300‑character rule. Whitespace stripping prevents accidental length overruns.  
* **Score ranges** – the `ScoredRationale` sub‑model fixes scores to the integer interval [1, 10].  
* **Rationale presence** – a non‑empty string is required for every rationale; blank strings raise a `ValueError`.  
* **Conditional review reason** – a `root_validator` inspects `review_required` and makes `review_reason` mandatory (and non‑blank) when true, otherwise normalises it to `None`.  
* **Schema example** – the `Config.schema_extra` entry mirrors the provided `example_ticket.json`, serving both documentation and a quick sanity check.

The resulting `Ticket` model can be used directly to parse each generated ticket, guaranteeing that every ticket conforms to the structure and business rules defined in the exercise.