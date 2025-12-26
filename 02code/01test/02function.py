import random

def rand_add():
    a = random.randint(1,100)
    b = random.randint(1,100)
    answer = int(input(f"{a} + {b} = "))
    if answer == a+b:
        print(f"정답입니다.")
    else:
        print(f"오답입니다.")    

rand_add()

