# Assumptions

The provide knowledge resources is small and a simple LLM Agent call has been adopted, instead of adding further complexity of RAG or Agentic AI.

Metadata filtering has been employed based on equipment id during ticketing to avoid contamination of info from other equipment.

LLM inference temprature = 0 has been set to limit hallucinations and force the LLMs to focus on the factual data provided in the prompt.

For LLM inference Ollama is adopted with local and cloud configuration setup, as provided in the setup bash script. 

The codes and orchestration is my own work, no external AI coding, support or external source has been employed, except for the cases explained below under AI assistance.


# AI assistance

I have AI assitance (developed local code for it) to generate prompt draft and data schema pydantic validators for ticketing LLL agent.
The drafts were compared and curated before finally employed in the ticket triaging agent. 
Owing to limited time, I have not explored in-depth on the prompt, but rather supplied the knowledge sources during ticketing inference to improve performance.

    python triage_agents.py -md "design" -la "$LLM_ACCESSPOINT" -lm "$LLM_MODELNAME" -qt "prompt_design" -s

    python triage_agents.py -md "design" -la "$LLM_ACCESSPOINT" -lm "$LLM_MODELNAME" -qt "schema_validator_design" -s 

# A. Structured output

I have added schema validation to the LLM in three stages: TICKET_SCHEMA format in the LLM prompt, output formatting using pydantic during Ollama call, and after retrieving the response.
Currently, failed ticket are skipped with error notification on the terminal, but could have been handled better with LOGGER setup.

# B. Domain knowledge

Currently, the knowledge (small context) and inspection comments are supplied to the LLM prompt directly. 
In case of discrepency between summary instructions (drafted by the AI Design Assistance Agent) and the knowledge: the prompt can be modified to flag the discrepency, trigger regeneration of new summary instructions, or assist the agent with override instruction (how to handle the situation)

# C. Urgency derivation

This should be done with experts, during system design decision on how to handle overriding rule and corner cases. The agent can follow the instruction, e.g. to infer rules and flag the cases. 
I have included extracted knowledge in the draft prompts generated using different LLMs, such as GPT-OSS:20b, Gemma4, GPT-OSS:20b, and GPT-OSS:20b. 
The summary knowledge can be explored the provided 'triage_llm_prompt_draft.md'text files.

# D. Limits 

The current system is build achieve the desire task as minimal complexity. 

I have not spent much effort in assessing in detail the extracted knowledge, as the submission has been focused on building a operations orchestration with minor minor oversight on the domain knowledge. 
Thus, I have provide four tickets.json for each of the four LLMs, "tickets_agent_with_metakey_equipment_id__[LLM_NAME].json".

I have decided not to use knowledge context retrieval through semantic RAG and reasoning Agent for the following reasons: 

    1) The knowledge text is very small, most ist content is relevant for ticketing and can fully fit into the LLM context window. 

    2) Metadata filtering has been employed with per ticket inference for an enhanced accuracy. The drawback is the repeated call to the agent for every ticket, instead of handling the CSV file directly and infer as once.

    3) ReACt (with tool and actions) could be better alternative for modular orchestration using tool calling to handle the full pipeline. I have not included it the submission, due to the limited time and restrictions on dev tools for the task.

    4) Once gain, I wish I added ticket evaluator Agent using RAGAS. It would haven a great addition.

    5) A docker container and test scripts (pytest) would have been a great addition in the repo. But, a simple requirements.txt along with installation and execution scripts have been provided.  

