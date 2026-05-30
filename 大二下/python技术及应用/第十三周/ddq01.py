import sys

def Jiecheng(n):
    a,ans1,ans2,counter = 1,1,1,0
    while True:
        if(counter > n):
          return
        yield ans1
        a = a+1

        ans1 = ans1 * a
        ans2 += ans1
        print(ans2)
        counter = counter + 1


f = Jiecheng(10)

while True:
    try:
        print("阶乘:",next(f),end=" 阶乘和:")
    except:
        sys.exit()