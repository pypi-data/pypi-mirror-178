import random
import math
from .Qubit import *

class Polarizer:

    def __init__(self, polarizerAngle=0):
        self.polarizerAngle = polarizerAngle
        if self.checkState() == False:
            print("Invalid polarizer angle")
            self.__exit__()
        
    def __str__(self):
        return "Polarizer: " + str(self.polarizerAngle)
    
    def cleanup(self):
        self.generateRandomPolarizer()
        print("Cleaning up Polarizer, and creating a new one randomly")
        
    def __exit__(self, *args):
        self.cleanup()
        
    def generateRandomPolarizer(self):
        self.polarizerAngle = random.choice([0, 1])*90
        return self
    
    def checkState(self):
        if self.polarizerAngle == 0 or self.polarizerAngle == 90:
            return True
        return False
        
    def polarize(self, qubit):
        if self.polarizerAngle == 0:
            probability = qubit.alpha
            value = random.uniform(0, 1)
            if value < probability:
                qubit.changeState(1, 0)
            else:
                qubit.changeState(0, 1)
            return qubit
        elif self.polarizerAngle == 90:
            probability = qubit.beta
            value = random.uniform(0, 1)
            if value > probability:
                qubit.changeState(0, 1)
            else:
                qubit.changeState(1, 0)
            return qubit
        else:
            print("Invalid polarizer angle")
            return None