import requests
import json

response = requests.get("https://user-lucasbouju-212605-user.user.lab.sspcloud.fr/attack/745")

if response.status_code != 200:
    raise Exception(
        f"Cannot reach (HTTP {response.status_code}): {response.text}"
    )
else:    
    print(json.dumps(response.json(), indent=2))       # JSON Pretty print