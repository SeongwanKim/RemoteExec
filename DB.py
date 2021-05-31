import sqlite3


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
                (user text, resource text,
                gitAddr text, checkout text, exec text, 
                st_time datetime, ed_time datetime, 
                log text)
            ''')
    def select(self, query = None):
        if query:
            ret = self.cur.execute(f'select * from jobs where {query}')
        else:
            ret = self.cur.execute('select * from jobs')
        print ret
        return ret
        pass
    def insert(self, value):
        pass
    def update(self, where, value):
        pass
    def remove(self, where):
        pass            

if __name__ == '__main__':
    db = sqlite('test.db')

