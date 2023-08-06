# 1 = Celcius, 2 = Fahrenheit, 3 = Kelvin, 4 = Reaumur, 5 = Rankine
class TempConv:
    def __init__(self, conv_val, conv_scale):
        self.c_val = conv_val
        self.c_scale = conv_scale
        
    # Type 1 as an argument if you want to print out 'conversion' + 'symbol' as a string.
    def celcius(self, symbol = None):
        if self.c_scale == 1:
            conversion = self.c_val
        elif self.c_scale == 2:
            conversion = (self.c_val - 32)*(5/9)
        elif self.c_scale == 3:
            conversion = self.c_val - 273.15
        elif self.c_scale == 4:
            conversion = self.c_val*(5/4)
        elif self.c_scale == 5:
            conversion = (self.c_val-491.67)*(5/9)
        else:
            conversion = None
            print("Please enter a valid scale.")
        if symbol == 1:
            return (f"{round(conversion, 3)} °C")
        else:
            return conversion

    def fahrenheit(self, symbol = None):
        if self.c_scale == 1:
            conversion = self.c_val + 32*(9/5)
        elif self.c_scale == 2:
            conversion = self.c_val
        elif self.c_scale == 3:
            conversion = self.c_val*(9/5)-459.67
        elif self.c_scale == 4:
            conversion = self.c_val*(9/4)+32
        elif self.c_scale == 5:
            conversion = self.c_val-459.67
        else:
            conversion = None
            print("Please enter a valid scale.")
        if symbol == 1:
            return (f"{round(conversion, 3)} °F")
        else:
            return conversion

    def kelvin(self, symbol = None):
        if self.c_scale == 1:
            conversion = self.c_val + 273.15
        elif self.c_scale == 2:
            conversion = self.c_val*5/9+459.67
        elif self.c_scale == 3:
            conversion = self.c_val
        elif self.c_scale == 4:
            conversion = self.c_val*5/4+273.15
        elif self.c_scale == 5:
            conversion = self.c_val*5/9
        else:
            conversion = None
            print("Please enter a valid scale.")
        if symbol == 1:
            return (f"{round(conversion, 3)} K")
        else:
            return conversion

    def reaumur(self, symbol = None):
        if self.c_scale == 1:
            conversion = self.c_val*4/5
        elif self.c_scale == 2:
            conversion = (self.c_val-32)*4/9
        elif self.c_scale == 3:
            conversion = (self.c_val-273.15)*4/5
        elif self.c_scale == 4:
            conversion = self.c_val
        elif self.c_scale == 5:
            conversion = (self.c_val*5/9+273.15)*4/5
        else:
            conversion = None
            print("Please enter a valid scale.")
        if symbol == 1:
            return (f"{round(conversion, 3)} °Re")
        else:
            return conversion
    
    def rankine(self, symbol = None):
        if self.c_scale == 1:
            conversion = self.c_val*9/5+491.67
        elif self.c_scale == 2:
            conversion = self.c_val+459.67
        elif self.c_scale == 3:
            conversion = self.c_val*9/5
        elif self.c_scale == 4:
            conversion = (self.c_val*5/4-273,15)*9/5
        elif self.c_scale == 5:
            conversion = self.c_val
        else:
            conversion = None
            print("Please enter a valid scale.")
        if symbol == 1:
            return (f"{round(conversion, 3)} R")
        else:
            return conversion
