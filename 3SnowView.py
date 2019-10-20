#
# SnowView.py
# @author bulbasaur
# @description 
# @created 2019-03-21T21:47:34.183Z+08:00
# @last-modified 2019-07-04T20:28:52.732Z+08:00
#



from turtle import *
from random import *

def drawSnow():
    hideturtle()
    pensize(2)
    for i in range(120):
        r,g,b=random(),random(),random()
        pencolor((r,g,b))         #snow of various color?
        penup()
        x=randint(-370,370)
        y=randint(1,270)
        goto(x,y)
        pendown()
        ssize = randint(6,15)
        denz = randint(8,12)
        for i in range(denz):
            fd(ssize)
            goto(x,y)
            right(360/denz)

def drawGround():
    hideturtle()
    for i in range(400):
        pensize(randint(4,10))
        x=randint(-400,350)
        y=randint(-290,-1)
        r,g,b=-y/290,-y/290,-y/290
        pencolor((r,g,b))
        penup()
        goto(x,y)
        pendown()
        forward(randint(40,100))

setup(800,600,200,200)
bgcolor("darkgrey")
tracer(False)
drawGround()
drawSnow()
done()
