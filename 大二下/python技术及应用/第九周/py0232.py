import turtle

n = int(turtle.numinput("请输入图形圈数","num"))
turtle.setup(1024,400,100,100)
#绘画窗口的宽度、高度，左上角的X坐标、Y坐标。
turtle.speed(2)                      # 速度
turtle.pencolor("white")

def drawShape(color1):
    turtle.seth(0)                   # 0度
    turtle.pencolor(color1)          # 颜色

    for m in range(1,4*n+1):
        for i in range(0,m):
            turtle.pendown()
            turtle.forward(5)
        turtle.left(90)

drawShape("black")
turtle.done()
