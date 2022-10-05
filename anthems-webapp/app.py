from flask import Flask, render_template, request, redirect
import pandas as pd
import numpy as np
import pycountry as pc
from random import randrange
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import re
import json
import requests

app = Flask(__name__)
app.secret_key = "key"

df = pd.read_csv('static/clean_anthems.csv')
countries_list = list(df['country'].unique())

def get_country_info(name):
    country = df[df['country'] == name]
    alpha3 = country.alpha3.item()
    url = country.url.item()
    translit = country.transliteration.item()
    eng = country.english.item()
    flag = country.image.item()
    return alpha3, url, translit, eng, flag

def remove_stopwords(anthem):
    # Taken from https://www.geeksforgeeks.org/removing-stop-words-nltk-python/
    stop_words = set(stopwords.words('english'))
    anthem = re.sub(r'[^\w]', ' ', anthem)
    word_tokens = word_tokenize(anthem)
    filtered_sentence = [w for w in word_tokens if not w.lower() in stop_words]
    return ' '.join(filtered_sentence)

def freq(str):
    lst_dict = []
    str_list = str.split()
    unique_words = set(str_list)
     
    for word in unique_words :
        dict = {}
        dict['x'] = word
        dict['value'] = str_list.count(word)
        lst_dict.append(dict)
    return lst_dict

def get_definitions(word):
    res = requests.get(f'https://api.dictionaryapi.dev/api/v2/entries/en/{word}')
    definitions = {}

    if res.status_code == 200:
        content = res.json()[0]
        meanings = content['meanings']
        for meaning in meanings:
            type = meaning['partOfSpeech']
            defn = meaning['definitions'][0]['definition']
            definitions[type] = defn
    else:
        definitions['Error'] = '404' 

    return definitions

@app.route('/')
def index():
    return render_template('index.html', countries=countries_list)

@app.route('/random')
def random():
    # Getting a random country
    rand = randrange(len(df))
    name = df['country'][rand]
    # Getting country info 
    alpha3, url, translit, eng, flag = get_country_info(name)
    # Preparing the frequencies    
    eng = remove_stopwords(eng)
    freqs = json.dumps(freq(eng))

    return render_template('country.html', country=name, alpha3=alpha3, flag=flag, eng=eng, translit=translit, freqs=freqs)

@app.route('/country/<name>')
def country(name):
    # Getting country info
    alpha3, url, translit, eng, flag = get_country_info(name)
    # Preparing the frequencies    
    eng = remove_stopwords(eng)
    freqs = json.dumps(freq(eng))

    return render_template('country.html', country=name, alpha3=alpha3, flag=flag, eng=eng, translit=translit, freqs=freqs)

@app.route('/search', methods=["GET","POST"])
def search():
    # Search
    option = request.form.get("search", None)
    search_res = pc.countries.search_fuzzy(option)
    search_res = search_res[0].alpha_3
    name = df[df['alpha3'] == search_res].country.item()
    # Getting country info 
    alpha3, url, translit, eng, flag = get_country_info(name)
    # Preparing the frequencies    
    eng = remove_stopwords(eng)
    freqs = json.dumps(freq(eng))
    # Else
    #word = request.args.get('word', default=None, type=str)
    word = 'cohort'

    return render_template('country.html', country=name, alpha3=alpha3, flag=flag, eng=eng, translit=translit, freqs=freqs)

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)