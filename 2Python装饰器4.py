#-*- coding:utf-8 -*-

"""装饰器类"""
"""
现在我们有了能用于正式环境的logit装饰器，但当我们的应用的某些部分还比较脆弱时，异常也许是需要更紧急关注的事情。
比方说有时你只想打日志到一个文件。而有时你想把引起你注意的问题发送到一个email，同时也保留日志，留个记录。
这是一个使用继承的场景，但目前为止我们只看到过用来构建装饰器的函数。
幸运的是，类也可以用来构建装饰器。那我们现在以一个类而不是一个函数的方式，来重新构建logit。
"""
from functools import wraps

class logging:
    def __init__(self,logfile = 'out.log'):
        self.file = logfile
    
    def __call__(self,func):
        @wraps(func)
        def wrapped_func(*args, **wargs):
            log = func.__name__ + ' was called'
            print(log)
            #打开logfile并开始读写
            with open(self.file,'a') as openfile:
                #将日志写入指定文件
                openfile.write(log + '\n')
            self.notify() #发送一个通知
            return func(*args, **wargs)
        
        return wrapped_func
    
    def notify(self):
        pass

class email_log(logging):
    """实现logging通同时实现发送email的功能"""
    def __init__(self,email = 'joker.lord@foxmail.com',*args,**wargs):
        logging.__init__(self,*args,**wargs)
        self.email = email
        #super(email_log,self).init(*args,**wargs)
    
    def notify(self):
        #实现发送邮件
        pass

name = 'wjk'
@email_log(logfile = 'out_new.log')
def func(name = 'admin'):
    print("{0}使用了他的至高无上的权限".format(name))

func(name)


