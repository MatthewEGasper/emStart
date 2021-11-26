# Earth Subsystem

### Table of Contents
- [Setup](#setup)
- [Run](#run)
- [Usage](#usage)
- [Resources](#resources)

***

### Setup

#### Scenario #1 - Batch File
1. Clone the [repository](https://github.com/MatthewEGasper/emStart)
2. Run `Setup.bat`

#### Scenario #2 - Command Line
1. Clone the [repository](https://github.com/MatthewEGasper/emStart)
2. Navigate to the folder in the terminal `cd path/to/subsystem`
3. (*optional*) Set up a virtual python environment
    1. Create a virtual environment: `python -m venv venv`
    2. Activate the virtual environment `"venv/Scripts/activate"`
4. Install project dependencies `pip install -r requirements.txt`

***

### Run

#### Scenario #1 - Batch File
1. Ensure that the virtual environment is configured correctly (see [setup](#setup) 3.i)
2. (*optional*) Create a shortcut to `emStart.bat` and place it anywhere
3. Run `emStart.bat` (or the shortcut)

#### Scenario #2 - Command Line
1. Ensure that the [setup](#setup) is complete
2. If using the virtual environment, ensure that it is active (see [setup](#setup) 3.ii)
3. Run the main python script `python emStart.py`
    1. If no virtual environment is being used, `emStart.py` can be launched from the file explorer
    2. `emStart.py` can be launched with the following arguments:
        - `-h, --help` display the help dialogue
        - `-cmd, --commandline` launch without user interface
        - `-sim, --simulation` launch without arm controls


***

### Usage

#### Emulator
- This window will display information about the state of the robotic arm

#### Simulator
- This window will display details about the current simulation
- This window will accept user commands to alter the state of the current simulation or load a new simulation

#### Dashboard
- This window will display when the dashboard has been initialized
- The user must manually open the dashboard by opening the linked address

***

### Resources

>- [astropy](https://www.astropy.org/) astronomy data package
>- [dash](https://dash.plotly.com/) browser based dashboard package
>- [pymycobot](https://github.com/elephantrobotics/pymycobot) robotic arm package