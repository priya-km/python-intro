class Height:
    def __init__(self, feet, inches):
        self.feet = feet
        self.inches = inches

        
    def __gt__(self, other):
        height_inches_A = self.feet * 12 + self.inches
        height_inches_B = other.feet * 12 + other.inches
        return height_inches_A > height_inches_B
        
    def __ge__(self, other):
        height_inches_A = self.feet * 12 + self.inches
        height_inches_B = other.feet * 12 + other.inches
        return height_inches_A >= height_inches_B
    
    def __ne__(self, other):
        height_inches_A = self.feet * 12 + self.inches
        height_inches_B = other.feet * 12 + other.inches
        return height_inches_A != height_inches_B
      
# Height objects
height1 = Height(4, 6)
height2 = Height(4, 5)
height3 = Height(5, 9)
height4 = Height(5, 10)

# Test methods w boolean response
print(height1 > height2)  # Output: True
print(height2 >= height2)  # Output: True
print(height3 != height4)  # Output: True