# %%
import requests
import json
from lxml.html import fromstring
import time

# %%
url = 'https://veridoc.org/'
resp = requests.get(url, timeout=10)
resp

# %%
url = 'https://veridoc.org/api/v1/licenseTypes'
resp = requests.get(url, timeout=10)
resp

# %%
resp.text

# %%
with open('check.html', 'wb') as f:
    f.write(resp.content)

# %%
site_key = '6Lc4dKsaAAAAAC19W1N354oeg7CDX7WIusazgdRc'
captcha_api = 'd3419d031fb51df26e5144d6803ce1f3'

def solve_captcha(captcha_api, wurl, sitekey):
    print(wurl, sitekey)
    payload = {
        "clientKey":captcha_api,
        "task": {
            "type":"RecaptchaV3TaskProxyless",
            "websiteURL": wurl,
            "websiteKey": sitekey,
            "minScore": 0.7,  # Lowered for better success rate
            "pageAction": "submit"
        }
    }

    url = 'https://api.2captcha.com/createTask'
    try:
        resp = requests.post(url, json=payload, timeout=30)
        resp_json = resp.json()
        
        if 'errorId' in resp_json and resp_json['errorId'] > 0:
            print(f"Error creating task: {resp_json.get('errorDescription', 'Unknown error')}")
            return None
            
        task_id = resp_json.get('taskId')
        if not task_id:
            print("No taskId in response:", resp_json)
            return None
        
        print(f"Task created with ID: {task_id}")
        
        # Poll for results
        result_url = 'https://api.2captcha.com/getTaskResult'
        for attempt in range(5):
            time.sleep(10)
            result_payload = {"clientKey": captcha_api, "taskId": task_id}
            r = requests.post(result_url, json=result_payload, timeout=30)
            result = r.json()
            
            if result.get('status') == 'ready':
                print("Captcha solved successfully!")
                return result.get('solution', {}).get('gRecaptchaResponse')
            print(f"Attempt {attempt + 1}: Captcha not yet solved. Waiting...")
            
        print("Timed out waiting for captcha solution")
        return None
        
    except Exception as e:
        print(f"Error during captcha solving: {str(e)}")
        return None

# %%
site_url = 'https://veridoc.org/'
gtoken = solve_captcha(captcha_api, site_url, site_key)
gtoken

# %%
gtoken

# %%
session = requests.Session()
site_url = 'https://veridoc.org/'
session.get(site_url)

# %%

headers = {
    'accept': 'application/json',
    'accept-language': 'en-US,en;q=0.9,ta;q=0.8',
    'content-type': 'application/json',
    'origin': 'https://veridoc.org',
    'priority': 'u=1, i',
    'referer': 'https://veridoc.org/',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
}

json_data = {
    'lastName': [
        'Abano',
    ],
    'dateOfBirth': '1980-07-13',
    'licenseTypeGroupId': 'a1b2c3d4-e5f6-47a8-89b0-1c2d3e4f5adb',
    'captchaToken': gtoken
}
proxy = "http://8873af9a8d89581e1953:b936689d98900883@gw.dataimpulse.com:823"
proxies = {'http':proxy, 'https':proxy}
response = requests.post('https://veridoc.org/api/v1/licenses/search', proxies=proxies, json=json_data)
response


