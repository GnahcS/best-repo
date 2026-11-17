string = '121'
#string = string[::-1]
print(string == string[::-1])

def largest_palindrome():
    all_three_digit_numbers = [i for i in range(100, 1000)]
    largest_palindrome = 0

    for i in all_three_digit_numbers:
        for j in range(100, 1000):
            number = str(i*j)
            if number == number[::-1] and i*j > largest_palindrome:
                largest_palindrome = i*j
                print(i,j)

    return largest_palindrome

print(largest_palindrome())
