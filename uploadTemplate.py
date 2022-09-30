import requests

uploadFiles = [
    ['IKO_PERGRP', 'persongroups.csv'],
    ['IKO_ITEMMASTER', 'IKO_ITEMMASTER.csv',],
    ['IKO_LOCATION','IKO_LOCATION.csv',],
    ['IKO_ASSET','IKO_ASSET.csv',],
    ['IKO_JOBPLAN','IKO_JOBPLAN.csv',],
    ['IKO_JPASSETLINK', 'IKO_JPASSETLINK.csv',],
    ['IKO_JOBLABOR', 'IKO_JOBLABOR.csv'],
    ['IKO_JPASSETLINK', 'IKO_JPASSETLINK2.csv',],
    ['IKO_JOBLABOR', 'IKO_JOBLABOR2.csv'],
    ['IKO_ASSET','IKO_ASSETFailureClass.csv',],
    ['IKO_SPAREPART','SparePart - Copy.csv',],
]

baseUrl = 'https://dev.manage.dev.iko.max-it-eam.com/maximo/api/os/xxx?action=importfile&lean=1'
apiKey = 'n075qt6edkgf931ike9pegc3vejbbtgalabbrrrf'

for file in uploadFiles:
    f = open(file[1], "r")
    body = f.read()
    url = baseUrl.replace('xxx', file[0])
    # preview
    headers = {'apikey': apiKey,'preview': '1','Content-Type': 'text/plain'}
    req = requests.post(url, headers=headers, data=body)
    print(req.text)
    # fr fr
    headers = {'apikey': apiKey,'Content-Type': 'text/plain'}
    req = requests.post(url, headers=headers, data=body)
    print(req.text)