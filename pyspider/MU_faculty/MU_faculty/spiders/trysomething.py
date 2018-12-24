import requests as req
import json
api_key = '9008218724e236887e4c74f3eb98c09d'
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/'
                  '537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safar'
                  'i/537.36',
    'Accept': 'application/json'
}
query_string = 'http://api.elsevier.com/content/author/author_id/7202762180?' + '&apiKey=' +api_key + '&start=0&count=20&view=DOCUMENTS'
print(query_string)
response = req.get(query_string,headers=headers)
result = json.loads(response.content)

print("hello")