#!/bin/bash
# Author : Mulugeta W. Asres
# bash setup_ollama_api_key.sh

echo "Initiating Ollama sign-in..."
echo "A browser window should open. Log in or create an account if prompted."
echo "--------------------------------------------------------"

# Trigger the CLI login process
ollama signin

echo "--------------------------------------------------------"
echo "Next Steps to grab your API Key:"
echo "1. Go to your browser: https://ollama.com/settings/keys"
echo "2. Click 'Generate API key' (give it a name if asked)."
echo "3. Copy the generated key to your clipboard."
echo "--------------------------------------------------------"

# Prompt user to input the key safely
echo -n "Paste your Ollama API Key here: "
read -s OLLAMA_API_KEY
echo ""

if [ -z "$OLLAMA_API_KEY" ]; then
    echo "Error: No API key provided. Aborting."
    return 1 2>/dev/null || exit 1
fi

# Persist to shell profile for future sessions
echo -n "Please confirm saving the OLLAMA_API_KEY key to your local environment variables? (y/N): "
read -n 1 -r CONFIRM
echo ""
if [[ "$CONFIRM" =~ ^[Yy]$ ]]; then
    # Export to the current environment
    export OLLAMA_API_KEY="$OLLAMA_API_KEY"

    PROFILE_FILE="$HOME/.bashrc"
    [ -n "$ZSH_VERSION" ] && PROFILE_FILE="$HOME/.zshrc"
    [ -f "$HOME/.zprofile" ] && PROFILE_FILE="$HOME/.zprofile"
        
    # Remove older duplicate lines if they exist, then append
    sed -i.bak '/export OLLAMA_API_KEY=/d' "$PROFILE_FILE" 2>/dev/null
    echo "export OLLAMA_API_KEY=\"$OLLAMA_API_KEY\"" >> "$PROFILE_FILE"
    echo "The Key is saved permanently to $PROFILE_FILE"
fi

echo "--------------------------------------------------------"