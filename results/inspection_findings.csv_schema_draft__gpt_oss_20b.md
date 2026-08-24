Design a Pydantic data schema that validates each row of the file **inspection_findings.csv**.  
The schema must:

- Define a `BaseModel` named `InspectionFinding` with one field per CSV column.  
- Use the exact column names as field names.  
- Apply the following type and value constraints:  
  - `finding_id`: string matching the pattern `F-\d{4}`.  
  - `reported_date`: ISO‑8601 date string (`YYYY‑MM‑DD`).  
  - `equipment_id`: string matching the pattern `E-\d{4}`.  
  - `equipment_type`: string, no further restriction.  
  - `inspection_type`: literal union of the seven values listed in the CSV description.  
  - `inspection_method`: string, no further restriction.  
  - `finding_description`: non‑empty string.  
  - `reported_by`: non‑empty string.  
  - `reporter_role`: non‑empty string.  
- Include a `Config` class that forbids extra fields.  
- Provide a `@validator` for `reported_date` that ensures the string is a valid date.  
- Provide a `@validator` for `finding_id` and `equipment_id` that enforces the regex patterns.  
- Add concise docstrings to each field explaining its purpose.  
- Output the complete Python code in a single code block, with no surrounding text or markdown headers.  
- Do not include any explanatory prose, comments beyond the required docstrings, or additional output.  
- Ensure the prompt is clear, professional, and unambiguous, so the LLM produces a ready‑to‑use Pydantic model that can be imported and instantiated to parse the CSV rows.