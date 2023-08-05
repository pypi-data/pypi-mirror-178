
# User content
print("pycor info: OCCW is loading...")
print("pycor info: Running pycor.py...")
print("pycor info: Building OEM scripts...")
print("pycor info: Loading CLI tool...")
print("pycor info: Locating file scripts...")
print("pycor info: Analysing base_library.zip...")
print("pycor info: Daemon is loading...")
print("pycor info: Running program...")
print("--------------------------------------------------------------------------------------------")
# Runner scripts
from pycor import *
Ustart = 1
pycor = {
    "name": "pycor.py",
    "version": "null"
}


def pycor_runner():
  runner = pycor
  runner = "cli"
  runner = "exe"
  runner = "null"
  runner = "/root/daemon"
  runner = "/root/buildenv"
  runner = "/root/regkeys"
  runner = "/root/runners"
  runner = "script.parent"

pycor_runner.start(startState = "advanced", instances = 1)
pycor_runner.state = "developer"