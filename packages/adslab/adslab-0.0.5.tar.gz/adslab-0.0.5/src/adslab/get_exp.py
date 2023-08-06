def exp_one(num):
    f = open(str(num)+".txt", "r")
    con = f.read()
    return con

x = exp_one(1)
print(x)
