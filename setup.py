import os
import sys
import json
import subprocess
import shutil

def load_config():
    """Load the setup configuration from setup-config.json or create a default one."""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    config_file = os.path.join(script_dir, "setup-config.json")

    if not os.path.exists(config_file):
        print("Missing setup-config.json file. Creating default one...")

        default_config = {
            "project_name": "UnnamedProject",
            "main_file": "main.py",
            "requirements_file": "requirements.txt",
            "venv_dir": "venv",
            "python_version": "3.12"
        }

        with open(config_file, "w", encoding="utf-8") as f:
            json.dump(default_config, f, indent=2)

        print("Created default setup-config.json.")

    with open(config_file, "r", encoding="utf-8") as f:
        config = json.load(f)

    return config, script_dir

def find_python_executable(version):
    """
    Attempt to find the Python executable matching the specified version.

    Args:
        version (str): Desired Python version.

    Returns:
        str or None: Path to the Python executable if found, else None.
    """
    candidates = [f"python{version}", f"python{version[0]}", "python"]
    for cmd in candidates:
        try:
            output = subprocess.check_output([cmd, "--version"], stderr=subprocess.STDOUT).decode()
            if output.strip().endswith(version):
                return cmd
        except Exception:
            continue
    return None

def get_tool_path(venv_dir, tool):
    """
    Get full path to a tool inside the virtual environment.

    Args:
        venv_dir (str): Path to the virtual environment directory.
        tool (str): Tool name (e.g., 'python', 'pip').

    Returns:
        str: Full path to the tool.
    """
    return os.path.join(venv_dir, "Scripts" if os.name == "nt" else "bin", tool)

def create_virtualenv(python_exe, venv_dir):
    """
    Create a virtual environment and upgrade pip.

    Args:
        python_exe (str): Python executable path.
        venv_dir (str): Directory to create the virtual environment in.
    """
    print("Creating virtual environment...")
    subprocess.run([python_exe, "-m", "venv", venv_dir], check=True)
    print("Upgrading pip...")
    subprocess.run([get_tool_path(venv_dir, "python"), "-m", "pip", "install", "--upgrade", "pip"], check=True)

def install_requirements(venv_dir, requirements_file):
    """
    Install packages from requirements.txt.

    Args:
        venv_dir (str): Virtual environment directory.
        requirements_file (str): Path to the requirements file.
    """
    if not os.path.exists(requirements_file):
        print("requirements.txt not found. Creating an empty one...")
        with open(requirements_file, "w", encoding="utf-8") as f:
            f.write("")
    print("Installing requirements...")
    subprocess.run([get_tool_path(venv_dir, "pip"), "install", "-r", requirements_file], check=True)

def run_main_script(venv_dir, main_file):
    """
    Run the main script specified in the configuration.

    Args:
        venv_dir (str): Path to the virtual environment.
        main_file (str): Path to the main Python script.
    """
    if not os.path.exists(main_file):
        print("Main script not found. Creating a default one...")
        with open(main_file, "w", encoding="utf-8") as f:
            f.write(f'print("Default {os.path.basename(main_file)} is running!")\n')

    print(f"Running {main_file}...")
    args = [arg for arg in sys.argv[1:] if arg not in ["install-only", "run-only", "full", "--clean"]]
    subprocess.run([get_tool_path(venv_dir, "python"), main_file] + args, check=True)

def cleanup_temp_files(script_dir):
    """
    Remove temporary files created during setup.

    Args:
        script_dir (str): Directory where the script is located.
    """
    temp_file = os.path.join(script_dir, "tempCodeRunnerFile.py")
    if os.path.exists(temp_file):
        try:
            os.remove(temp_file)
            print("Removed tempCodeRunnerFile.py.")
        except Exception as e:
            print(f"Failed to remove tempCodeRunnerFile.py: {e}")

def main():
    """
    Main function to manage setup based on provided arguments.
    """
    config, script_dir = load_config()
    os.chdir(script_dir)

    main_file = os.path.join(script_dir, config.get("main_file", "main.py"))
    requirements_file = os.path.join(script_dir, config.get("requirements_file", "requirements.txt"))
    venv_dir = os.path.join(script_dir, config.get("venv_dir", "venv"))
    python_version = config.get("python_version", "3.12")
    python_exe = sys.executable

    selected_python = find_python_executable(python_version)
    if not selected_python:
        print(f"Warning: Could not find python{python_version}. Using current Python: {sys.version.split()[0]}")
        selected_python = python_exe
    else:
        print(f"Found Python {python_version}: {selected_python}")

    args = sys.argv[1:]
    mode = None
    clean_requested = False

    for arg in args:
        if arg in ["install-only", "run-only", "full"]:
            mode = arg
        elif arg == "--clean":
            clean_requested = True

    mode = mode or "full"

    if clean_requested and os.path.exists(venv_dir):
        print("Removing existing virtual environment...")
        shutil.rmtree(venv_dir)

    if mode == "install-only":
        if not os.path.exists(venv_dir):
            create_virtualenv(selected_python, venv_dir)
        install_requirements(venv_dir, requirements_file)
    elif mode == "run-only":
        if not os.path.exists(venv_dir):
            print("Virtual environment not found. Run with: python setup.py install-only or full")
            sys.exit(1)
        run_main_script(venv_dir, main_file)
    elif mode == "full":
        if not os.path.exists(venv_dir):
            create_virtualenv(selected_python, venv_dir)
        install_requirements(venv_dir, requirements_file)
        run_main_script(venv_dir, main_file)
    else:
        print(f"Unknown mode: {mode}")
        print("Usage: python setup.py [install-only|run-only|full] [--clean]")
        sys.exit(1)

    cleanup_temp_files(script_dir)

if __name__ == "__main__":
    config, _ = load_config()
    print(f"Starting setup for project: {config.get('project_name', 'Unnamed')}")
    main()
