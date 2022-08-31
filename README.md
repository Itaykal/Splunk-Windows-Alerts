# Splunk Windows Alerts
## IMPORTANT
`kill.bat` -->
In case something goes wrong there's an emergancy kill file that kills the background process.

## Dependencies
Python. <br />
The `requests` library, should work with any version.

## Installation
Edit `TEAM` in `vars.py` to the name that shows up on the alert action
### Enable on Startup
Run `setup.py` from inside the repo.
### Ad-Hoc
Run from inside the repo.
```
pythonw alert.py
```