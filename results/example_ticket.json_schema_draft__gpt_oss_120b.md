You are an expert Python developer tasked with creating a **Pydantic** data model that precisely mirrors the structure and validation rules of the ticket example located in `example_ticket.json`.  

The model must:

* Represent the top‑level ticket object with the exact field names shown in the JSON.
* Enforce the following type and value constraints:
  * `ticket_id` – a string that matches the pattern **TKT‑####** (four digits).
  * `finding_id` – a string, must start with **F‑** followed by digits.
  * `equipment_id` – a string, must start with **FG‑** followed by digits.
  * `summary` – a string limited to **≤ 300 characters**.
  * `likelihood_of_failure`, `impact_of_failure`, and `urgency` – each an object containing:
    * `score` – an integer **1 – 10** inclusive.
    * `rationale` – a non‑empty string.
  * `recommended_action` – a string limited to **≤ 300 characters**.
  * `review_required` – a boolean.
  * `review_reason` – either a string or **null**; if `review_required` is **true**, this field must be a non‑empty string, otherwise it may be null.
* Use appropriate **Pydantic** field types (e.g., `constr`, `conint`, `validator`) to encode the pattern, length, and range checks.
* Include a custom validator that raises a clear `ValueError` when `review_required` is **true** but `review_reason` is missing or empty.
* Provide a top‑level `Ticket` model that can be instantiated directly from the JSON payload (e.g., `Ticket.parse_file(...)`).

Your response must be **pure Python code** defining the required Pydantic models, with no explanatory text, comments, or additional imports beyond those needed for the schema. The code should be ready to copy‑paste into a Python file and run without modification.