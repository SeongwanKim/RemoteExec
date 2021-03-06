from flask import Flask, render_template_string, render_template, request
import os 
from DB import sqlite
import datetime


from worker import Exec

app = Flask(__name__)
today = datetime.date.today().isoformat()
jobs = []

@app.route('/')
def home():
    return render_template_string('<ul>{% for x in range(10) %}<li>{{ x }}: itm</li>{% endfor%}</ul>, ' + os.getcwd())

@app.route('/cw')
@app.route('/cw-')
@app.route('/cw-<string:target_date>')
def cw(target_date = today ):
    from datetime import date
    kwargs = {}
    kwargs['target_date'] = date.fromisoformat(target_date)
    kwargs['st_date'] = kwargs['target_date'] - datetime.timedelta(days = kwargs['target_date'].weekday())
    for job in jobs:
        job.x = (job.st_time.weekday()) * 103 + 54
        job.y = job.st_time.hour * 60 + job.st_time.minute + 31
        job.h = ((job.ed_time - job.st_time).seconds * 61 / 3600) 
    kwargs['divs'] = jobs
    kwargs['n_divs'] = len(jobs)
    kwargs['day'] = datetime.timedelta(days = 1)
    return render_template('cw.html', **kwargs)

@app.route('/addjob')
def addjob():
    kwargs = {}
    return render_template('addJob.html', **kwargs)


@app.route('/addjob', methods=['POST'])
def addjobPost():
    db = DB.sqlite('schedule.db')
    params = request.form
    db.insert(params)
    return db.select()

if __name__ == '__main__':
    db = sqlite('sample.db')
    jobs = db.select()
    app.run(debug=True)