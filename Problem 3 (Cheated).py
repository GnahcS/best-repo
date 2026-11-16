def generate_prime_numbers(n):
    prime_numbers = []

    for i in range(2, n):        
        for prime in prime_numbers:
            if i % prime == 0:               
                break
        else:
            yield i
            prime_numbers.append(i)

def solution_reducing(n) -> int:
    remainder = n
    last_factor = None
    for prime in generate_prime_numbers(n):
        while remainder % prime == 0:
            last_factor = prime
            remainder /= prime
        if remainder == 1:
            break
    return last_factor

print(solution_reducing(600851475143))

for i in generate_prime_numbers(100):
    print(i)


def largest_prime_factor(n):
    prime_factors = 0

    return prime_factors

