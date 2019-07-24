import requests


# testing the POST method
new_country = {
    'name': 'Cuba',
    'code': 'CUB',
    'region': 'Latin America & Caribbean',
    'population': 11338138
}

url = 'http://127.0.0.1:5000/api/country'
r = requests.post(url, data=new_country)