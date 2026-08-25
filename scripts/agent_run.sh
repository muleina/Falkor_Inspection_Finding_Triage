#!/bin/bash
# Author : Mulugeta W. Asres
# bash agent_run_script.sh

echo "Running agent_run_script.sh"

# #####################################################################################
# Ensure the Ollama CLI is installed
if !command -v ollama &> /dev/null; then
    echo "------------------------------------------------"
    echo "Error: Ollama CLI is not installed."
    echo "Please install it first: curl -fsSL https://ollama.com/install.sh | sh"
    echo "------------------------------------------------"
    return 2 2>/dev/null || exit 2
fi

#####################################################################################
# Specify the Ollama LLM model accesspoint to use: local or cloud
LLM_ACCESSPOINT="local"
LLM_ACCESSPOINT="cloud"

# Choose Local LLM model you want to use
# LLM_MODELNAME="llama3.2:latest" # only local

# Choose Cloud Model you want to use
# LLM_MODELNAME="gpt-oss:20b" # Cloud
# LLM_MODELNAME="gpt-oss:120b" # Cloud
LLM_MODELNAME="gemma4" # Cloud

echo $LLM_ACCESSPOINT
echo $LLM_MODELNAME

if [[ "$LLM_ACCESSPOINT" == "local" ]]; then
    echo "Checking if local model '$LLM_MODELNAME' exists..."
    
    # Check if the model name appears in the 'ollama list' outputW
    if ollama list | awk '{print $1}' | grep -q "^${LLM_MODELNAME}$"; then
        echo "Model '$LLM_MODELNAME' is already installed locally."
    else
        echo "Model '$LLM_MODELNAME' is not found. Pulling it now..."
        ollama pull "$LLM_MODELNAME"
    fi

elif [[ "$LLM_ACCESSPOINT" == "cloud" ]]; then
    echo "Checking if OLLAMA_API_KEY exists..."
    
    if [[ -v OLLAMA_API_KEY ]]; then
        echo "OLLAMA_API_KEY exists"
    else
        # Copy here your Ollama API KEY, or export it your environment using setup_ollama_api_key.sh
        # export OLLAMA_API_KEY="__your_api_key__" 
        echo "OLLAMA_API_KEY does not exist. Please run 'bash scripts/setup_ollama_api_key.sh' first (y/n):"
        exit 1
    fi
else
    echo "Invalid LLM_ACCESSPOINT='$LLM_ACCESSPOINT'. Please set is as 'local' or 'cloud'."
    exit 1
fi

# # PROMPT DESIGN FOR TIAGE AGENT USING AI DESGIN ASSISTANT
python triage_agents.py -md "design" -la "$LLM_ACCESSPOINT" -lm "$LLM_MODELNAME" -qt "prompt_design" -s

# # VALIDATOR SCHEMA DESIGN FOR TIAGE AGENT USING AI DESGIN ASSISTANT
python triage_agents.py -md "design" -la "$LLM_ACCESSPOINT" -lm "$LLM_MODELNAME" -qt "schema_validator_design" -s 

# # INSPECTION TRIAGE TOCKET GENERATION USING TICKEET TIAGE AGENT
python triage_agents.py -md "triage" -la "$LLM_ACCESSPOINT" -lm "$LLM_MODELNAME" -mk "equipment_id" -s
