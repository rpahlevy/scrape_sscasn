import requests
import json


url = 'https://data-sscasn.bkn.go.id/spf/getInstansi?jenisPengadaan=2'
results = []

res = requests.get(url)
if (res.status_code == 200):
    results = json.loads(res.content)
    with open('instansi.json', 'w') as f:
        f.write(json.dumps(results, indent=2))
