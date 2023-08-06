import random
import math
from .Polarizer import *

class Qubit:

    def __init__(self, alpha=0, beta=1):
        self.alpha = alpha
        self.beta = beta
        self.state = [alpha, beta]
        if self.checkState() == False:
            print("Invalid state {} for Qubit".format(self.state))
            self.__exit__()
        
    def cleanup(self):
        self.generateRandomQubit()
        print("Cleaning up Qubit, and creating a new one randomly")
        
    def __exit__(self, *args):
        self.cleanup()
        
    def strOriginalState(self):
        return "Qubit State: " + str(self.state)
        
    def __str__(self):
        polarizer = Polarizer()
        polarizer.polarize(self)
        return "Qubit value: " + str(self.measure()) # It creates a new random Polarizer (Because to "print" a Qubit you have to measure it)

    def checkState(self):
        if 0.99999 <= (self.alpha)**2 + (self.beta)**2 <= 1.11111:
            return True
        return False

    def generateRandomQubit(self):
        self.alpha = random.uniform(0, 1)
        while self.checkState() == False:
            self.alpha = random.uniform(0, 1)
            self.beta = math.cos(math.asin(self.alpha))
            self.state = [self.alpha, self.beta]
        return self

    def changeState(self, alpha, beta):
        self.alpha = alpha
        self.beta = beta
        self.state = [alpha, beta]
        return self
    
    def measure(self):
        if self.alpha == 0 and self.beta == 1:
            return 1
        elif self.alpha == 1 and self.beta == 0:
            return 0
        else:
            return "The Qubit can not be measured"
        
    def createFromBit(self, bit):
        if bit == 1:
            self.changeState(0, 1)
        elif bit == 0:
            self.changeState(1, 0)
        else:
            print(f"Invalid bit {bit} must be 0 or 1")
            self.__exit__()
        return self