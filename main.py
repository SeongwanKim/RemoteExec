import subprocess
import git 
import shlex
import hashlib

class gitManage:
    def __init__(self, path, uri = ''):
        self.basePath = path
        pass
    def clone(self, uri):
        git.Git(self.basePath).clone(uri)
        pass
    def checkout(self, target):
        pass
    def commit(self, target, message):
        pass
    def clean(self, target):
        pass

class Exec:
    def __init__(self, path, args, cwd = None, key = '', git_addr = '', checkout = ''):
        self.m_run = path
        self.m_arg = [path, *args]
        self.p = None
        self.cwd = cwd
        if key == '':
            key = hashlib.sha256('_'.join(self.m_arg).encode()).hexdigest()[:16]
        print(key)
        self.log_fn = 'log.txt'
        self.log_fp = open(self.log_fn, 'w')
        self.st_time = None
        self.ed_time = None
        self.forceEnd = False
    def exec(self):
        import os 
        print (os.getcwd())
        self.p =  p = subprocess.Popen(self.m_arg, stdout=self.log_fp, cwd = self.cwd)
    def terminate(self):
        self.p.terminate()
        pass
    def __str__(self):
        return self.__repr__()
    def __repr__(self):
        ret = f"{self.id}, {self.p.pid}, {self.st_time}, {self.ed_time}, {self.forceEnd}, {' '.join(self.m_arg)}"
        return ret
        
    def grep(self, pattern = '.*'):
        if self.p == None or self.p.poll():
            return
        x = open(self.log_fn, 'r').read()
        return x
        #lines = self.p.stdout.readline()
        #print('lines', lines)
        #print('errs', errs)

class Manager:
    def __init__(self, base_path = 'temp'):
        from pathlib import Path
        self.jobList = []
        self.runList = []
        self.cnt = 0
        self.base_path = base_path
        Path(base_path).mkdir(parents=True, exist_ok=True)
        pass

    def setWork(self, job):
        self.jobList.append(job)
        self.jobList[-1].checkout()
        self.jobList[-1].exec()
        self.jobList[-1].id = self.cnt
        self.cnt += 1

    def getWork(self):
        return self.jobList[-1]
    
    def getList(self):
        return self.jobList
    
    def monitor(self):
        pass

    def reserve(self, job, startTime, duration, forceEnd = False):
        self.jobList.append(job)
        self.jobList[-1].st_time = startTime
        self.jobList[-1].ed_time = startTime + duration
        self.jobList[-1].forceEnd = forceEnd
        self.jobList[-1].id = self.cnt
        self.cnt += 1

    def cancle(self, jobID):
        for x in self.jobList:
            if x.id == jobID:
                x.terminate()
        

if __name__ == '__main__':
    c = Exec('python', ('TestApp.py', '-m', '1234'), git_addr='git@github.com:SeongwanKim/RemoteExec.git', checkout='master')
    m = Manager("D:\\Devs\\Temp")
    m.setWork(c)
    import time
    for i in range(4):
        print(m.getWork())
        s = m.getWork().grep()
        print(s)
        time.sleep(5)
    m.getWork().terminate()
