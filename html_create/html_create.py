from flask import Flask, render_template
import pandas as pd

app = Flask(__name__, template_folder='../templates')

@app.route('/')
def show_estoque():
    df = pd.read_csv('csv/produtos.csv', sep=';')
    dados = df.to_dict(orient='records')
    return render_template('index.html', estoque=dados)

def start_site():
    app.run(debug=True)
