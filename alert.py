from urllib.parse import urlencode
import subprocess
import requests
import time
import json

INTERVAL = 10
POPUP_SCRIPT = "quick_popup.vbs"
TEAM = 'monitoring'

def createPopup(title = "New Alerts", body = "Unkown Alert"):
    subprocess.call(f'wscript {POPUP_SCRIPT} "{body}" "{title}"')

def getData():
    base_url = 'https://localhost:42069'
    username = 'admin'
    password = 'qwe123qwe123'

    data = {
        'search': f'| makeresults count=50 | eval team="monitoring", alert_name="dead", description="shit just dieded" | search team="{TEAM}"',
        'output_mode': 'json',
        'exec_mode': 'oneshot'
    }
    
    payload = urlencode(data)
    r = requests.post(base_url + "/services/search/jobs?output_mode=json", data=payload,
                    auth=(username, password), verify=False)
    
    json_response = json.loads(r.text)
    return json_response

def mainloop():
    while True:
        results = getData()['results']
        if results:
            createPopup(body = '\n'.join([result['alert_name'] for result in results]))
        time.sleep(INTERVAL)

def main():
    mainloop()

if __name__ == "__main__":
    main()
