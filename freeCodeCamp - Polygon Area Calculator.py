class Rectangle:
    def __init__(self, width, height):
        self.width = width
        self.height = height
    
    def __str__(self):
        return f'{self.__class__.__name__}(width={self.width}, height={self.height})'

    def set_width(self, width):
        self.width = width

    def set_height(self, height):
        self.height = height

    def get_area(self):
        return (self.width * self.height)

    def get_perimeter(self):
        return (2 * (self.width + self.height))

    def get_diagonal(self):
        return ((self.width ** 2 + self.height ** 2) ** 0.5)

    def get_picture(self):
        if max(self.width, self.height) > 50:
            return 'Too big for picture.'
            
        picture = ''

        for i in range(self.height):
            picture += '*'*self.width
            picture += '\n'

        return picture

    def get_amount_inside(self, other):
        # Match how many widths of (other) fits in the width of (self)
        widths = self.width//other.width
        # Match how many heights of (other) fits in the height of (self)
        heights = self.height//other.height

        amount_inside = widths * heights
        return amount_inside


class Square(Rectangle):
    def __init__(self, side):
        super().__init__(side, side)
        self.side = side

    def __str__(self):
        return f'{self.__class__.__name__}(side={self.side})'

    def set_width(self, side_length):
        self.side = side_length

    def set_height(self, side_length):
        self.side = side_length

    def set_side(self, side_length):
        self.height = side_length
        self.width = side_length
        self.side = side_length
