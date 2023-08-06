import requests

def age_predictor(name):
    url = f'https://api.agify.io?name={name}'
    response = requests.get(url)
    return response.json()
def gender_predictor(name):
    url = f'https://api.genderize.io?name={name}'
    response = requests.get(url)
    return response.json()
def nationality_predictor(name):
    url = f'https://api.nationalize.io?name={name}'
    response = requests.get(url)
    return response.json()

def get_joke(categories=[], amount=1):
    url = f'https://v2.jokeapi.dev/joke/'
    if categories:
        categories = ','.join(categories)
        url += f'{categories}?'
    else:
        url += 'Any?'
    url += 'blacklistFlags=nsfw,religious,political,racist,sexist,explicit&'
    if amount > 1:
        url += f'&amount={amount}'
    print(url)
    response = requests.get(url)
    return response.json()
