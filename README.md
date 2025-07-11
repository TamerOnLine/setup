# ⚙️ setup.py — Smart Project Bootstrapper

This script (`setup.py`) automates the setup of a Python project using dynamic configuration. It creates a virtual environment, installs dependencies, and runs the main script defined in `setup-config.json`.

---

## 🎯 Purpose

To make the setup and execution of any Python project automatic and portable without modifying the `setup.py` file itself.

---

## 📁 What It Does

| Task                      | Description                                                                 |
|---------------------------|-----------------------------------------------------------------------------|
| Load configuration        | Reads `setup-config.json` or creates it with default values if missing     |
| Locate Python interpreter | Tries to find `pythonX.Y` based on config version                          |
| Create virtualenv         | Uses `venv` to create the virtual environment                              |
| Upgrade pip               | Ensures pip is up to date                                                   |
| Install requirements      | Installs dependencies from `requirements.txt`, or creates one if missing   |
| Run main script           | Executes the specified `main_file`                                         |
| Clean up temp files       | Deletes files like `tempCodeRunnerFile.py` if found                        |

---

## 🧩 setup-config.json Example

Created automatically on first run if missing:

```json
{
  "project_name": "UnnamedProject",
  "main_file": "main.py",
  "requirements_file": "requirements.txt",
  "venv_dir": "venv",
  "python_version": "3.12"
}
```

You can edit this file freely to adjust the configuration.

---

## 🚀 Available Modes

| Command                          | Description                                                           |
|----------------------------------|------------------------------------------------------------------------|
| `python setup.py full`          | Default mode: creates venv + installs + runs main script               |
| `python setup.py install-only`  | Only creates venv and installs requirements                            |
| `python setup.py run-only`      | Only runs the main script (requires venv to exist)                     |
| `python setup.py full --clean`  | Full clean setup: deletes and recreates virtual environment            |

---

## 📂 Recommended Project Structure

```
your-project/
├── setup.py
├── setup-config.json
├── requirements.txt
├── main.py
└── .github/
    └── workflows/
        └── setup.yml
```

---

## 🔧 Configuration Example

```json
{
  "project_name": "resume-manager",
  "main_file": "setup.py",
  "requirements_file": "requirements.txt",
  "venv_dir": "venv",
  "python_version": "3.12"
}
```

---

## 💡 Highlights

- No need to touch `setup.py` to adapt it to new projects.
- Great for onboarding and consistent local/dev setup.
- GitHub Actions ready.
- Works identically on all OSes that support Python & venv.