# Use the official Ubuntu base image
FROM ubuntu:26.04 

# Prevent interactive prompts during installation
ENV DEBIAN_FRONTEND=noninteractive

# # Install dependencies, add deadsnakes PPA, and install Python 3.14
RUN apt-get update && apt-get install -y --no-install-recommends \
    software-properties-common \
    && add-apt-repository ppa:deadsnakes/ppa \
    && apt-get update \
    && apt-get install -y \
    python3.14 \
    python3.14-venv \
    python3-pip \
    && rm -rf /var/lib/apt/lists/*

# # Create a virtual environment and update PATH so 'pip' and 'python' use it automatically
# RUN update-alternatives --install /usr/bin/python python /usr/bin/python3.14 1
RUN python3 -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Set the working directory inside the container
WORKDIR /app

# Copy only requirements.txt first to optimize Docker caching
COPY requirements.txt .

# Install the Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy all current directory files (respecting .dockerignore)
COPY . .

# # Set the default action to execute when the container starts
ENTRYPOINT ["python", "triage_agents.py"]

##################################################################
# Build Docker Image
# docker build -t falkor_triage_agents .

##################################################################
# Create and Run Docker containers

# PROMPT DESIGN FOR TIAGE AGENT USING AI DESIGN ASSISTANT
# docker run --rm -e OLLAMA_API_KEY=$OLLAMA_API_KEY falkor_triage_agents -md "design" -la "cloud" -lm "gemma4" -qt "prompt_design"

# To save to local file e.g. "D:/Falkor/results", change the path to your local directory path
# docker run --rm -v D:/Falkor/results:/app/results -e OLLAMA_API_KEY=$OLLAMA_API_KEY falkor_triage_agents -md "design" -la "cloud" -lm "gemma4" -qt "prompt_design" -s 


# VALIDATOR SCHEMA DESIGN FOR TIAGE AGENT USING AI DESIGN ASSISTANT
# docker run --rm -v D:/Falkor/results:/app/results -e OLLAMA_API_KEY=$OLLAMA_API_KEY falkor_triage_agents -md "design" -la "cloud" -lm "gemma4" -qt "schema_validator_design" -s

# INSPECTION TRIAGE TOCKET GENERATION USING TICKEET TIAGE AGENT
# docker run --rm -v D:/Falkor/results:/app/results -e OLLAMA_API_KEY=$OLLAMA_API_KEY falkor_triage_agents -md "triage" -la cloud -lm gemma4 -mk "equipment_id" -s
