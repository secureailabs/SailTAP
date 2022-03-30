# Secure AI Labs Azure Utility Tools

## Setup
- Install Python 3.9 and add python to PATH
- Clone Scratchpad Repo
- Navigate to `StanleyLin/` and Create a virtual environment: `python -m venv <name_venv>`
- Activate your Virtual env (venv): `.\<name_venv>\Scripts\activate`
- Install dependencies on your Virtual env (venv): `pip install -r .\StanleyLin\misc\requirements.txt`

## del_azure_vm.py (SCRATCHPAD)
> Run script to delete specified vm and its' associated resources in `ScratchpadRg`\
Execute `python del_azure_vm.py`

## manage_virtual_network.py
> Run Script against a empty Subscription. You are required to know  your SUBSCRIPTION_ID \
> Execute az login with azure cli \
Execute `python manage_virtual_network.py`
- Edit const variable names as required except, `GATEWAY_SUBNET` and `FIREWALL_SUBNET` values should not be modified
- Script will setup templated resource group, vnet, vpn, firewall.
- vpn Point 2 Site is not configured. User should design own method to setup P2S
- Empty Firewall Policy is generated. Rules should be ammended by User as deemed necessary.

## Deactivate your Virtual Env (venv)
- Exit from your Virtual Env `deactivate`
