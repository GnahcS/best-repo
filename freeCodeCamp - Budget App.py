class Category:
    def __init__(self, category):
        self.category = category
        self.ledger = []
        self.expenses = 0

    def __str__(self):
        ledger_string = f'{self.category:*^30}\n'
        total = self.get_balance()

        for transaction in self.ledger:
            description = transaction['description']
            amount = transaction['amount']
            formatted_amount = f'{amount:>7.2f}'

            if len(description) > 30:
                spacing = 7
            else:
                spacing = 30 - len(description)
            
            ledger_string += f'{description:.23}{formatted_amount:>{spacing}}' 
            ledger_string += '\n'

        ledger_string += f'Total: {total:.2f}'
        return ledger_string


    def deposit(self, amount, description = ''):
        self.ledger.append({'amount': amount, 'description': description})


    def withdraw(self, amount, description = ''):
        if not self.check_funds(amount):
            return False

        self.ledger.append({'amount': -amount, 'description': description})
        self.expenses += amount
        return True


    def get_balance(self):
        current_balance = 0
        for transaction in self.ledger:
            current_balance += transaction['amount']
        return current_balance


    def transfer(self, amount, transfer_destination):
        if not self.check_funds(amount):
            return False
        
        self.withdraw(amount, 'Transfer to ' + transfer_destination.category)
        transfer_destination.deposit(amount, 'Transfer from ' + self.category)
        return True


    def check_funds(self, amount):
        total = 0
        for transaction in self.ledger:
            total += transaction['amount']
        if total < amount:
            return False
        else:
            return True 



def create_spend_chart(categories):
    title = 'Percentage spent by category'

    total_expenses = 0
    expenditure_percentage = []

    # Calculations
    for category in categories:
        total_expenses += category.expenses

    for category in categories:
        rounded_percentages = int((((category.expenses/total_expenses)*100)//10)*10)
        expenditure_percentage.append(rounded_percentages)

    line_length = 3 * len(categories) + 6
    empty_string = ''
    # Write the percentages and o's
    for i in range(100,-1,-10):
        title += f'\n{i:>3}| '
        for j in expenditure_percentage:
            if j >= i:
                title += 'o  '
            else:
                title += '   '
                
    # Write out the dashes
    dashes = '-'*(3 * len(categories) + 1)
    title += f'\n{dashes:>{len(dashes)+4}}\n'

    # Write out the category names horizontally
    longest_category_name = 0
    category_names_string = []
    for category in categories:
        category_names_string.append(category.category)
        if len(category.category) > longest_category_name:
            longest_category_name = len(category.category)
            

    for i in range(longest_category_name):
        title += '     '
        for category in category_names_string:
            if i < len(category):
                title += category[i] + '  '
            else:
                title += '   '
        if i < longest_category_name - 1:
            title += '\n'


    return title


food = Category('Food')
food.deposit(900, 'deposit')
food.withdraw(45.67, 'milk, cereal, eggs, bacon, bread')

business = Category('Business')

food.transfer(100, business)
business.withdraw(67, 'hat')

entertainment = Category('Entertainment')
food.transfer(500, entertainment)
entertainment.withdraw(134, 'gym membership')

print(food)
print('\n')
print(food)
print('\n')

print(create_spend_chart([business, food, entertainment]))