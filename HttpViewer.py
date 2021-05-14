from flask import Flask, render_template_string, render_template
import os 
import datetime
from main import 

app = Flask(__name__)
today = datetime.date.today().isoformat()
jobs = [[]]

@app.route('/')
def home():
    return render_template_string('<ul>{% for x in range(10) %}<li>{{ x }}: itm</li>{% endfor%}</ul>, ' + os.getcwd())

@app.route('/cw')
@app.route('/cw/')
@app.route('/cw/<string:target_date>')
def cw(target_date = today ):
    return render_template('cw.html', t_date=target_date, divs = jobs)

if __name__ == '__main__':
    app.run(debug=True)