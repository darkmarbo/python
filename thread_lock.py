#coding=utf-8
import thread 
from time import sleep, ctime 

loops = [2,4,6,8,10,12,14] 

def loop(nloop, nsec, lock):
    print 'start loop', nloop, 'at:', ctime() 
    sleep(nsec) 
    print 'loop', nloop, 'done at:', ctime()
    #解锁
    lock.release() 

def main():
    print 'starting at:', ctime()
    locks =[]
    #以loops数组创建列表，并赋值给nloops
    nloops = range(len(loops)) 

    for i in nloops:
        lock = thread.allocate_lock()
        #锁定
        lock.acquire()
        #追加到locks[]数组中 
        locks.append(lock)

    #执行多线程
    for i in nloops:
        thread.start_new_thread(loop,(i,loops[i],locks[i]))

    for i in nloops:
        while locks[i].locked():
            pass

    print 'all end:', ctime() 

if __name__ == '__main__': 
    main()


