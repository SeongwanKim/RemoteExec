import datetime
import sys
import getopt
import time

if __name__ == '__main__':
    print(sys.argv)
    i=0
    while True:
        print('test module: ', datetime.datetime.now(), flush = True)
        time.sleep(0.5)

