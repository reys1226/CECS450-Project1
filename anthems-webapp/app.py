from flask import Flask, render_template, request, redirect
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from random import randrange
import pycountry as pc
import pandas as pd
import numpy as np
import requests
import json
import re

app = Flask(__name__)
app.secret_key = "key"

df = pd.read_csv('static/clean_anthems.csv')
all_anthems = ' '.join(df["english"])
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

@app.route('/')
def index():
    world_anthems = remove_stopwords(all_anthems)
    freqs = freq(world_anthems)
    max = len(freqs)
    freqs = json.dumps(freqs)

    return render_template('index.html', countries=countries_list, freqs=freqs, anthems=world_anthems, max=max)

@app.route('/random')
def random():
    # Getting a random country
    rand = randrange(len(df))
    name = df['country'][rand]
    # Getting country info 
    alpha3, url, translit, eng, flag = get_country_info(name)
    # Preparing the frequencies    
    eng_stop = remove_stopwords(eng)
    freqs = freq(eng_stop)
    freqs = json.dumps(freqs)

    return render_template('country.html', country=name, alpha3=alpha3, flag=flag, eng=eng, translit=translit, freqs=freqs)

@app.route('/country/<name>')
def country(name):
    # Getting country info
    alpha3, url, translit, eng, flag = get_country_info(name)
    # Preparing the frequencies    
    eng_stop = remove_stopwords(eng)
    freqs = freq(eng_stop)
    freqs = json.dumps(freqs)

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
    eng_stop = remove_stopwords(eng)
    freqs = freq(eng_stop)
    freqs = json.dumps(freqs)

    return render_template('country.html', country=name, alpha3=alpha3, flag=flag, eng=eng, translit=translit, freqs=freqs)

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)