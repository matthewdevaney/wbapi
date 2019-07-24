import requests


# testing the POST method
new_country = {
      'name': 'Cuba',
      'code': 'CUB',
      'region': 'Latin America & Caribbean',
      'population': 11338138,
      'landarea': 104020,
      'density': 109
    }

url = 'http://127.0.0.1:5000/api/countries'
r = requests.post(url, data=new_country)
print(r.text)