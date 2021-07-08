import sqlite3
import datetime
from worker import Exec


class DB:
    def __init__(self, filename) -> None:
        pass
    def select(self, query):
        pass
    def insert(self, value):
        pass
    def update(self, where, value):
        pass
    def remove(self, where):
        pass

class sqlite(DB):
    import sqlite3
    def __init__(self, filename) -> None:
        super().__init__(filename)  
        self.fn = filename
        self.con = sqlite3.connect(filename)
        self.cur = self.con.cursor()
        self.cur.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tbls = self.cur.fetchall() 
        print(tbls)
        if ('jobs',) not in tbls:
            print('create table for jobs')
            self.cur.execute('''CREATE TABLE jobs
                ( idx integer primary key autoincrement,
                user text, resource text,
                gitAddr text, checkout text, exec text, 
                st_time datetime, ed_time datetime, 
                log text)
            ''')
    def select(self, query = None):
        exec_lst = []
        if query:
            ret = self.cur.execute(f'select * from jobs where {query}')
        else:
            ret = self.cur.execute('select * from jobs')
        for x in ret:
            print(x)
            exec_lst.append(Exec(*x))
        return exec_lst
        pass
    def insert(self, value):
        # check availablity in the time slot
        exec_str = f"insert into jobs {str(tuple(value.keys()))} values {str(tuple(value.values()))}"
        print(exec_str)
        self.cur.execute(exec_str)
        self.con.commit()
        pass
    def update(self, where, value):
        pass
    def remove(self, where):
        pass            

if __name__ == '__main__':
    db = sqlite('sample.db')
    lst = db.select()
    if len(lst) == 0:
        db.insert({
            'user': 'user01',
            'resource': 'none',
            'gitAddr':'',
            'checkout':'',
            'exec':'python --version',
            'st_time':(datetime.datetime(2021,7,1,9,30)).isoformat(),
            'ed_time':(datetime.datetime(2021,7,1,11,0)).isoformat()
        })
        db.insert({
            'user': 'user02',
            'resource': 'none',
            'gitAddr':'',
            'checkout':'',
            'exec':'pip list',
            'st_time':(datetime.datetime(2021,7,2,15,0)).isoformat(),
            'ed_time':(datetime.datetime(2021,7,2,17,45)).isoformat()
        })
        db.insert({
            'user': 'user00',
            'resource': 'none',
            'gitAddr':'git@github.com:SeongwanKim/RemoteExec.git',
            'checkout':'master',
            'exec':'python TestApp.py',
            'st_time':(datetime.datetime(2021,7,3,15,0)).isoformat(),
            'ed_time':(datetime.datetime(2021,7,3,17,45)).isoformat()
        })
        lst = db.select()
    for x in lst:
        x.exec()
