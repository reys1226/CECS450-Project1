from flask import Flask, render_template, request
import pandas as pd
import numpy as np
import pycountry as pc
from random import randrange
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import re

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

@app.route('/')
def index():
    return render_template('index.html', countries=countries_list)

@app.route('/random')
def random():
    rand = randrange(len(df))
    name = df['country'][rand]
    alpha3, url, translit, eng, flag = get_country_info(name)
    eng = remove_stopwords(eng)

    return render_template('country.html', country=name, alpha3=alpha3, flag=flag, eng=eng, translit=translit)

@app.route('/country/<name>')
def country(name):
    alpha3, url, translit, eng, flag = get_country_info(name)    
    eng = remove_stopwords(eng)

    return render_template('country.html', country=name, alpha3=alpha3, flag=flag, eng=eng, translit=translit)

@app.route('/search', methods=["GET","POST"])
def search():
    option = request.form.get("search", None)
    search_res = pc.countries.search_fuzzy(option)
    search_res = search_res[0].alpha_3
    name = df[df['alpha3'] == search_res].country.item()
    alpha3, url, translit, eng, flag = get_country_info(name)
    eng = remove_stopwords(eng)

    return render_template('country.html', country=name, alpha3=alpha3, flag=flag, eng=eng, translit=translit)

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)