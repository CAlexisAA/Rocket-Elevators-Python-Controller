elevatorID = 1
floorRequestButtonID = 1
callButtonID = 1

class Column:
    def __init__(self, _id, _amountOfFloors, _amountOfElevators):
        self.ID = _id
        self.status = 'active'
        self.elevatorList = []
        self.callButtonList = []
        self.amountOfFloors = _amountOfFloors
        self.amountOfElevators = _amountOfElevators       
        self.createElevators(_amountOfFloors, _amountOfElevators)
        self.createCallButtons(_amountOfFloors)

    def createCallButtons(self, _amountOfFloors):
        buttonFloor = 1
        global callButtonID
        
        for i in range(0, _amountOfFloors):
            if buttonFloor < _amountOfFloors:
                callButton = CallButton(callButtonID, buttonFloor, 'Up')
                self.callButtonList.append(callButton)
                callButtonID += 1

            if buttonFloor > 1 :
                callButton = CallButton(callButtonID, buttonFloor, 'Down')
                self.callButtonList.append(callButton)
                callButtonID += 1

            buttonFloor += 1

    def createElevators(self, _amountOfFloors, _amountOfElevators):
        global elevatorID
       
        for i in range(_amountOfElevators):
            global elevatorID
            elevator = Elevator(elevatorID, _amountOfFloors)
            self.elevatorList.append(elevator)
            elevatorID += 1

    def requestElevator(self, floor, direction):
        elevator = self.findElevator(floor, direction)
        elevator.floorRequestList.append(floor)
        elevator.move()
        elevator.operateDoors()
        return elevator

    def findElevator(self, requestedFloor, requestedDirection):
        bestElevator = None
        bestScore = 5
        referenceGap = 10000000
        bestElevatorInformations = {
            "bestScore": None,
            "bestElevator": None,
            "referenceGap": None,
            }

        for elevator in self.elevatorList:

            if requestedFloor == elevator.currentFloor and elevator.status == 'stopped' and requestedDirection == elevator.direction:
                bestElevatorInformations = self.checkIfElevatorIsBetter(1, elevator, bestScore, referenceGap, bestElevator, requestedFloor)
            elif requestedFloor > elevator.currentFloor and elevator.direction == 'up' and requestedDirection == elevator.direction:
                bestElevatorInformations = self.checkIfElevatorIsBetter(2, elevator, bestScore, referenceGap, bestElevator, requestedFloor)
            elif requestedFloor < elevator.currentFloor and elevator.direction == 'down' and requestedDirection == elevator.direction:
                bestElevatorInformations = self.checkIfElevatorIsBetter(2, elevator, bestScore, referenceGap, bestElevator, requestedFloor)
            elif elevator.status == 'idle':
                bestElevatorInformations = self.checkIfElevatorIsBetter(3, elevator, bestScore, referenceGap, bestElevator, requestedFloor)
            else:
                bestElevatorInformations = self.checkIfElevatorIsBetter(4, elevator, bestScore, referenceGap, bestElevator, requestedFloor)

            bestElevator = bestElevatorInformations["bestElevator"]
            bestScore = bestElevatorInformations["bestScore"]
            referenceGap = bestElevatorInformations["referenceGap"]
        return bestElevator

    def checkIfElevatorIsBetter(self, scoreToCheck, newElevator, bestScore, referenceGap, bestElevator, floor):
        if scoreToCheck < bestScore:
            bestScore = scoreToCheck
            bestElevator = newElevator
            referenceGap = abs(newElevator.currentFloor - floor)
        elif bestScore == scoreToCheck:
            gap = abs(newElevator.currentFloor - floor)
        
            if referenceGap > gap:
                bestElevator = newElevator
                referenceGap = gap
            
        return {
            "bestScore": bestScore,
            "bestElevator": bestElevator,
            "referenceGap": referenceGap
            }

        

class Elevator:
    def __init__(self, _id, _amountOfFloors,):
        self.ID = _id
        self.status = 'idle'
        self.currentFloor = 1
        self.direction = None
        self.door = Door(_id)
        self.floorRequestButtonList = []
        self.floorRequestList = []
        
        self.createFloorRequestButtons(_amountOfFloors)

    def createFloorRequestButtons(self, _amountOfFloors):
        buttonFloor = 1
        for i in range(0, _amountOfFloors):
            floorRequestButton = FloorRequestButton(i, buttonFloor) # put params
            self.floorRequestButtonList.append(floorRequestButton)
            
            buttonFloor += 1

    def requestFloor(self, requestedFloor):
        self.floorRequestList.append(requestedFloor)
        self.move()
        self.operateDoors()

    def move(self):
        while len(self.floorRequestList) != 0:
            destination = self.floorRequestList[0]
            self.status = 'moving'
            if self.currentFloor < destination:
                self.direction = 'up'
                self.sortFloorList()
            elif self.currentFloor > destination:
                self.direction = 'down'
                self.sortFloorList()
                while self.currentFloor < destination:
                    self.currentFloor += 1
                while self.currentFloor > destination:
                    self.currentFloor -=1
        
            self.status = 'stopped'
            self.floorRequestList.pop(0)
            self.status = 'idle'

    def sortFloorList(self):
        if self.direction == 'up':
            self.floorRequestList.sort(reverse = False) #ASCENDING
        else:
            self.floorRequestList.sort(reverse = True) #DESCENDING

    def operateDoors(self):
        if self.door.status == 'opened':
            self.door.status == 'closed'
        elif self.door.status == 'opened':
            self.door.status == 'closed'


class CallButton:
    def __init__(self, _id, _floor, _direction):
        self.ID = _id
        self.floor = _floor
        self.direction = None
        self.status = 'active'


class FloorRequestButton:
    def __init__(self, _id, _floor):
        self.ID = _id
        self.floor = _floor
        self.status = "active"


class Door:
    def __init__(self, _id):
        self.ID = _id
        self.status = 'active'
