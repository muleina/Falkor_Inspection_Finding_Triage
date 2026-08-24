To design the Pydantic data schema for `inspection_findings.csv`, you should implement a model that strictly enforces the types and constraints defined in the resource variables. Below is the production-ready prompt for an LLM agent to generate this specific implementation.

***

**Prompt Template:**

You are an expert Python developer specializing in data validation and Pydantic. Your task is to design a Pydantic data schema that represents a single row from the `inspection_findings.csv` file.

**Data Specifications:**
The schema must include the following fields with these specific constraints:
- `finding_id`: String. Must follow the pattern `F-####` (e.g., F-1001).
- `reported_date`: Date. Must be parsed from an ISO date string.
- `equipment_id`: String. This is a foreign key into the equipment registry.
- `equipment_type`: String. Denormalized from the registry.
- `inspection_type`: String. Must be restricted to one of the following allowed values: `Routine Operator Round`, `Function Test`, `Corrosion Survey`, `Statutory Inspection`, `Condition Monitoring`, `Structural Survey`, `Shutdown Inspection`.
- `inspection_method`: String. Describes how the finding was detected.
- `finding_description`: String. The primary signal free-text observation.
- `reported_by`: String. Name of the reporter.
- `reporter_role`: String. Job title of the reporter.

**Technical Requirements:**
1. Use `pydantic` (v2) for the implementation.
2. Use `Field` for descriptions and `Literal` or `Enum` for the `inspection_type` to ensure strict validation.
3. Use `datetime.date` for the `reported_date` field.
4. Include a root validator or field validator to ensure the `finding_id` matches the required `F-####` regex pattern.
5. Ensure the model is configured to forbid extra fields to maintain data integrity.

**Output:**
Provide the complete Python code including imports and a brief example of how to instantiate the model with a sample row from the CSV.

***

**Requirement Checklist & Validation:**
- **Field Coverage:** All 9 columns from `inspection_findings.csv` are included.
- **Type Safety:** ISO dates are mapped to date objects; `inspection_type` is constrained to the specific list provided in the scope.
- **Pattern Matching:** The `finding_id` constraint (`F-####`) is explicitly required.
- **Constraint Adherence:** The prompt avoids high-level orchestration frameworks and focuses on the utility library (`pydantic`) permitted by the project constraints.
- **Ambiguity Note:** The prompt treats `equipment_id` as a string, as the registry is a separate CSV and the schema for findings only requires the key.