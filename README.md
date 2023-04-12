#Intro

This projet is a GUI in QT made to easily transfer files and directories from computer to ESP32 board with micropython installed, it should work with other microcontrolers

#Requirements

- Python 3.11+
- pyserial
- pyqt6

#On linux

Clone the repository

In order to have access to the board the user need to be in dialout group, for that type the command :
`sudo usermod -a -G dialout $USER`

