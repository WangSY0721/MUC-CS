import turtle

turtle.setup(1000,1000,100,100)
turtle.speed(2)
turtle.penup()
turtle.goto(-200, 200)

drawpos = -200

def drawShape(n):
    turtle.seth(0)
    turtle.pencolor("red")

    for i in range(n):
        for j in range(0,10):
            turtle.pendown()
            turtle.forward(4)

        turtle.right(180-((180*(n-2))/n))

    for i in range(0,20):
        turtle.penup()
        turtle.forward(4)

# n = int(input("How many shapes do you want? "))
drawShape(3)
drawShape(4)
drawShape(5)
drawShape(6)
turtle.done()