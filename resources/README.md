# Take-Home Exercise — Inspection Finding Triage

Role: AI Engineer. Expected effort: 4–6 hours. Submit as a repository or archive.

## 1. Scope

Inspection and maintenance activity on an offshore production platform generates findings: free-text
observations recorded against a piece of equipment by whoever made them. Findings are currently
triaged manually by a duty integrity engineer, who assesses each one, assigns scores, writes a
summary and raises a ticket for maintenance planning.

Build the system that performs this triage. Input is a CSV of findings plus an equipment registry.
Output is a JSON file of tickets. A human still approves the result; the system produces the draft.

## 2. Input data

### `data/inspection_findings.csv` — 21 rows

| Column | Notes |
|---|---|
| `finding_id` | `F-####`, unique |
| `reported_date` | ISO date |
| `equipment_id` | Foreign key into the registry |
| `equipment_type` | Denormalised from the registry |
| `inspection_type` | Routine Operator Round, Function Test, Corrosion Survey, Statutory Inspection, Condition Monitoring, Structural Survey, Shutdown Inspection |
| `inspection_method` | How the finding was detected |
| `finding_description` | Free text, written by the person who found it. Primary signal. |
| `reported_by` | Name |
| `reporter_role` | Job title of the reporter |

### `data/equipment_registry.csv` — 18 rows

| Column | Notes |
|---|---|
| `equipment_id` | Primary key |
| `equipment_type`, `service_description` | Descriptive |
| `criticality_score` | 1 = least critical, 10 = most critical |
| `reliability_score` | 1 = fails frequently, 10 = highly reliable. Note the direction. |
| `safety_critical_element` | `Yes` / `No`. Equipment on which a major accident scenario depends. |
| `redundancy` | Free text: `None`, `N+1 (TAG)`, `Voted 2oo3`, `Duplicated (TAG)`, `Yes (bypass available)` |
| `engineer_comment` | Unstructured notes about that specific item |

### `reference/domain_knowledge.md`

Handover notes from the outgoing integrity engineer, describing how findings are currently triaged.
This is the only written record of the triage rules.

### `reference/example_ticket.json`

One ticket, illustrating the required output structure and the expected level of detail in the
rationale fields. The scores shown are one defensible assessment, not a reference answer.

## 3. Required output

A single file, `tickets.json`, containing one ticket per input finding:

```json
{
  "generated_at": "<ISO-8601 timestamp>",
  "tickets_generated": 21,
  "tickets": [ ... ]
}
```

Ticket structure, per `reference/example_ticket.json`:

| Field | Type | Constraint |
|---|---|---|
| `ticket_id` | string | `TKT-####` |
| `finding_id` | string | Must match a `finding_id` in the input |
| `equipment_id` | string | Must match an `equipment_id` in the registry |
| `summary` | string | ≤ 300 characters |
| `likelihood_of_failure` | object | `{ "score": int 1–10, "rationale": string }` |
| `impact_of_failure` | object | `{ "score": int 1–10, "rationale": string }` |
| `urgency` | object | `{ "score": int 1–10, "rationale": string }` |
| `recommended_action` | string | ≤ 300 characters |
| `review_required` | boolean | Whether a human must check the ticket before it enters the work queue |
| `review_reason` | string or null | Required when `review_required` is true |

`summary` states what is wrong, on what, and why it matters, in a form usable in a planning meeting.
It is not a restatement of `finding_description`.

`recommended_action` names a specific activity. "Investigate further" is not sufficient.

Rationale fields cite the evidence used for that score.

### Definition explanation

**Likelihood of failure `likelihood_of_failure` (1–10).** Probability that the item fails to perform its function in the near
term, given the evidence in this finding. A confirmed functional failure that has already occurred
sits at the top of the range. `reliability_score` is a prior, not the answer, and runs in the
opposite direction.

**Impact of failure `impact_of_failure` (1–10).** Consequence if the failure occurs. Accounts for redundancy where it is
real, for delayed and hidden consequences, and for the fact that Safety Critical Elements are judged
against the major accident they protect against rather than against repair cost. `criticality_score`
is a prior, not the answer.

**Urgency `urgency` (1–10).** How soon a human must act. Requirements:

1. Derived from likelihood and impact by a function you define and document. A model asked to output
   an urgency score directly does not satisfy this.
2. Neither a plain average nor a plain maximum. State how your derivation behaves at both corners:
   high likelihood with low impact, and low likelihood with high impact.
3. Supports escalation rules that override the derived value. The domain knowledge notes describe two. Where an
   override applies, state it in the urgency rationale.

## 5. Constraints on building the system

Permitted: any (reasonable) language; any LLM provider or local model; structured-output, function-calling or
constrained-decoding features; schema validators; retry logic you implement; rules or classical NLP
where appropriate.

Not permitted: high-level AI orchestration frameworks — LangChain, LangGraph, LlamaIndex, CrewAI, AutoGen, Haystack, Semantic Kernel, DSPy and equivalents. 
Provider SDKs (`openai`, `anthropic`, `google-genai`, `ollama`) are ok, but only use the inference endpoints and write your own orchestration code. 
Schema libraries (`pydantic`, `zod`, `jsonschema`) and standard data tooling are permitted, with the limitation that we want to see you create
your own orchestration and structured output, without offloading core logic, for example via `Pydantic AI` structured generation or harnesses.
The restriction is on orchestration and logic, not utility.

Additional constraints:

- No hand-written or hand-corrected content in `tickets.json`.
- No committed API keys.
- The system runs end to end from one documented command.
- Keep the cost of a full run low enough to reproduce.

## 6. Design document

Answer the following questions concisely in `DESIGN.md`.

**A. Structured output.** How you enforce conformance to the output structure. Behaviour on a
malformed response, a structural violation, and a valid-but-incorrect score. Failure mode when a
ticket cannot be produced.

**B. Domain knowledge.** How the content of `domain_knowledge.md` and the registry `engineer_comment`
field reaches the model's decision, and why that mechanism. Then: an integrity engineer needs to
change how PSV findings are scored six months from now. What do they modify?

**C. Urgency derivation.** The function, its behaviour at the corners, the override rules, and why
this approach over the alternatives.

**D. Limits.** How the system decides to defer to a human instead of answering. What you chose not
to build, and why.

State any assumptions you made. If you used AI assistance, note how and where you overrode it.

## 7. Deliverables

- `tickets.json` covering all 21 findings, generated by the system
- Source, with a dependency manifest and the run command
- A `DESIGN.md` containing your high-level approach and architecture, along with thoughts you deem relevant
- Use git for version control and send along your commit history so we see how you work

## 8. Assessment criteria

1. System design and structured-output handling: the boundary between model-decided and code-decided
2. Domain knowledge encapsulation and maintainability
3. Output quality: summaries, score defensibility, rationale grounding
4. `DESIGN.md`

Code style, test coverage and packaging are noted but not separately weighted.

## 9. Notes

The 21 findings vary in severity. Several are routine.

Where the brief is ambiguous, make a reasonable assumption, record it in `DESIGN.md` and proceed.
