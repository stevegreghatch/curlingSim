import time
import tkinter
from tkinter import *

# import physics

# curling sheet dimensions:
# total length = 150ft * 10 = 1500px (with 100px buffer, dimensions are 100px to 1600px)
# total width = 15ft * 10 = 150px (with 175px buffer, dimensions are 175px to 325px)

refreshSec = 0.001

window = Tk()

window.geometry('1800x500')
window.title('Curling Sim')

canvas = Canvas(window, width=1800, height=500)

global stone1Y
global stone1R
global stone2Y
global stone3Y
global stone4Y
global stone5Y
global stone6Y
global stone7Y
global stone8Y
global stone2R
global stone3R
global stone4R
global stone5R
global stone6R
global stone7R
global stone8R

currentRockLocations = []
listOfThrownRocks = []

# line parameters: (start x, start y, end x, end y)
# sheet measurements
def displayMeasurements():
    # length
    canvas.create_text(850, 15, text="150ft", font='Times 14')
    canvas.create_line(100, 25, 1600, 25, dash=(4, 2))
    canvas.create_line(100, 25, 100, 175, dash=(4, 2))
    canvas.create_line(1600, 25, 1600, 175, dash=(4, 2))

    # center line
    canvas.create_text(850, 250, text="center line", font='Times 12')
    # vertical
    canvas.create_line(850, 175, 850, 325, dash=(4, 2))
    # horizontal
    canvas.create_line(100, 250, 1600, 250)

    # width
    canvas.create_text(55, 250, text="15ft", font='Times 14')
    canvas.create_line(75, 175, 75, 325, dash=(4, 2))
    canvas.create_line(75, 175, 100, 175, dash=(4, 2))
    canvas.create_line(75, 325, 100, 325, dash=(4, 2))
    canvas.create_text(1645, 250, text="15ft", font='Times 14')
    canvas.create_line(1625, 175, 1625, 325, dash=(4, 2))
    canvas.create_line(1625, 175, 1600, 175, dash=(4, 2))
    canvas.create_line(1625, 325, 1600, 325, dash=(4, 2))

    # tee line to tee line
    canvas.create_text(850, 65, text="114ft", font='Times 14')
    canvas.create_line(280, 75, 1420, 75, dash=(4, 2))
    canvas.create_line(280, 75, 280, 325, dash=(4, 2))
    canvas.create_line(1420, 75, 1420, 325, dash=(4, 2))

    # slide line
    canvas.create_text(385, 115, text="21ft", font='Times 14')
    canvas.create_text(1315, 115, text="21ft", font='Times 14')
    canvas.create_line(280, 125, 490, 125, dash=(4, 2))
    canvas.create_line(490, 120, 490, 175, dash=(4, 2))
    canvas.create_line(1210, 125, 1420, 125, dash=(4, 2))
    canvas.create_line(1210, 120, 1210, 175, dash=(4, 2))

    # main stretch
    canvas.create_text(850, 115, text="72ft", font='Times 14')
    canvas.create_line(490, 125, 1210, 125, dash=(4, 2))

    # tee line to back line
    canvas.create_text(250, 115, text="6ft", font='Times 14')
    canvas.create_line(280, 125, 220, 125, dash=(4, 2))
    canvas.create_line(220, 120, 220, 175, dash=(4, 2))
    canvas.create_text(1450, 115, text="6ft", font='Times 14')
    canvas.create_line(1420, 125, 1480, 125, dash=(4, 2))
    canvas.create_line(1480, 120, 1480, 175, dash=(4, 2))

    # back line to hack
    canvas.create_text(190, 115, text="6ft", font='Times 14')
    canvas.create_line(220, 125, 160, 125, dash=(4, 2))
    canvas.create_line(160, 120, 160, 325, dash=(4, 2))
    canvas.create_text(1510, 115, text="6ft", font='Times 14')
    canvas.create_line(1480, 125, 1540, 125, dash=(4, 2))
    canvas.create_line(1540, 120, 1540, 325, dash=(4, 2))


def displaySheet():
    # top line of sheet
    canvas.create_line(100, 175, 1600, 175)

    # bottom line of sheet
    canvas.create_line(100, 325, 1600, 325)

    # right barrier line of sheet
    canvas.create_line(100, 175, 100, 325)

    # left barrier line of sheet
    canvas.create_line(1600, 175, 1600, 325)

    # slide line (21ft/210px inward from button line
    canvas.create_line(490, 175, 490, 325, width=4, fill='red')
    canvas.create_line(1210, 175, 1210, 325, width=4, fill='red')

    # horizontal center line
    canvas.create_line(158, 250, 1542, 250, fill='lightcoral', width=0)

    # tee line vertical lines
    canvas.create_line(280, 175, 280, 325, fill='lightcoral', width=0)
    canvas.create_line(1420, 175, 1420, 325, fill='lightcoral', width=0)

    # back ine
    canvas.create_line(220, 175, 220, 325, fill='lightcoral', width=0)
    canvas.create_line(1480, 175, 1480, 325, fill='lightcoral', width=0)

    # hacks
    canvas.create_rectangle(158, 240, 162, 248, fill='black')
    canvas.create_rectangle(158, 252, 162, 260, fill='black')
    canvas.create_rectangle(1538, 240, 1542, 248, fill='black')
    canvas.create_rectangle(1538, 252, 1542, 260, fill='black')

    # HOUSE (center points = (280, 250) and (1420, 250)
    # 12 ft outer circles (12ft = diameter = 120px = r = 60px)
    canvas.create_oval(220, 190, 340, 310, fill='blue')
    canvas.create_oval(1360, 190, 1480, 310, fill='blue')
    # 8 ft middle circles (8ft = diameter = 80px = r = 40px)
    canvas.create_oval(240, 210, 320, 290, fill='white')
    canvas.create_oval(1380, 210, 1460, 290, fill='white')
    # 4ft inner circles (4ft = diameter = 40px = r = 20px)
    canvas.create_oval(260, 230, 300, 270, fill='red')
    canvas.create_oval(1400, 230, 1440, 270, fill='red')
    # inner most circle (r = 6in = 0.5ft = 5px)
    canvas.create_oval(275, 245, 285, 255, fill='white')
    canvas.create_oval(1415, 245, 1425, 255, fill='white')


def displayStones(stonePosition):
    # (diameter = 11in = 0.916667ft = 9.16667px)

    if stonePosition == 'left':
        # ON LEFT
        # center
        stone1Y = canvas.create_oval(100, 240.83333, 109.16667, 250, fill='gold')
        stone1R = canvas.create_oval(100, 250, 109.16667, 259.16667, fill='maroon')
        # sides (top)
        stone2Y = canvas.create_oval(100, 175, 109.16667, 184.16667, fill='gold')
        stone3Y = canvas.create_oval(109.16667, 175, 118.33334, 184.16667, fill='gold')
        stone4Y = canvas.create_oval(118.33334, 175, 127.50001, 184.16667, fill='gold')
        stone5Y = canvas.create_oval(127.50001, 175, 136.66668, 184.16667, fill='gold')
        stone6Y = canvas.create_oval(136.66668, 175, 145.83335, 184.16667, fill='gold')
        stone7Y = canvas.create_oval(145.83335, 175, 155.00002, 184.16667, fill='gold')
        stone8Y = canvas.create_oval(155.00002, 175, 164.16669, 184.16667, fill='gold')
        # sides (bottom)
        stone2R = canvas.create_oval(100, 315.83333, 109.16667, 325, fill='maroon')
        stone3R = canvas.create_oval(109.16667, 315.83333, 118.33334, 325, fill='maroon')
        stone4R = canvas.create_oval(118.33334, 315.83333, 127.50001, 325, fill='maroon')
        stone5R = canvas.create_oval(127.50001, 315.83333, 136.66668, 325, fill='maroon')
        stone6R = canvas.create_oval(136.66668, 315.83333, 145.83335, 325, fill='maroon')
        stone7R = canvas.create_oval(145.83335, 315.83333, 155.00002, 325, fill='maroon')
        stone8R = canvas.create_oval(155.00002, 315.83333, 164.16669, 325, fill='maroon')

    elif stonePosition == 'right':
        # ON RIGHT
        # center
        stone1Y = canvas.create_oval(1590.83333, 240.83333, 1600, 250, fill='gold')
        stone1R = canvas.create_oval(1590.83333, 250, 1600, 259.16667, fill='maroon')
        # sides (top)
        stone2Y = canvas.create_oval(1590.83333, 175, 1600, 184.16667, fill='gold')
        stone3Y = canvas.create_oval(1581.66666, 175, 1590.83333, 184.16667, fill='gold')
        stone4Y = canvas.create_oval(1572.49999, 175, 1581.66666, 184.16667, fill='gold')
        stone5Y = canvas.create_oval(1563.33332, 175, 1572.49999, 184.16667, fill='gold')
        stone6Y = canvas.create_oval(1554.16665, 175, 1563.33332, 184.16667, fill='gold')
        stone7Y = canvas.create_oval(1544.99998, 175, 1554.16665, 184.16667, fill='gold')
        stone8Y = canvas.create_oval(1535.83331, 175, 1544.99998, 184.16667, fill='gold')
        # sides (bottom)
        stone2R = canvas.create_oval(1590.83333, 315.83333, 1600, 325, fill='maroon')
        stone3R = canvas.create_oval(1581.66666, 315.83333, 1590.83333, 325, fill='maroon')
        stone4R = canvas.create_oval(1572.49999, 315.83333, 1581.66666, 325, fill='maroon')
        stone5R = canvas.create_oval(1563.33332, 315.83333, 1572.49999, 325, fill='maroon')
        stone6R = canvas.create_oval(1554.16665, 315.83333, 1563.33332, 325, fill='maroon')
        stone7R = canvas.create_oval(1544.99998, 315.83333, 1554.16665, 325, fill='maroon')
        stone8R = canvas.create_oval(1535.83331, 315.83333, 1544.99998, 325, fill='maroon')


# labels
velocityLabel = tkinter.Label(window, text='Velocity:')
velocityLabel.place(x=1245, y=400)
velocityLabel.grid_remove()

options = 'draw', 'takeout', 'guard'
variable = StringVar(window)
variable.set(options[0])

velocityBox = tkinter.OptionMenu(window, variable, 'draw', 'takeout', 'guard')
velocityBox.place(x=1300, y=400)

rotationLabel = tkinter.Label(window, text='Rotation:')
rotationLabel.place(x=1245, y=430)


def getVelocity():
    return variable.get()


def getStone():
    stone = listOfStonesCopy[0]
    return stone


rotationTextBox = tkinter.Text(window, height=1, width=5)
rotationTextBox.place(x=1300, y=430)


def animateShot(stone, xMovement, yMovement):

    currentRockLocations = updateCurrentRockLocations()
    collisionStone = None

    currentPosOfMovingRock = [1700, 0, 0, 0]

    while currentPosOfMovingRock[0] > 275:

        canvas.move(stone, xMovement, yMovement)
        window.update()
        time.sleep(refreshSec)
        currentPosOfMovingRock = canvas.coords(stone)

        print('current position of moving rock: ' + str(currentPosOfMovingRock))
        print('current positions of all thrown rocks:' + str(currentRockLocations))

        # x-axis (right-side) check
        # for i in range(len(currentRockLocations)):
        # if currentPosOfMovingRock[2] <= currentRockLocations[i][2]:
        #  print('rock is same distance X as another rock')

        # y-axis (bottom-side) check
        # for i in range(len(currentRockLocations)):
        # if abs(currentPosOfMovingRock[3] - currentRockLocations[i][3]) < 9.16667:
        # print('rock is same distance Y as another rock')


def sendShot():
    stone = getStone()
    velocity = getVelocity()
    if velocity == 'draw':
        print('need draw velocity')
    print(velocity)
    xMovement = -5
    yMovement = 0
    animateShot(stone, xMovement, yMovement)
    listOfStonesCopy.remove(stone)
    listOfThrownRocks.append(0)
    moveStoneToStartingPosition()
    moveStoneToStartingPositionButton['text'] = 'send next stone'
    moveStoneToStartingPositionButton['command'] = sendShot


def moveStoneToStartingPosition():
    print(listOfStonesCopy)
    if listOfStonesCopy:
        print(listOfStonesCopy[0])
        stone = listOfStonesCopy[0]

        xMovement = 0
        yMovement = 0

        if listOfStones.index(stone) == 0:
            xMovement = -110.83333
            yMovement = 4.583335
        elif listOfStones.index(stone) == 1:
            xMovement = -110.83333
            yMovement = -4.583335
        elif listOfStones.index(stone) == 2:
            xMovement = -110.83333
            yMovement = 70.416665
        elif listOfStones.index(stone) == 3:
            xMovement = -110.83333
            yMovement = -70.416665
        elif listOfStones.index(stone) == 4:
            xMovement = -101.66666
            yMovement = 70.416665
        elif listOfStones.index(stone) == 5:
            xMovement = -101.66666
            yMovement = -70.416665
        elif listOfStones.index(stone) == 6:
            xMovement = -92.49999
            yMovement = 70.416665
        elif listOfStones.index(stone) == 7:
            xMovement = -92.49999
            yMovement = -70.416665
        elif listOfStones.index(stone) == 8:
            xMovement = -83.33332
            yMovement = 70.416665
        elif listOfStones.index(stone) == 9:
            xMovement = -83.33332
            yMovement = -70.416665
        elif listOfStones.index(stone) == 10:
            xMovement = -74.16665
            yMovement = 70.416665
        elif listOfStones.index(stone) == 11:
            xMovement = -74.16665
            yMovement = -70.416665
        elif listOfStones.index(stone) == 12:
            xMovement = -64.99998
            yMovement = 70.416665
        elif listOfStones.index(stone) == 13:
            xMovement = -64.99998
            yMovement = -70.416665
        elif listOfStones.index(stone) == 14:
            xMovement = -55.83331
            yMovement = 70.416665
        elif listOfStones.index(stone) == 15:
            xMovement = -55.83331
            yMovement = -70.416665

        canvas.move(stone, xMovement, yMovement)

        moveStoneToStartingPositionButton['text'] = 'send stone'
        moveStoneToStartingPositionButton['command'] = sendShot
    else:
        print('all stones have been thrown')


# buttons
moveStoneToStartingPositionButton = tkinter.Button(window, text='set stone to throw position',
                                                   command=moveStoneToStartingPosition)
moveStoneToStartingPositionButton.place(x=1500, y=450)


def updateCurrentRockLocations():
    for i in range(len(listOfThrownRocks)):
        currentLocation = canvas.coords(listOfStones[i])
        currentRockLocations.append(currentLocation)
    # print(currentRockLocations)
    return currentRockLocations

# ----------------------------------------------------------------------------------------------------------------

displayMeasurements()
displaySheet()
displayStones('right')

listOfStones = [stone1Y, stone1R, stone2Y, stone2R, stone3Y, stone3R, stone4Y, stone4R, stone5Y, stone5R, stone6Y,
                stone6R, stone7Y, stone7R, stone8Y, stone8R]
listOfStonesCopy = listOfStones.copy()

launchWindow()
