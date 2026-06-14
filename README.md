# State-Driven Form Engine & Lifecycle Modeler Node

This repository houses the complete architecture for a modular, low-code form generation and lifecycle execution mesh. Form structures, state progression paths, and multi-state view masks are completely isolated from targeted business data model instances.

## 🚀 Instant Deployment Playbook (GitHub Codespaces)

1. Click the **Code** dropdown button on this GitHub repository.
2. Select the **Codespaces** tab and click **Create codespace on main**.
3. Wait for the environment setup to finish. The `.devcontainer` automation script will automatically install all node modules and Python dependencies.

## 🛠️ Local Terminal Execution Manifest

If testing locally outside an automated dev-container environment, execute the following commands sequence in separate terminals:

### Step 1: Fire up the Pluggable API Engine
```bash
# From the root directory
pip install -r requirements.txt
cd studio-api
python main.py
