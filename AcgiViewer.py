from typing import Optional

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

import DB
import datetime
from main import Exec

today = datetime.date.today().isoformat()

app = FastAPI()
templates = Jinja2Templates(directory="templates")

j1 = Exec("test1", ['-a', '1'])
j1.st_time = datetime.datetime(2021,5,13,9,30)
j1.ed_time = j1.st_time + datetime.timedelta(hours = 1.5)
j2 = Exec("test2", ['-a', '1'])
j2.st_time = datetime.datetime(2021,5,14,12,00)
j2.ed_time = j2.st_time + datetime.timedelta(hours = 2.5)
j3 = Exec("test3", ['-a', '1'])
j3.st_time = datetime.datetime(2021,5,15,14,00)
j3.ed_time = j3.st_time + datetime.timedelta(hours = 2)
jobs = [j1, j2, j3]

@app.get("/")
async def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
async def read_item(item_id: int, q: Optional[str] = None):
    return {"item_id": item_id, "q": q}

@app.get('/cw/', response_class=HTMLResponse)
async def cw(request: Request, target_date: Optional[str] = today):
    from datetime import date
    kwargs = {}
    kwargs['request'] = request
    kwargs['target_date'] = date.fromisoformat(target_date)
    kwargs['st_date'] = kwargs['target_date'] - datetime.timedelta(days = kwargs['target_date'].weekday())
    for job in jobs:
        job.x = (job.st_time.weekday()) * 103 + 54
        job.y = job.st_time.hour * 60 + job.st_time.minute + 31
        job.h = ((job.ed_time - job.st_time).seconds * 61 / 3600) 
    kwargs['divs'] = jobs
    kwargs['n_divs'] = len(jobs)
    kwargs['day'] = datetime.timedelta(days = 1)
    return templates.TemplateResponse('cw.html', kwargs)
    #return kwargs.__str__()

@app.post('/addjob', response_class=HTMLResponse)
async def addjob(request: Request):
    kwargs = {"request": request}
    return templates.TemplateResponse('addJob.html', kwargs)