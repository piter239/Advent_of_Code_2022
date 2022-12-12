import time

t = time.time()
try:
    s = 0
    for i in range(9**9):
        s += 1
finally:
    print("reached", s)
    print("time", t1:=time.time() - t)
    print(f"estimated for {9**14}", (9**14/s * t1)//(3600*24), "days")


