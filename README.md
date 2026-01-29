# Ricky-MCP-Remote
MCP created by myself for helpful tools I want accessible via MCP.


## Requirements:
* Python3 knowledge
* OpenAI API key
* UV Package manager (recommended, can use pip but uv recommended)

### Quick UV Guide (replaces pip, requirements.txt, venv, etc.)
* Assuming you have python 3 installed then you have pip installed
* In terminal:
  
'''
python -m pip install --upgrade pip

touch requirements.txt # add files to this

pip install uv

# SKIP IF NOT WANTED: to run specific version of python
uv python install 3.12

# workflow In Working Folder
uv itit 

# create Environment
uv venv

# activate environment (name relative to folder name, not venv name)
source .venv/bin/activate 

# add packages 
uv add ipykernel ipywidgets jupyterlab "mcp[cli]" openai openai-agents python-dotenv pandas numpy

# sync uv to working venv (if git clone, can run after init)
# can also delete packages if edited out of pyproject.toml
uv sync

# Remove packages (example)
uv remove pandas 
'''

## Service will call random free APIs I am interested in
* Ebird: https://api.ebird.org/v2/data/obs/{{regionCode}}/recent 


## Create .env file for following dependencies:
* OPENAI_API_KEY=your_api_key_here

## create functionality and develope MVP


## Add and setup Authentication 

### Add to ENV:
* AUTH0_DOMAIN=your-auth0-domain
* AUTH0_AUDIENCE=your-api-identifier # same as RESOURCE_SERVER_URL in this example
* RESOURCE_SERVER_URL=<your-server-public-url>/mcp
