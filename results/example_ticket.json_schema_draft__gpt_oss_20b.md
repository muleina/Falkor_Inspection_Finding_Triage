Please generate a Pydantic data model that matches the structure of the example ticket JSON shown below.  
The model must enforce the following constraints:

- `ticket_id` must match the pattern `TKT-####` (four digits).  
- `finding_id` must match the pattern `F-####`.  
- `equipment_id` must match the pattern `FG-####`.  
- `summary` and `recommended_action` must be strings of at most 300 characters.  
- `likelihood_of_failure`, `impact_of_failure`, and `urgency` are objects each containing:
  - `score`: an integer in the inclusive range 1–10.  
  - `rationale`: a non‑empty string.  
- `review_required` is a boolean.  
- `review_reason` is a string when `review_required` is `True`; it may be `null` when `review_required` is `False`.  
- Use Pydantic validators to enforce the length limits, regex patterns, and the conditional requirement of `review_reason`.  
- The model should be defined with nested `BaseModel` classes for the three score objects.  
- Include any necessary imports from `pydantic`.  
- Output only the Python code, no explanatory text or markdown fences.  

The code should compile with Pydantic v2 and be ready for use in a production pipeline.