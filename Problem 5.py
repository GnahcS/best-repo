def find_smallest():
    numbers = [i for i in range(1,21)]
    n = 20

    while True:
        for i in numbers:
            if n % i != 0:
                n += 1
                break
        else:
            return n
                
print(find_smallest())
