def multiples_of_three_and_five(n):
    divisible_by_three = [i for i in range(1,n) if i % 3 == 0]
    divisible_by_five  = [i for i in range(1,n) if i % 5 == 0]
    divisible_by_both = [i for i in range(1,n) if i % 3 == 0 and i % 5 == 0]

    # print(divisible_by_three)
    # print(divisible_by_five)
    return (sum(divisible_by_three)) + (sum(divisible_by_five)) - (sum(divisible_by_both))

print(multiples_of_three_and_five(1000))