from typing import Optional

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from DB import sqlite
import datetime
from worker import Exec

today = datetime.date.today().isoformat()

app = FastAPI()
templates = Jinja2Templates(directory="templates")

db = sqlite('sample.db')
jobs = db.select()

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
        if job.st_time:
            job.x = (job.st_time.weekday()) * 103 + 54
            job.y = job.st_time.hour * 60 + job.st_time.minute + 31
            job.h = ((job.ed_time - job.st_time).seconds * 61 / 3600) 
        else:
            pass
            
    kwargs['divs'] = jobs
    kwargs['n_divs'] = len(jobs)
    kwargs['day'] = datetime.timedelta(days = 1)
    return templates.TemplateResponse('cw.html', kwargs)
    #return kwargs.__str__()

@app.post('/addjob', response_class=HTMLResponse)
async def addjob(request: Request):
    kwargs = {"request": request}
    return templates.TemplateResponse('addJob.html', kwargs)

