Please design a Pydantic data model for the `equipment_registry.csv` file.  
The CSV contains the following columns:  

- `equipment_id` – a unique identifier, string.  
- `equipment_type` – descriptive string.  
- `service_description` – descriptive string.  
- `criticality_score` – integer 1–10, where 10 is most critical.  
- `reliability_score` – integer 1–10, where 10 is highly reliable (opposite direction to likelihood).  
- `safety_critical_element` – string, must be either “Yes” or “No” (case‑insensitive).  
- `redundancy` – free‑text description (e.g., “None”, “N+1 (TAG)”, “Voted 2oo3”, “Duplicated (TAG)”, “Yes (bypass available)”).  
- `engineer_comment` – free‑text notes, may be empty.

The Pydantic model should:

1. Inherit from `pydantic.BaseModel`.  
2. Declare each field with the correct type and include a short docstring.  
3. Use `Field(..., ge=1, le=10)` for the score fields to enforce the 1–10 range.  
4. Validate `safety_critical_element` to accept only “Yes” or “No” (case‑insensitive) and store it in title‑case.  
5. Allow `redundancy` and `engineer_comment` to be optional strings (default to empty string).  
6. Provide a `Config` class that sets `allow_population_by_field_name = True` and `json_encoders` if needed.  
7. Include a `parse_row` class method that accepts a dictionary (e.g., from `csv.DictReader`) and returns an instance, raising a `pydantic.ValidationError` on invalid data.  
8. Ensure the model can be serialized to JSON with `model.json()`.

Output only the Python code for the model, no explanatory text.  
If any ambiguity exists (e.g., the exact allowed values for `redundancy`), note it in a comment within the code.