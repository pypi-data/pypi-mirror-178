import turtle

import matplotlib.pyplot as plt
import numpy

class Turtler:

    def __init__(self):
        turtle.mode("logo")
        turtle.title("Turtler")
        self.t = turtle.Turtle()
        self.t.shape("turtle")
        self.stepSize = 100
        self.plotType = "directions"

        self.nUp = 0
        self.nDown = 0
        self.nLeft = 0
        self.nRight = 0

        self.start()
    
    def start(self):
        print("\n===== Turtler =====\n\nHello, Turtles!\nPaste this into your browser to see the documentation: https://github.com/dehadeaaryan/turtler\n\n===================\n")

    def setStepSize(self, size : int):
        self.stepSize = size
    
    def setSpeed(self, speedString : str):
        if speedString == "fastest":
            self.t.speed(0)
        elif speedString == "fast":
            self.t.speed(10)
        elif speedString == "normal":
            self.t.speed(6)
        elif speedString == "slow":
            self.t.speed(3)
        elif speedString == "slowest":
            self.t.speed(1)
        else:
            print("Invalid speed")
        speed = 0
        self.t.speed(speed)
    
    def done(self):
        self.plot()
        turtle.done()
    
    def plot(self):
        if self.plotType == "directions":
            x = ["Up", "Down", "Left", "Right"]
            heights = [self.nUp, self.nDown, self.nLeft, self.nRight]
        
        figure, axes = plt.subplots()
        axes.bar(x, heights)
        axes.set_ylabel("Frequency")
        axes.set_xlabel("Directions")
        axes.set_title("Turtler Directions")
        plt.show()



    
    
    # MAIN

    def goUp(self):
        self.t.seth(0)
        self.t.fd(self.stepSize)
        self.nUp += 1
    
    def goDown(self):
        self.t.seth(180)
        self.t.fd(self.stepSize)
        self.nDown += 1
    
    def goLeft(self):
        self.t.seth(270)
        self.t.fd(self.stepSize)
        self.nLeft += 1
    
    def goRight(self):
        self.t.seth(90)
        self.t.fd(self.stepSize)
        self.nRight += 1

    def path(self, pathString):
        for i in pathString:
            if i == "u":
                self.goUp()
            elif i == "d":
                self.goDown()
            elif i == "l":
                self.goLeft()
            elif i == "r":
                self.goRight()
            else:
                print("Invalid path")
                break
    
    def draw(self, drawString : str):
        self.t.pendown()
        self.path(drawString)
    
    def go(self, goString : str):
        self.t.penup()
        self.path(goString)
        self.t.pendown()

