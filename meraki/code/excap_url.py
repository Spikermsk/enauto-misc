# https://github.com/meraki/js-splash
import urllib.parse
s=urllib.parse.unquote("http://localhost:5000/?base_grant_url=https%3A%2F%2Fn143.network-auth.com%2Fsplash%2Fgrant&user_continue_url=http%3A%2F%2Fspeedof.me%2F&node_id=149624922840090&node_mac=88:15:44:60:1c:1a&gateway_id=149624922840090&client_ip=10.255.60.208&client_mac=f4:5c:89:9b:17:67")
#print(s)

# http://localhost:5000/?base_grant_url=https://n143.network-auth.com/splash/grant&user_continue_url=http://speedof.me/&node_id=149624922840090&node_mac=88:15:44:60:1c:1a&gateway_id=149624922840090&client_ip=10.255.60.208&client_mac=f4:5c:89:9b:17:67

url = "http://52.206.215.125/index.html"
params = {
    "base_grant_url": "https://n143.network-auth.com/splash/grant",
    "user_continue_url": "http://njrusmc.net/",
    "node_id": 149624922840090,
    "node_mac": "88:15:44:60:1c:1a",
    "gateway_id": 149624922840090,
    "client_ip": "10.255.60.208",
    "client_mac": "f4:5c:89:9b:17:67"
}

import requests
resp = requests.get(url, params=params)
# print(resp)
# print(resp.text)
print(resp.request.url)
