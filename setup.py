import os

vbs_startup_file = "startup.vbs"
home = os.path.expanduser("~")
startup_path = fr"{home}\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup"
current_path = os.path.dirname(os.path.realpath(__file__))
destination = fr"{startup_path}\{vbs_startup_file}"



with open(vbs_startup_file, "r") as script:
    f = script.read()
    
    print(f"Creating {vbs_startup_file} In {destination}")
    with open(destination, "w") as startup_file:
        startup_file.write(f.format(path=fr"{current_path}\alert.py"))

