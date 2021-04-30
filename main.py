import subprocess
import git 
import shlex
import hashlib

class gitManage:
    def __init__(self, path, url = ''):
        pass
    def clone(self, url):
        pass
    def checkout(self, target):
        pass
    def commit(self, target, message):
        pass
    def clean(self, target):
        pass

class Exec:
    def __init__(self, path, args, cwd = None, key = ''):
        self.m_run = path
        self.m_arg = [path, *args]
        self.p = None
        self.cwd = cwd
        if key == '':
            key = hashlib.sha256('_'.join(self.m_arg).encode()).hexdigest()[:16]
        print(key)
        self.log_fn = 'log.txt'
        self.log_fp = open(self.log_fn, 'w')
    def exec(self):
        import os 
        print (os.getcwd())
        self.p =  p = subprocess.Popen(self.m_arg, stdout=self.log_fp, cwd = self.cwd)
    def terminate(self):
        self.p.terminate()
        pass
    def grep(self, pattern = '.*'):
        if self.p == None or self.p.poll():
            return
        x = open(self.log_fn, 'r').read()
        print(x, end='')
        print('-')
        #lines = self.p.stdout.readline()
        #print('lines', lines)
        #print('errs', errs)

class Manager:
    def __init__(self, user):
        self.jobList = []
        self.runList = []
        pass
    def getStatus(self):
        for x in self.jobList:
            x.grep()
        pass
    def setWork(self, job):
        self.jobList.append(job)
        self.jobList[-1].exec()
    def getWork(self):
        return self.jobList[-1]
    def reserve(self, job, startTime, duration, forceEnd = 'false'):
        pass
    def cancle(self, jobID):
        pass

if __name__ == '__main__':
    c = Exec('python', ('TestApp.py', '-m', '1234'))
    m = Manager('swan.kim')
    m.setWork(c)
    import time
    for i in range(4):
        m.getStatus()
        time.sleep(5)
    m.getWork().terminate()
    m.getStatus()
