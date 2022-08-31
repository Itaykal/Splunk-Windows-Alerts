from logging.handlers import RotatingFileHandler
from urllib.parse import urlencode

import subprocess as sp
import requests
import logging
import time
import json
import os

INTERVAL = 10
ONE_HOUR = 3600
TEAM = 'monitoring'
EXIT_CODES = {
    6: True, # 6 = vbYes - Yes was clicked
    7: False # 7 = vbNo - No was clicked
}

EMERGANCY_KILL = "kill.bat"
POPUP_SCRIPT = "quick_popup.vbs"
LOGGER = "audit.log"


def create_rotating_log(path):
    """
    Creates a rotating log
    """
    formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    logger = logging.getLogger("alert_notification")
    logger.setLevel(logging.INFO)
    
    # add a rotating handler
    handler = RotatingFileHandler(path, maxBytes=10*1024*1024,
                                  backupCount=5)
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    return logger


def Popup(title = "New Alerts", body = "Unkown Alert"):
    body += "\n\nMute alerts for 1 hour?"
    return sp.Popen(f'wscript {POPUP_SCRIPT} "{body}" "{title}"', stdout=sp.PIPE)


def getData():
    base_url = 'https://localhost:42069'
    username = 'admin'
    password = 'qwe123qwe123'

    data = {
        'search': f'''
            | makeresults count=5
            | streamstats count
            | eval team=case(count=1, "monitoring", count=2, "a", count=3, "monitoring", count=4, "b", count=5, "c")
            | eval alert_name=case(count=1, "S3 Bucket is Full (90%)", count=2, "Bruh Moment", count=3, "Splunk Died :(", count=4, "Elad Shamen", count=5, "CPU Usage Over 90%")
            | eval sid=case(count=1, random(), count=2, random(), count=3, random(), count=4, random(), count=5, random())
            | search team="{TEAM}"
            | table team alert_name sid''',
        'output_mode': 'json',
        'exec_mode': 'oneshot'
    }
    
    payload = urlencode(data)
    r = requests.post(base_url + "/services/search/jobs?output_mode=json", data=payload,
                    auth=(username, password), verify=False)
    
    json_response = json.loads(r.text)
    return json_response


def mainloop(logger):    
    while True:
        results = getData()['results']
        if results:
            alerts = [result['alert_name'] for result in results]
            [logger.info(f"raising alert {alert}") for alert in alerts]
            
            p = Popup(body = '\n'.join(alerts))
            p.communicate()[0]
            
            if EXIT_CODES[p.returncode]:
                logger.warning("silent mode period started")
                time.sleep(ONE_HOUR - INTERVAL)
                logger.warning("silent mode period ended")
        time.sleep(INTERVAL)


def main():
    pid = os.getpid()
    logger = create_rotating_log(LOGGER)
    logger.info(f"starting with PID: {pid}")
    with open(EMERGANCY_KILL, "w") as kill:
        kill.write(f"taskkill /PID {pid} /F \npause")
    mainloop(logger)

if __name__ == "__main__":
    main()
