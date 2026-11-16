def sum_square_difference(n):
    sum_of_squares = 0
    square_of_sum = 0

    while n > 0:
        sum_of_squares += n*n
        square_of_sum += n
        n -= 1
    square_of_sum *= square_of_sum
    difference = square_of_sum - sum_of_squares

    return difference

print(sum_square_difference(100))
