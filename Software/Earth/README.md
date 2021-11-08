# Earth Emulation Subsystem

### Table of Contents
- [Setup](#setup)
- [Run](#run)
- [Usage](#usage)

### Setup
\[REQUIRED\] Navigate to the folder in the Command prompt `cd path/to/subsystem`

\[OPTIONAL\] Set up the virtual python environment
1. Create a virtual environment: `python -m venv venv`
2. Activate the virtual environment `"env/Scripts/activate"`

\[REQUIRED\] Install dependencies `pip install -r requirements.txt`

### Run

#### Scenario #1
1. Ensure that the virtual environment is configured as specified in [setup](#setup)
2. \[OPTIONAL\] Create a shortcut to `emStart.bat` and place it wherever you desire
3. Run `emStart.bat` (or the shortcut)

#### Scenario #2
1. Ensure that the [setup](#setup) is complete (with or without the virtual environment)
2. If using the virtual environment, verify that it is activated
3. Run the main python script `python emStart.py` (note that if no virtual environment is being used, `emStart.py` can be launched from the file explorer)

### Usage

Once the program is running, it will open multiple windows:
- Simulator
  + This window will display details about the current simulation
  + This window will accept user commands to alter the state of the current simulation or load a new simulation
- Dashboard
  + This window will display when the dashboard has been initialized
  + The user must manually open the browser based dashboard by opening the link