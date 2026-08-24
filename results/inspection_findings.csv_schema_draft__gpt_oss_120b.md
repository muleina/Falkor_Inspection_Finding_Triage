You are a Python developer tasked with writing a **single Pydantic data model** that precisely represents each row of the file `data/inspection_findings.csv`.  

The CSV contains the following columns (in the given order) and associated constraints that must be reflected in the schema:

* `finding_id` – a unique identifier in the exact pattern **`F-####`** where each `#` is a digit.  
* `reported_date` – an ISO‑8601 date (e.g., `2024-03-15`).  
* `equipment_id` – a string that matches a key in the equipment registry; treat it as a plain non‑empty string.  
* `equipment_type` – a free‑form string taken from the registry; keep it as a plain string.  
* `inspection_type` – one of the seven known types: `Routine Operator Round`, `Function Test`, `Corrosion Survey`, `Statutory Inspection`, `Condition Monitoring`, `Structural Survey`, `Shutdown Inspection`.  
* `inspection_method` – free‑form string; keep it as a plain string.  
* `finding_description` – free‑form text; keep it as a plain string.  
* `reported_by` – name of the person reporting the finding; keep it as a plain string.  
* `reporter_role` – job title of the reporter; keep it as a plain string.  

Your model must:

1. **Use appropriate Pydantic field types** (`str`, `date`, `Literal`, etc.).  
2. **Enforce the `finding_id` pattern** with a `constr` regex validator.  
3. **Enforce the ISO‑8601 date** by declaring the field as `date`.  
4. **Limit `inspection_type`** to the exact list above by using `Literal` (or an `Enum`).  
5. **Include a helpful docstring** for each field that repeats the note from the CSV description.  
6. **Provide a class‑level docstring** that explains the model represents a single inspection finding record.  
7. **Wrap the entire definition in a single fenced Python code block** and output **only** that code block—no surrounding explanation, no additional prose.  

Before finishing, perform a self‑check and **state explicitly** whether the generated schema satisfies every column constraint listed above. If any constraint cannot be represented directly in Pydantic, mention the limitation and the chosen workaround.  

The response must be concise, production‑ready, and ready to be imported into a Python project without further modification.