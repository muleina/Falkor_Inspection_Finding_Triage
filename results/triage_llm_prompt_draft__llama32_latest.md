Based on the provided knowledge base and query, I will generate a LLM prompt for inspection triaging. Here is the prompt:

"Design a system that performs inspection triage on offshore production platform findings. The system should take a CSV of findings and an equipment registry as input and produce a JSON file of tickets. The system should perform the following tasks:

1. Read the CSV of findings and extract relevant information such as finding_id, reported_date, equipment_id, equipment_type, inspection_type, inspection_method, finding_description, reported_by, and reporter_role.
2. Read the equipment registry and extract relevant information such as equipment_id, equipment_type, criticality_score, reliability_score, redundancy, and engineer_comment.
3. Use the extracted information to calculate the likelihood of failure and impact of failure for each finding, based on the following rules:
	* Likelihood of failure is affected by the presence of trends, repeat failures, active mechanisms, and detection methods.
	* Impact of failure is affected by the presence of redundancy, safety critical elements, and delayed or hidden consequences.
4. Use the calculated likelihood and impact scores to determine the urgency of each finding, based on the following rules:
	* Urgency is derived from a function that takes into account likelihood and impact, with a maximum score of 10.
	* Urgency overrides are applied for certain types of findings, such as those that leave a protection layer impaired or reduce evacuation capacity.
5. Generate a summary for each finding that states what is wrong, on what, and why it matters, without restating the original finding text.
6. Generate a recommended action for each finding that includes a specific activity to be taken, such as raising an impairment entry or replacing a component.
7. Include a review requirement for each finding that touches a safety critical element, and specify the review reason.
8. Produce a JSON file of tickets that includes the following information:
	* ticket_id
	* finding_id
	* equipment_id
	* summary
	* likelihood_of_failure (score and rationale)
	* impact_of_failure (score and rationale)
	* urgency (score and rationale)
	* recommended_action
	* review_required
	* review_reason

The system should be designed to handle 21 findings and produce a single JSON file of tickets. The system should also be able to handle conflicts or ambiguities in the input data and produce a robust and accurate output.

Note: The prompt is designed to be concise and robust, while also ensuring that all requirements are met. The LLM prompt is intended to be used for prompting an LLM agent, and the output should satisfy all requirements given in the knowledge base."