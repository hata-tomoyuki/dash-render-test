#!/usr/bin/env python3
"""
Setup script for Oshi App
Automatically creates virtual environment and installs dependencies
"""

import os
import sys
import subprocess
import platform

def run_command(command, cwd=None):
    """Run a shell command and return the result"""
    try:
        result = subprocess.run(
            command,
            shell=True,
            cwd=cwd,
            capture_output=True,
            text=True,
            check=True
        )
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        print(f"Error running command: {command}")
        print(f"Error output: {e.stderr}")
        sys.exit(1)

def main():
    print("Setting up Oshi App...")
    print("=" * 50)

    # Check Python version
    if sys.version_info < (3, 8):
        print("ERROR: Python 3.8 or higher is required")
        sys.exit(1)

    print(f"OK: Python version: {sys.version}")

    # Create virtual environment if it doesn't exist
    venv_path = "venv"
    if not os.path.exists(venv_path):
        print("Creating virtual environment...")
        run_command(f"python -m venv {venv_path}")
        print("OK: Virtual environment created")
    else:
        print("OK: Virtual environment already exists")

    # Activate virtual environment and install requirements
    print("Installing dependencies...")

    if platform.system() == "Windows":
        activate_cmd = f"{venv_path}\\Scripts\\activate"
        pip_cmd = f"{activate_cmd} && python -m pip install --upgrade pip && pip install -r requirements.txt"
    else:
        activate_cmd = f"source {venv_path}/bin/activate"
        pip_cmd = f"{activate_cmd} && python -m pip install --upgrade pip && pip install -r requirements.txt"

    run_command(pip_cmd)
    print("OK: Dependencies installed")

    # Create .env file if it doesn't exist
    if not os.path.exists(".env"):
        print("Creating .env template...")
        env_content = """# Supabase Configuration
SUPABASE_URL=your_supabase_url_here
SUPABASE_KEY=your_supabase_anon_key_here

# IO Intelligence API Configuration
IO_INTELLIGENCE_API_KEY=your_io_api_key_here
IO_INTELLIGENCE_MODEL=meta-llama/Llama-3.2-90B-Vision-Instruct

# Rakuten API Configuration
RAKUTEN_APPLICATION_ID=your_rakuten_app_id_here
"""
        with open(".env", "w", encoding="utf-8") as f:
            f.write(env_content)
        print("OK: .env template created - Please fill in your API keys")

    print("=" * 50)
    print("Setup complete!")
    print("")
    print("To run the app:")
    if platform.system() == "Windows":
        print("  .\\venv\\Scripts\\activate")
        print("  python app.py")
    else:
        print("  source venv/bin/activate")
        print("  python app.py")
    print("")
    print("Or run directly:")
    if platform.system() == "Windows":
        print("  .\\venv\\Scripts\\python app.py")
    else:
        print("  ./venv/bin/python app.py")

if __name__ == "__main__":
    main()
