You are an expert Python developer tasked with creating a **single Pydantic model** that precisely captures the structure and constraints of the file **`equipment_registry.csv`** described in the resources.

The model must:

- Define one field for each column in the CSV, using the most appropriate Python type.
- Enforce the numeric range 1 – 10 for both **`criticality_score`** and **`reliability_score`**.
- Represent **`safety_critical_element`** as an enumeration that accepts only the strings `"Yes"` or `"No"`.
- Represent **`redundancy`** as an enumeration limited to the exact values that appear in the reference data: `"None"`, `"N+1 (TAG)"`, `"Voted 2oo3"`, `"Duplicated (TAG)"`, `"Yes (bypass available)"`.
- Treat **`engineer_comment`** as an optional free‑text string (it may be empty or missing).
- Preserve the original column names in the model (e.g., `equipment_id`, `equipment_type`, etc.) and provide clear field‑level docstrings that summarise the meaning of each column as given in the knowledge base.
- Include a custom validator that raises a **`ValueError`** with a helpful message if any field violates its constraints (for example, a score outside 1‑10 or an unexpected enumeration value).
- Supply an example instance (as a Python dictionary) that demonstrates a valid record, and another example that triggers each validation error.
- Output the complete, self‑contained Python source code, including the necessary imports (`pydantic`, `enum`) and the example data structures, wrapped in a single code block.

Your response must **only** contain the requested Python code and the brief explanatory comments above it; do not add any additional narrative, headings, or markdown titles. If you detect missing columns, ambiguous values, or any conflict between the CSV description and the domain‑knowledge notes, explicitly state the issue in a comment within the code and raise a `RuntimeError` explaining why the model cannot be generated.