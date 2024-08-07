# Intelligent Systems Project

This project is an intelligent system designed to simulate a detective solving a murder case. The system can interact via text files, terminal input, and speech recognition. The responses are provided via speech synthesis.

## Table of Contents

- [Intelligent Systems Project](#intelligent-systems-project)
  - [Table of Contents](#table-of-contents)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
    - [macOS](#macos)
    - [Ubuntu](#ubuntu)
    - [Windows](#windows)
  - [Running the Project](#running-the-project)
  - [File Structure](#file-structure)

## Prerequisites

- Python 3.10
- Conda (recommended for environment management)

## Installation

### macOS

1. **Install Homebrew** (if not already installed):
    ```bash
    /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
    ```

2. **Install `portaudio` using Homebrew**:
    ```bash
    brew install portaudio
    ```

3. **Create and activate a new Conda environment**:
    ```bash
    conda create --name intelligent_systems_env python=3.10
    conda activate intelligent_systems_env
    ```

4. **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

### Ubuntu

1. **Install `portaudio`**:
    ```bash
    sudo apt-get install portaudio19-dev
    ```

2. **Create and activate a new Conda environment**:
    ```bash
    conda create --name intelligent_systems_env python=3.10
    conda activate intelligent_systems_env
    ```

3. **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

### Windows

1. **Create and activate a new Conda environment**:
    ```bash
    conda create --name intelligent_systems_env python=3.10
    conda activate intelligent_systems_env
    ```

2. **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

## Running the Project

1. **Activate the Conda environment**:
    ```bash
    conda activate intelligent_systems_env
    ```

2. **Run the main script**:
    ```bash
    python main.py
    ```

## File Structure

```
└── 📁log635_lab3
    └── README.md
    └── 📁__pycache__
        └── agents.cpython-310.pyc
        └── communication.cpython-310.pyc
        └── inference_engine.cpython-310.pyc
        └── text_to_speech.cpython-310.pyc
        └── utils.cpython-310.pyc
    └── agents.py
    └── communication.py
    └── 📁data
        └── facts.txt
        └── input.txt
        └── output.txt
        └── rules.txt
        └── state_board.json
    └── inference_engine.py
    └── main.py
    └── requirements.txt
    └── text_to_speech.py
    └── utils.py
```
