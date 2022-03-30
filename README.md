# Secure AI Labs

## Setup
- Install Python 3.9 and add python to PATH
- Clone Scratchpad Repo
- Navigate to `StanleyLin/` and Create a virtual environment: `python -m venv <name_venv>`
- Activate your Virtual env (venv): `.\<name_venv>\Scripts\activate`
- Install dependencies on your Virtual env (venv): `pip install -r requirements.txt`
- If running the test_orchestrator suite update config.py to have ORCHESTRATOR_PATH reflect the directory where your Orchestrator python libraries are

## Run active Tests
> `--ip`
> : This is OPTIONAL param used to specify SAIL API portal ip. Defaults to value in Config.py

> `--port`
> : This is OPTIONAL param used to specify SAIL API portal port. Defaults to value in Config.py
- Run Pytest: `pytest StanleyLin/test_api/sail_api_test.py -m active -sv --ip <ip> --port <port> --junitxml=result.xml`
- Example: `pytest StanleyLin/test_api/sail_api_test.py -m active -sv --ip 1.2.3.4 --port 6200 --junitxml=result.xml`

## Deactivate your Virtual Env (venv)
- Exit from your Virtual Env `deactivate`
