### TJ Scherer's
# Engineering Notebook

### 9/13
Met with the product owner (Dr. Liu)

### 9/14
Began working on the System Architecture section of the SDS

### 9/15
Reformatted the SDS to maintain consistent styling
Added some issues to the project to start the product backlog:
- [ ] https://github.com/MatthewEGasper/emStart/issues/1
- [ ] https://github.com/MatthewEGasper/emStart/issues/2
- [ ] https://github.com/MatthewEGasper/emStart/issues/3

### 9/16
Added more issues to the project to further develop the product backlog:
- [ ] https://github.com/MatthewEGasper/emStart/issues/7
- [ ] https://github.com/MatthewEGasper/emStart/issues/8
- [ ] https://github.com/MatthewEGasper/emStart/issues/9

Added the product vision to the [wiki](https://github.com/MatthewEGasper/emStart-Senior-Design/wiki)
- [x] https://github.com/MatthewEGasper/emStart/issues/6

### 9/17
Added more issues to the project to further develop the product backlog:
- [ ] https://github.com/MatthewEGasper/emStart/issues/10
- [ ] https://github.com/MatthewEGasper/emStart/issues/26

Edited issues, adding assignees, descriptions, tags, and milestones
- [ ] https://github.com/MatthewEGasper/emStart/milestone/2?closed=1
- [ ] https://github.com/MatthewEGasper/emStart/milestone/1?closed=1
- [ ] https://github.com/MatthewEGasper/emStart/milestone/3?closed=1

### 9/20
Met with the product owner
Worked with team to decide on hardware and software architectures for the project
Completed section 2 of the SDS

### 9/21
Added most of section 2 to the SRS

### 9/27
Met with the product owner
- Requested more detailed plans for the Earth subsystem software
- Determined that python would be the best language to use
- [ ] https://github.com/MatthewEGasper/emStart/issues/22

Updated SRS 2.3, completing section 2 of the SRS

### 9/28
Submitted the SRS and SDS
- [x] https://github.com/MatthewEGasper/emStart/issues/2
- [x] https://github.com/MatthewEGasper/emStart/issues/3

### 9/29- 10/3
Worked on the Earth subsystem software
- Added argument parser for command line interface
- Calculated the UTC time given the latitude and longitude of the ground station and the local time
- Integrated astropy to get astronomy data at the location of the ground station

### 10/4
Met with the product owner
- Demonstrated software obtaining astronomy data and performing calculations in the command line interface
- [x] https://github.com/MatthewEGasper/emStart/issues/22
- Product owner requested a graphical user interface as well

### 10/5
Met with the product owner
- Demonstrated software obtaining astronomy data and performing calculations in the command line interface
- [ ] https://github.com/MatthewEGasper/emStart/issues/22

### 10/5
Sprint 1 Demo
- [x] https://github.com/MatthewEGasper/emStart/issues/7
- [x] https://github.com/MatthewEGasper/emStart/issues/8
- [x] https://github.com/MatthewEGasper/emStart/issues/9
- [x] https://github.com/MatthewEGasper/emStart/issues/27

### 10/6- 10/17
Worked on the Earth subsystem software
- Integrated dash and plotly for the user interface
- Successfully tracked the altitude and azimuth of the sun from a given location
- Displayed this progress on a graph

### 10/18
Met with the product owner
- Demonstrated software accepting inputs and displaying data on an interactive graph in the user interface
- Product owner requested new software architecture for Earth subsystem, using sockets on independent programs for the emulator and the user interface
- [x] https://github.com/MatthewEGasper/emStart/issues/22

### 10/19
Test Plan
- [x] https://github.com/MatthewEGasper/emStart/issues/26

### 10/20
Worked on Earth subsystem software
- Began integrating ZeroMQ sockets so that the emulator and the user interface can operate independent of each other, only communicating through the sockets
- This required a lot of new architecture planning
- I lost sleep over this

### 10/22
Created engineering notebook and updated it to present
Added real time capabilities to ensure emulation is timed properly without drift
Added ZeroMQ socket functionality to improve the user interface, displaying the altaz data on a real time graph
Updated required sections of SDS and SRS in preparation for v2

### 10/25
Met with product owner
- Demonstrated software communication through sockets
- Demonstrated software updating in real-time based on configuration
- Began planning integration with the robotic arm skeleton code

### 10/26
Made final touches for SDS and SRS v2

### 10/27
Picked up delivery containing almost everything except the robotic arm
- The robotic arm was ordered on 10/20 and has no shipping information or estimated delivery

Worked on presentation for sprint 2 demo

### 10/28
Presented the sprint 2 demo

### 11/4
Improved socket architecture for more efficient communication
Added small features to command line interface
Added example user configurations to demonstrate usage of multiple stored sequences

### 11/5
Made improvements to responsiveness of user interface

### 11/6
Updated engineering notebook

### 11/8-11/10
Integrated robotic arm code into the rest of the subsystem in preparation for the arrival of the arm
Made some more small improvements to the user interface to ensure proper updating

### 11/13
Updated engineering notebook

### 11/15
Met with product owner
- Demonstrated controlling the robotic arm
- The algorithm for positioning the robotic arm needs improvements

### 11/16
Worked in the lab to improve the movement of the robotic arm