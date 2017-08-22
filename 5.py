#多线程测试
#定义计时器
import time
from time import sleep,ctime
import threading
#开始时间
start=time.clock()


#程序主体(计算1加到10000000)单线程约4秒：
def half1():
	sum=0
	for i in range(1,5000001):
		sum=sum+i
	return sum
def half2():
	sum=0
	for i in range(5000001,10000001):
		sum=sum+i
	return sum

threads = []
t1 = threading.Thread(target=half1)
threads.append(t1)
t2 = threading.Thread(target=half2)
threads.append(t2)
for t in threads:
	t.setDaemon(True)
	t.start()
t.join()
print(t1)
print(t2)

#结束时间
end=time.clock()
#输出时间
print('Running time: %s Seconds'%(end-start))