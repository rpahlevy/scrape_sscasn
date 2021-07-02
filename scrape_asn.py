import requests
from bs4 import BeautifulSoup
import json
import base64


def b64(str):
    bytes = str.encode('ascii')
    b64bytes = base64.b64encode(bytes)
    b64str = b64bytes.decode('ascii')
    return b64str
    
def parse_html(content, nama_instansi):
    results = []
    html = BeautifulSoup(content)
    for row in html.find('tbody').find_all('tr'):
        col = row.find_all('td')
        jabatan         = col[0].text.strip()
        lokasi          = col[1].text.strip()
        pendidikan      = col[2].text.strip()
        jenis_formasi   = col[3].text.strip()
        disabilitas     = col[4].text.strip()
        kebutuhan       = col[5].text.strip()
        results.append({
            'nama_instansi': nama_instansi,
            'jabatan': jabatan,
            'lokasi': lokasi,
            'pendidikan': pendidikan,
            'jenis_formasi': jenis_formasi,
            'disabilitas': disabilitas,
            'kebutuhan': kebutuhan,
        })
    return results

cache_dir = '.cache/'
url = 'https://data-sscasn.bkn.go.id/spf?jenisPengadaan=2&instansi='
results = []
with open('instansi.json', 'r') as f:
    instansi = json.loads(f.read())
    total = len(instansi)
    progress = 1
    for i in instansi:
        kode_instansi = i['kode']
        nama_instansi = i['nama']
        print('[{}/{}] {}'.format(progress, total, nama_instansi))
        
        # scraping sh*its
        res = requests.get(url + str(kode_instansi))
        if (res.status_code != 200):
            print('ERROR: ' + res.url)
        else:
            # cache
            with open(cache_dir + b64(res.url), 'w') as c:
                c.write(res.content)
            results.extend(parse_html(res.content, nama_instansi))
        # scraping sh*its
        
        progress += 1
        
with open('asn.json', 'w') as f:
    f.write(json.dumps(results))

