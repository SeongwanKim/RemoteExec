from flask import Flask, render_template_string, render_template
import os 
import datetime
from main import Exec

app = Flask(__name__)
today = datetime.date.today().isoformat()
jobs = []

@app.route('/')
def home():
    return render_template_string('<ul>{% for x in range(10) %}<li>{{ x }}: itm</li>{% endfor%}</ul>, ' + os.getcwd())

@app.route('/cw')
@app.route('/cw/')
@app.route('/cw/<string:target_date>')
def cw(target_date = today ):
    return render_template('cw.html', t_date=target_date, divs = jobs, n_divs = len(jobs))

if __name__ == '__main__':
    j1 = Exec("test1", ['-a', '1'])
    j1.st_time = datetime.datetime(2021,5,14,9,30)
    j1.ed_time = j1.st_time + datetime.timedelta(hours = 1.5)
    j2 = Exec("test1", ['-a', '1'])
    j2.st_time = datetime.datetime(2021,5,14,12,00)
    j2.ed_time = j2.st_time + datetime.timedelta(hours = 2.5)
    jobs = [j1, j2]
    app.run(debug=True)