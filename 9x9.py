import copy

class Node:
    """A node in a search tree. Contains a pointer to the parent (the node
    that this is a successor of) and to the actual state for this node. Note
    that if a state is arrived at by two paths, then there are two nodes with
    the same state.  Also includes the action that got us to this state"""

    #parent = None
    #child = []      #Ill not keep track of this since it's not needed for the problem and will use less memory.
    lines = []

head = None
actS = None
queue = []

nodes = 0

blockSizeH = 3
#horizontal size of the block, 
blockSizeV = 3
#vertical size of the block, change to 2 for 6x6
elementsAva = 9 +1 #number of elements plus one, change to 6 +1 for 6x6 sudoku
complete = False

def readInput():
    global head
    global actS
    lines2 = []
    firstLine = input()
    lines2.append(list(firstLine))
    for x in range(1, len(firstLine)):
        lines2.append(list(input()))
    #lines.append(lines2)
    act = Node()

    act.lines = lines2
    head = act
    actS = head

def setDefaultSdk():
    global head
    global actS
    act = Node()

    act.lines =  [["", "", "", "8", "4", "", "6", "5", ""],
                  ["", "8", "", "", "", "", "", "", "9"],
		["", "", "", "", "", "5", "2", "", "1"],
		["", "3", "4", "", "7", "", "5", "", "6"],
		["", "6", "", "2", "5", "1", "", "3", ""],
		["5", "", "9", "", "6", "", "7", "2", ""],
		["1", "", "8", "5", "", "", "", "", ""],
		["6", "", "", "", "", "", "", "4", ""],
		["", "5", "2", "", "8", "6", "", "", ""]]
#change the sudoku here, remove elements and rows to 6x6
    head = act
    actS = head


def verifyRow(row, act):
    itemsFound = []
    for x in act.lines[row]:
        if x == "":
            continue
        elif x in itemsFound:
            return False
        else:
            itemsFound.append(x)
    return True



def verifyCol(col, act):
    itemsFound = []
    for y in act.lines:
        x = y[col]
        if x == "":
            continue
        elif x in itemsFound:
            return False
        else:
            itemsFound.append(x)
    return True



def verifyBlock(blk, act):
    itemsFound = []

    blockStartPosH = (blk % int(len(act.lines)/blockSizeH)) * blockSizeH
    blockStartPosV = blk - (blk % (blockSizeV))
    maxH = blockStartPosH+(blockSizeH)
    maxV = blockStartPosV+(blockSizeV)
    for x in range(blockStartPosH,maxH):
        for y in range(blockStartPosV, maxV):
            num = act.lines[y][x]

            if num == "":
                continue
            elif num in itemsFound:
                return False
            else:
                itemsFound.append(num)

    return True





def printSdk(act):
    global head
    global actS
    for x in act.lines:
        print (x)


def verifyBasedOnAdd(act, posX, posY):

    global blockSizeH
    global blockSizeV

    lenRows = len(act.lines)
    lenCols = len(act.lines[0])
    total = int((lenCols/blockSizeH)*(lenRows/blockSizeV))

    if not verifyRow(posX, act):
        return False

    if not verifyCol(posY, act):
        return False

    onX = int(posX/int(lenCols/blockSizeH))*int(lenCols/blockSizeH)
    onY = int(posY/int(lenRows/blockSizeV))
    block = onY+onX

    if not verifyBlock(block, act):
        return False
    return True

def verifyAll(act):

    global blockSizeH
    global blockSizeV

    lenRows = len(act.lines)
    lenCols = len(act.lines[0])
    total = int((lenCols/blockSizeH)*(lenRows/blockSizeV))

    for x in range(0, lenRows):
        if not verifyRow(x, act):
            return False
    for x in range(0, lenCols):
        if not verifyCol(x, act):
            return False


    for x in range(0, total):
        if not verifyBlock(x, act):
            return False
    return True

def verifyComplete(act):
    maxH = len(act.lines)-1
    maxV = len(act.lines[0])-1
    for x in range(maxH, -1 ,-1):
#start from the end for performance
        for y in range(maxV, -1, -1):
            if act.lines[x][y] == "":
                return False
    return True



def genChild(act):
    global actS
    global complete
    global nodes
    for x in range(0, len(act.lines)):
        for y in range(0, len(act.lines[0])):
            if act.lines[x][y] == "":
                for lastElem in range(1,(elementsAva)):
                    newNode = copy.deepcopy(act)
                    newNode.lines[x][y] = str(lastElem)
                    lastElem += 1
                    if verifyBasedOnAdd(newNode,x,y):
                        queue.append(newNode)
                        nodes += 1
                        if verifyComplete(newNode):
                            actS = newNode
                            complete = True
                return




def visitNodes(act):
    genChild(act)



setDefaultSdk()
printSdk(actS)
print(verifyBlock(5, actS))
print(verifyAll(actS))

#print(verifyBasedOnAdd(actS, 8,6))

import time

start = time.time()

genChild(actS)

while not complete:
    genChild(queue[0])
    queue.pop(0)

end = time.time()


#print (verifyAll(actS))
printSdk(actS)
print  ("\033[91mElapsed Time " + str(end - start)+'\033[0m')
print ("nodes: " + str(nodes) )
