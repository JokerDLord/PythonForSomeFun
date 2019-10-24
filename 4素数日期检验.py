#-*- coding:utf-8 -*-
#素数日期检验
import math

def isprime(n):
    n = int(n)
    if n<=1:
        return False
    for i in range(2,int(math.sqrt(n))+1):
        if n%i == 0:
            return False
    return True

def isleap(year):
    year = int(year)
    if (year % 4) == 0 and (year % 100) != 0 \
       or (year % 400) == 0:
        return True   #是闰年
    return False

def isprimed(date):
    n = len(date)
    flag = [isprime(date[i:]) for i in range(n)]
    if False in flag:
        return None
    return print("{0}是一个神奇的日子".format(date))

def main():    
    a,b = eval(input("请输入判断的年份(起始年份，终止年份)："))
    year = [repr(i) for i in range(a,b+1)]
    mon = ["01","02","03","04","05","06",\
           "07","08","09","10","11","12"]
    day = ["31","28","31","30",\
       "31","30","31","31","30","31","30","31",]
    for y in year:
        if isleap(y):
            day[1] = "29"
        else:
            day[1] = "28"
        for index_m in range(len(mon)):
            for d in range(1,int(day[index_m])+1):
                date = y+mon[index_m]+str('{0:02d}'.format(d))
                isprimed(date)    

if __name__ == '__main__':
    main()
