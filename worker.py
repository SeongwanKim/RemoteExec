import subprocess
import shlex
import hashlib
from git import Repo
class gitManage:
    def __init__(self, path):
        self.basePath = path
        self.rsa_key = '.ssh/'
        pass
    def register(self, user, pvt):
        with open(f'{self.rea_key}/{user}') as fp:
            fp.write(pvt)
    def clone(self, uri, user = 'default'):
        gitAddrExists = False
        if gitAddrExists:
            pass
        else:
            repo_name = uri.split('.git')[0].split('/')[-1]
            #git.Git(self.basePath).clone(uri)
            Repo.clone_from(uri, f'{self.basePath}/{repo_name}' ,
             env={"GIT_SSH_COMMAND": f'ssh -o StrictHostKeyChecking=no -i {self.rsa_key}/{user}'})
    def checkout(self, target):
        pass
    def commit(self, target, message):
        pass
    def clean(self, target):
        pass

class Exec:
    def __init__(self, 
    idx, # dummy
    user='None',
    resource='',
    git_addr = '', 
    checkout = '', 
    exec='', 
    st_time='',
    ed_time='',
    log = '' #dummy
    ):
        import os 
        if not os.path.exists(user):
            os.mkdir(user)
        self.cwd = user
        self.m_arg = exec
        self.p = None
        self.log_fn = f'{self.cwd}/log_{idx}.txt'
        self.log_fp = open(self.log_fn, 'w')
        self.st_time = st_time
        self.ed_time = ed_time
        self.forceEnd = False
        self.id = idx
        self.pid = -1
        self.git_addr = git_addr
        self.checkout = checkout
        self.user = user
        self.resource = resource
    def exec(self):
        import os 
        print (os.getcwd())
        if self.git_addr != '':
            self.git_manager = gitManage(self.cwd)
            #if (os.path.exists() )
            self.git_manager.clone(self.git_addr)
            self.git_manager.checkout(self.checkout)
            # check out to local git 
            print('check out git from ...')
            pass

        self.p = subprocess.Popen(shlex.split(self.m_arg), stdout=self.log_fp, cwd = self.cwd)
    def terminate(self):
        self.p.terminate()

    def __str__(self):
        return self.__repr__()
    def __repr__(self):
        ret = (f"{self.id}\n"
        f"{self.st_time}\n"
        f"{self.ed_time}\n"
        f"{self.forceEnd}\n"
        f"arg: {' '.join(self.m_arg)}"
        )
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
