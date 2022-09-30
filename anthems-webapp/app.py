from flask import Flask, render_template, request
import pandas as pd
import numpy as np
import pycountry as pc
from random import randrange

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

@app.route('/')
def index():
    return render_template('index.html', countries=countries_list)

@app.route('/random')
def random():
    rand = randrange(len(df))
    name = df['country'][rand]
    alpha3, url, translit, eng, flag = get_country_info(name)

    return render_template('country.html', country=name, alpha3=alpha3, flag=flag)

@app.route('/country/<name>')
def country(name):
    alpha3, url, translit, eng, flag = get_country_info(name)

    return render_template('country.html', country=name, alpha3=alpha3, flag=flag)

@app.route('/search', methods=["GET","POST"])
def search():
    option = request.form.get("search", None)
    search_res = pc.countries.search_fuzzy(option)
    search_res = search_res[0].alpha_3
    name = df[df['alpha3'] == search_res].country.item()
    alpha3, url, translit, eng, flag = get_country_info(name)

    return render_template('country.html', country=name, alpha3=alpha3, flag=flag)

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)