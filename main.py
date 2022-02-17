import requests
import os
from dotenv import load_dotenv
from flask import Flask, render_template, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from flask_bootstrap import Bootstrap

load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
Bootstrap(app)


class WordForm(FlaskForm):
    word = StringField('Word to Define:')
    submit = SubmitField("Get Definition")

params = {'key': os.environ.get('APP_KEY')}

@app.route("/", methods=["GET", "POST"])
def home():
    form = WordForm()
    short_def = ""
    if form.validate_on_submit():
        url = f"https://www.dictionaryapi.com/api/v3/references/collegiate/json/{form.word.data}"
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        print(data)
        # definitions = data[0]['def'][0]['sseq']
        # definitions_list = [item for item in definitions]
        # list = definitions_list
        if not isinstance(data[0], dict):
            return render_template("index.html", form=form, short_def='error')
        else:
            short_def = data[0]['shortdef']
    return render_template("index.html", form=form, short_def=short_def)

if __name__ == '__main__':
    app.run(debug=True)