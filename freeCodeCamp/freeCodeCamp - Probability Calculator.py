import copy
import random

class Hat:
    def __init__(self, **kwargs):
        self.contents = [k for k, v in kwargs.items() for _ in range(v)]
        
    def draw(self, draws):
        drawn_balls = []
        draws_count = min(draws, len(self.contents))

        for i in range(draws_count):
            drawn_balls.append(self.contents.pop(random.randrange(len(self.contents))))    
        
        return drawn_balls

def experiment(hat, expected_balls, num_balls_drawn, num_experiments):
    num_successful = 0
    list_expected_balls = [k for k, v in expected_balls.items() for _ in range(v)]
    
    # print(list_expected_balls)
    
    for _ in range(num_experiments):
        hat_copy = copy.deepcopy(hat)
        drawn_balls = hat_copy.draw(num_balls_drawn)

        # Will return the amount of balls in drawn_balls that matches the balls in expected_balls
        matches = sum([1 for k, v in expected_balls.items() if drawn_balls.count(k) >= v])
        
        # If all balls matches then we were successful
        if matches == len(expected_balls):
            num_successful += 1

    return num_successful/num_experiments


hat = Hat(black=6, red=4, green=3)
probability = experiment(hat=hat,
                  expected_balls={'red':2,'green':1},
                  num_balls_drawn=5,
                  num_experiments=2000)

print(len(hat.contents))
print(probability)