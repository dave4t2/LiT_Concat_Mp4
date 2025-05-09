# Python Workspace Setup Guide

This guide details instructions that you must follow one after the other to set up a Python development workspace. It includes questions to fine-tune the setup and detailed instructions based on the environment.
Before each step ensure the step instructions are clear.
At the end of each step ensure that the instructions have been applied well and exhaustively

## Environment Assumptions
- **Operating System**: Windows
- **Terminal**: C:\\Program Files\\Git\\bin\\bash.exe"
- **Version Control**: Git is used, but `pre-commit` is not utilized in this setup.

## Important to always remind 
Important : I am using Git\\bin\\bash.exe terminal

## Steps to Set Up the Workspace
follow the following numbered steps one after the other.
Before each step ensure the step instructions are clear.
At the end of each step ensure that the instructions have been applied well and exhaustively and detail you checks


### 1. Create a Virtual Environment
- Run the following command to create and activate a virtual environment:
```bash
python -m venv .venv && source .venv/Scripts/activate
```

### 2. Upgrade `pip`
- Run the following command to ensure `pip` is up-to-date:
```bash
python -m pip install --upgrade pip
```

### 3. Install Dependencies
- If you have specific requirements (e.g., `pandas`), create a `requirements.txt` file and add the dependencies:
```bash
pandas
```
- Install the dependencies:
```bash
pip install -r requirements.txt
```

### 4. Set Up Project Structure
To organize your Python project effectively, create the following structure :

```
project_name/
│
├── README.md          # Overview and usage instructions
├── requirements.txt   # Dependencies (e.g., pandas, openpyxl)
│
|── .github/           # Directory for copilot instructions
│   └── copilot-instructions.md    # copilot instructions
|
|── .prompts/         # Directory for prompts in md files
│   └── Prompts.md    # example prompt 
|
├── src/               # Main source code directory
│   ├── __init__.py    # Makes it a Python package
│   ├── module1.py     # Example module
│   └── module2.py     # Example module
│
├── tests/             # Unit tests and integration tests
│   ├── __init__.py
│   ├── test_module1.py # Tests for module1
│   └── test_module2.py # Tests for module2
│
├── input/             # Directory for input files
│   └── example_input.txt # Example input file for testing
│
├── output/            # Directory for generated output files
│   └── example_output.txt # Example output file
│
├── logs/              # Directory for generated log files
│   └── example_log.txt # Example log file
│
├── docs/              # Documentation files
│   └── usage_guide.md
│
└── scripts/           # Standalone scripts or CLI tools
    ├── run_analysis.py
    └── clean_data.py
```

### Explanation of Key Directories and Files

- **README.md**: Provides an overview of the project and usage instructions.
- **requirements.txt**: Lists the dependencies required for the project.
- **setup.py**: (Optional) Used for packaging and distributing the project.
- **src/**: Contains the main source code, organized into modules and packages.
- **tests/**: Includes unit tests and integration tests for the project.
- **input/**: Stores input files for testing or processing.
- **output/**: Stores generated output files.
- **data/**: (Optional) Contains raw and processed data files.
- **notebooks/**: Stores Jupyter notebooks for analysis or exploration.
- **docs/**: Contains documentation files.
- **scripts/**: Includes standalone scripts or command-line tools.

### 5. Add a `.gitignore` File
- Create a `.gitignore` file to exclude unnecessary files:
``` 
.venv/
__pycache__/
*.pyc
input/
output/
logs/
```

### 6. Install Development Tools (Optional)
- You can install development tools like `make`

- Install `make` using Chocolatey to enable the use of the `Makefile`:
```bash
choco install make
```

### 7. Add a `Makefile`
- Add a `Makefile` to simplify common tasks:
```makefile
install:
    pip install -r requirements.txt

test:
    python -m unittest discover tests

```

### 8. set-up Completion checks

- Review all steps, check that the environment is well aligned with these steps. Confirm the status of your checks