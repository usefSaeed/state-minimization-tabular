print("Enter the minterms: \nLeave a space between every minterm. (ex: 2 4 6 5)")
minterms = [int(x) for x in input().split()]  # turn the input into a list
variableCount = int(input("Number of variables: "))
minterms.sort()  # sort the list incase its not sorted

# Make a new minterms list in terms of binary
binaryEq = []
for i in minterms:
    binaryEq.append(bin(i)[2:].zfill(variableCount))

# Make the groups
# Step 1
groupsIndices = []
for x in binaryEq:
    # count the one's
    ones = 0
    for y in x:
        if y == '1':
            ones += 1
    # Check if there is a group for it , if not add it and then sort the list
    if ones not in groupsIndices:
        groupsIndices.append(ones)
        groupsIndices.sort()
print(groupsIndices)

# Step 2
# Make groups list the size of the groups indices
groups = [[] for i in range(len(groupsIndices))]
tickList = [[] for i in range(len(groupsIndices))]
PI = []  # PRIME IMPLICANT
currentGroupIndex = 0
# Fill the grouplist
for x in binaryEq:
    # Get the number of ones the minterm has
    ones = 0
    for y in x:
        if y == '1':
            ones += 1
    currentGroupIndex = groupsIndices.index(ones)
    groups[currentGroupIndex].append(x)
    tickList[currentGroupIndex].append(False)

# FIND THE PRIME IMPLICANTS
stages = [groups]
tickList = [tickList]
highestStage = 0

while True:
    curStage = []
    stageTick = []
    done = True
    for groupI in range(len(stages[highestStage])):
        greatestGroup = 0
        for mintermI in range(len(stages[highestStage][groupI])):
            if groupI + 1 <= len(stages[highestStage]) - 1:
                for mintermComparedI in range(len(stages[highestStage][groupI + 1])):
                    # Pair the 2 minterms with only 1 bit different
                    similarBits = 0
                    for bitIndex in range(len(stages[highestStage][groupI + 1][mintermComparedI])):
                        if stages[highestStage][groupI][mintermI][bitIndex] == \
                                stages[highestStage][groupI + 1][mintermComparedI][bitIndex]:
                            similarBits += 1
                    # Check if they are a pair
                    if similarBits == (variableCount - 1):
                        # Find the different bit again
                        for bitIndex in range(len(stages[highestStage][groupI + 1][mintermComparedI])):
                            if stages[highestStage][groupI][mintermI][bitIndex] != \
                                    stages[highestStage][groupI + 1][mintermComparedI][bitIndex]:
                                # Replace it with '-'
                                temp = stages[highestStage][groupI][mintermI][0:bitIndex] + '-' + \
                                       stages[highestStage][groupI][mintermI][bitIndex + 1:]
                                # UPDATE THE TICK LIST
                                tickList[highestStage][groupI][mintermI] = \
                                    tickList[highestStage][groupI + 1][mintermComparedI] = True
                                # DIVIDE IT AND INSERT IT
                                bits = 0
                                for y in temp:
                                    if y == '1' or y == '-':
                                        bits += 1
                                if bits == greatestGroup:
                                    if temp not in curStage[-1]:
                                        done = False
                                        curStage[-1].append(temp)
                                        stageTick[-1].append(False)
                                elif bits > greatestGroup:
                                    done = False
                                    greatestGroup = bits
                                    curStage.append(list())
                                    curStage[-1].append(temp)
                                    # EXTEND THE TICK LIST
                                    stageTick.append(list())
                                    stageTick[-1].append(False)
            else:
                break
    if done:
        break
    else:
        highestStage += 1
        stages.append(curStage)
        tickList.append(stageTick)

# SEARCH FOR UN-TICKED MINTERMS
for x in range(len(tickList)):
    for y in range(len(tickList[x])):
        for z in range(len(tickList[x][y])):
            if not tickList[x][y][z]:
                PI.append(stages[x][y][z])

# PRINT THE RESULTS
print("Groups:")
for i in range(len(groups)):
    print(groups[i])

for i in range(len(stages))[1:]:
    print("Stage", i, ":")
    print(stages[i])

# FUNCTION TO CONVERT BINARY INTO LITERALS
def convertVariables(binaryList):
    variables = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J']
    literals = []
    for binarytermI in binaryList:
        term = ""
        for variableIndex in range(len(binarytermI)):
            if binarytermI[variableIndex] == '-':
                continue
            elif binarytermI[variableIndex] == '1':
                term += variables[variableIndex]
            elif binarytermI[variableIndex] == '0':
                term = term + variables[variableIndex] + "'"
        term.strip('"\'')
        literals.append(term)
    print(*literals, sep=' + ')

# print(stages)
# print(tickList)
print("Prime Implicants:")
print(PI)
convertVariables(PI)
print("")

#######################
# PRIME IMPlICANT CHART
#######################

columnLength = len(minterms)
rowLength = len(PI)
# INTIALIZE THE CHART
piChart = [[0 for c in range(columnLength)] for r in range(rowLength)]

# FILL THE CHART
for row in range(rowLength):
    for column in range(columnLength):
        differentBits = 0
        for bit in range(len(PI[row])):
            if PI[row][bit] == '-':
                continue
            else:
                if PI[row][bit] == binaryEq[column][bit]:
                    continue
                else:
                    differentBits += 1
        if differentBits == 0:
            piChart[row][column] = 1

# PRINT THE CHART
print("Prime implicant Chart:")
print("Col", minterms)
for r in range(rowLength):
    print(PI[r], piChart[r])
print()

# MINIMIZE THE CHART
result = []
# FIND ESSENTIAL PRIME IMPLICANTS
essentialPI = []
essentialPI_indices = []

for column in range(columnLength):
    appearances = 0
    lastRowAppearance = 0
    for Row in range(rowLength):
        if piChart[Row][column] == 1:
            appearances += 1
            lastRowAppearance = Row
    if appearances == 1:
        if PI[lastRowAppearance] not in essentialPI:
            essentialPI.append(PI[lastRowAppearance])
            essentialPI_indices.append(lastRowAppearance)

essentialPI_indices.sort()
print("Essential Prime implicants :", essentialPI)
convertVariables(essentialPI)

# REMOVE ESSENTIAL PI ROWS AND COLUMNS AND MAKE A NEW MNIMIZED CHART
chartMinterms = minterms
# CHECK IF THERE IS ESSENTIAL PRIME IMPLICANTS
if len(essentialPI) == 0:
    finished = False
else:
    for e in range(len(essentialPI)):
        c = 0
        colRemoved = 0
        while c <= columnLength:
            if piChart[essentialPI_indices[e] - e][c - colRemoved] == 1:
                for r in range(rowLength):
                    piChart[r] = piChart[r][:c - colRemoved] + piChart[r][c - colRemoved + 1:]
                chartMinterms = chartMinterms[:c - colRemoved] + chartMinterms[c - colRemoved + 1:]
                columnLength -= 1
                colRemoved += 1
            c += 1
        piChart.remove(piChart[essentialPI_indices[e] - e])
        PI.remove(PI[essentialPI_indices[e] - e])
        result.append(essentialPI[e])
        rowLength -= 1

        # CHECK IF THERE IS NO X"S
        if piChart == []:
            chartMinterms = []
            finished = True
        # PRINT UPDATES
        else:
            finished = False
            print()
            print("Col", chartMinterms)
            for r in range(len(piChart)):
                print(PI[r], piChart[r])

# MINIMIZE THE CHART AFTER REMOVING THE ESSENTIAL PRIME IMPLICANTS
# INFINE LOOP
while not finished:
    highestXs = 0
    highestXsI = 0

    # FIND THE TERM THAT WOULD REMOVE THE MOST X'S
    for r in range(len(piChart)):
        sum = 0
        for c in range(len(chartMinterms)):
            if piChart[r][c] == 1:
                # find what else does it remove
                for row in range(len(piChart)):
                    if piChart[row][c] == 1:
                        sum += 1
            else:
                continue
        if sum > highestXs:
            highestXs = sum
            highestXsI = r
    # HOLD THE VALUE OF TERM TO PRINT IT (BECAUSE ITS REMOVED LATER)
    holder = [PI[highestXsI]]

    # BREAK THE INFINITE LOOP WHEN X'S NO LONGER EXIST IN THE CHART
    if highestXs == 0:
        print("Done")
        break

    # REMOVE THE TERM THAT REMOVES THE MOST THE MOST X'S
    c = 0
    colRemoved = 0
    while c <= columnLength:
        if piChart[highestXsI][c - colRemoved] == 1:
            for r in range(len(PI)):
                piChart[r] = piChart[r][:c - colRemoved] + piChart[r][c - colRemoved + 1:]
            chartMinterms = chartMinterms[:c - colRemoved] + chartMinterms[c - colRemoved + 1:]
            columnLength -= 1
            colRemoved += 1
        c += 1
    result.append(PI[highestXsI])
    piChart.remove(piChart[highestXsI])
    PI.remove(PI[highestXsI])

    # PRINT UPDATES
    print()
    print("Col", chartMinterms)
    for r in range(len(piChart)):
        print(PI[r], piChart[r])
    print("Added term: ")
    convertVariables(holder)
    print("F = ")
    convertVariables(result)

# PRINT FINAL RESULTS
print("\nFinal Result: ")
convertVariables(result)
