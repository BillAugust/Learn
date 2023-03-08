------------------------------------------------------------------------
This is a program that controls a car with a Raspberry Pi command module
and various sensors in an attempt, at first, to go straight. In includes
code to drive the wheels, get software interrupts to tally the ticks
of the wheel-counters on both sides, code for a camera, compass, AHRS,
and image recognition.
------------------------------------------------------------------------

PROJECT TITLE: Learn
PURPOSE OF PROJECT:Learn
VERSION or DATE:4/29/21
HOW TO START THIS PROJECT:
On a fresh pi:
1. mkdir Develop
2. cd Develop
3. Set up an ssh key on the pi, and upload it to github
4. git clone git@github.com:BillAugust/Learn.git
5. sudo raspi-config
6. In the interface menu, turn on I2C
7. shutdown -r
8. cd Develop
9. git clone https://github.com/romilly/quick2wire-python-api.git
10. cd quick2sire-python-api
11. python3 setup.py
12. cd ../Learn
13. cp project.env ../quick2wire-python-api
14. . ../project.env
15. git clone https://github.com/ameer1234567890/i2clibraries.git
16. Run Thonny and open Car*.py files and have fun.
AUTHORS:
USER INSTRUCTIONS:

