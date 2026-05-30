import turtle

turtle.setup(768,500,100,100)
turtle.speed(2)
turtle.penup()
turtle.goto(-200,200)

def drawShape(color1):
    turtle.seth(0)
    turtle.pencolor(color1)          # 颜色

    # 实线
    for i in range(0, 10):
        turtle.pendown()
        turtle.forward(40)

    turtle.seth(-135)
    for i in range(0, 10):
        turtle.pendown()
        turtle.forward(15)
    print(turtle.position())
    turtle.seth(180)
    for i in range(0, 10):
        turtle.forward(20)
        turtle.forward(20)

    turtle.seth(45)
    for i in range(0, 10):
        turtle.pendown()
        turtle.forward(15)
    turtle.seth(-90)
    for i in range(0, 10):
        turtle.pendown()
        turtle.forward(15)
        turtle.penup()
        turtle.forward(15)
    turtle.penup()
    turtle.goto(200,200)
    turtle.seth(-90)

    for i in range(0, 10):
        turtle.pendown()
        turtle.forward(30)
    turtle.seth(-135)

    for i in range(0, 10):
        turtle.pendown()
        turtle.forward(15)
    turtle.seth(90)
    for i in range(0, 10):
        turtle.pendown()
        turtle.forward(30)
    turtle.penup()
    turtle.goto(-200,-100)
    turtle.seth(-135)
    for i in range(0, 5):
        turtle.pendown()
        turtle.forward(15)
        turtle.penup()
        turtle.forward(15)
    turtle.seth(0)
    for i in range(0, 10):
        turtle.pendown()
        turtle.forward(40)
    turtle.seth(-180)
    turtle.penup()
    for i in range(0, 10):
        turtle.forward(40)
    turtle.seth(90)
    for i in range(0, 10):
        turtle.pendown()
        turtle.forward(30)
    turtle.penup()
    turtle.goto(-200,-100)
    turtle.seth(0)
    for i in range(0, 10):
        turtle.pendown()
        turtle.forward(20)
        turtle.penup()
        turtle.forward(20)
drawShape("black")
turtle.penup()
turtle.goto(-200,200)
drawShape("white")
turtle.home()
turtle.done()
