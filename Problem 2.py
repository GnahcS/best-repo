def fibonacci_even_sum(n):
    sum = 0

    fib_0 = 0
    fib_1 = 1

    fib_n = None

    for i in range(n):
        fib_n = fib_0 + fib_1

        fib_0 = fib_1
        fib_1 = fib_n

        if fib_n % 2 == 0 and fib_n <= 4000000:
            sum += fib_n

    return sum

print(fibonacci_even_sum(400))

# def sum_of_even_value(fib_list):
#     sum = 0
#     for i in fib_list:
#         if i % 2 == 0:
#             sum += i
    
#     return sum


