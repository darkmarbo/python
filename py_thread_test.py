
import thread 
from time import sleep, ctime 


def loop(num,tm): 
    print 'start loop %d at: '%(num), ctime() 
    sleep(int(num)) 
    print 'end.. loop %d at: '%(num), ctime() 

def main(): 
    print 'start main 15 at:', ctime() 
    thread.start_new_thread(loop, (3,5)) 
    thread.start_new_thread(loop, (6,5)) 
    thread.start_new_thread(loop, (9,5)) 
    thread.start_new_thread(loop, (12,5)) 
    sleep(15)
    print 'end.. main 15 at:', ctime() 

if __name__ == '__main__':
    main()
