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
    # Check if there is a group for it , if not add it
    if ones not in groupsIndices:
        groupsIndices.append(ones)
groupsIndices.sort()
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
print("\nGroups:")
for i in range(len(groups)):
    print("Group", groupsIndices[i], groups[i])

for i in range(len(stages))[1:]:
    print("\nStage", i, ":")
    for g in stages[i]:
        print(g)

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

print("\nPrime Implicants:")
print(PI)
convertVariables(PI)

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
print("\nPrime implicant Chart:")
if variableCount<4: print("Col", minterms)
elif variableCount==4: print("Col","", minterms)
else : print("col"," "*(variableCount-4),minterms)
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
print("Essential Prime implicants after step1:", essentialPI)
convertVariables(essentialPI)

# REMOVE ESSENTIAL PI ROWS AND COLUMNS AND MAKE A NEW MNIMIZED CHART
chartMinterms = minterms
# check if there is any essential prime implicant
if len(essentialPI) == 0:
    finished = False
# check if all prime implicants are essential
elif len(essentialPI) == len(PI):
    finished = True
    print("All prime implicants are essential")
    result = essentialPI
    
# otherwise remove rows and columns
else:
    for e in range(len(essentialPI)):
        c = 0
        # LOOP OVER EACH COLUMN
        while c <= columnLength - 1:
            if piChart[essentialPI_indices[e] - e][c] == 1:
                for r in range(len(PI)):
                    piChart[r] = piChart[r][:c] + piChart[r][c + 1:]
                chartMinterms = chartMinterms[:c] + chartMinterms[c + 1:]
                columnLength -= 1
            else:
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
            if variableCount<4: print("Col", chartMinterms)
            elif variableCount==4: print("Col","", chartMinterms)
            else : print("col"," "*(variableCount-4), chartMinterms)
            for r in range(len(piChart)):
                print(PI[r], piChart[r])
    if finished:
        convertVariables(result)
    else:
    # MINIMIZE THE CHART AFTER REMOVING THE ESSENTIAL PRIME IMPLICANTS
    #PRINT PI ASSIGNMENTS
        print()
        for i in range (len(PI)):
            print(PI[i],str(i))
        print()

    #GET PETRIKS METHODE ARRAY : (a+b)(b+c) is equivalent to [ab,bc]
        pet1 = ['']*columnLength
        for i in range (columnLength):
            for j in range(rowLength):
                if piChart[j][i] == 1:
                    pet1[i] += str(j)

    #GET TERM OF HIGHEST LENGTH IN PETRIKS ARRRAY
        highLTerm = ''
        for i in range (columnLength):
            if len(pet1[i])>len(highLTerm):
                highLTerm = pet1[i]
                highLTermIndex = i
                
    #REPLACE IT WITH FIRST ELEMENT IN ARRAY
        temp = pet1[0]
        pet1[0] = highLTerm
        pet1[highLTermIndex] = temp

    #PRINT ARRAY
        print ('F = ',end=' ')
        for i in range (len(pet1)):
            print ('(',end=' ')
            for j in range (len(pet1[i])):
                print (pet1[i][j],end=' ')
                if j != len(pet1[i])-1:
                    print ('+',end=' ')
            print (')',end=' ')
        print()

    #MAKE AN ARRAY FOR PERMUTATIONS OF HIGHEST LENGTH TERM
        highLTermPermutations = []
        for i in range (len(highLTerm)):
            temp2 = highLTerm[0]
            highLTerm = highLTerm.lstrip(temp2) + temp2
            highLTermPermutations.append(highLTerm)
            
    #SIMPLIFYING BY BITWISE OPERATIONS : (a+b)(b+c) = (b+ac) is equivalent to [ab,bc] = [b,ac]
        pet2 = []

        #MAKE A COPY FOR PETRICK ARRAY TO MAKE OPERATIONS ON IT
        pet1x = pet1.copy()

        #PERMUTE FIRST TERM
        for pet1x[0] in highLTermPermutations:
            curPet2=[]
            removedPairs=0
            #CODE OF EACH PERMUTAION 
            while len(pet1x) > 1:
                    #SECOND TO LAST TERMS VALUES
                    for comparedTerm in range (1,len(pet1x)):
                        if pet1x==[]:
                            break
                        if removedPairs !=0 :
                            comparedTerm = 1
                        combinations = 0
                        simplify = 0
                        #MINTERMS VALUES OF FIRST TERM
                        for minterm1 in range (len(pet1x[0])):
                            if pet1x==[] or simplify == 1:
                                break
                            if removedPairs == 0:
                                minterm1 = 0
                            comparedMinterm = 0
                            #MINTERM VALUES OF SENCOND TO LAST TERMS
                            while len(pet1x[0])>1 and comparedMinterm < len(pet1x[comparedTerm]):
                                #COMBINATION DETECTOR
                                if pet1x[0][minterm1] == pet1x[comparedTerm][comparedMinterm]:
                                    simplify = 1
                                    if (combinations == 0):
                                        curPet2.append(list())
                                        curPet2[removedPairs].append(pet1x[0][minterm1])
                                    else:
                                        curPet2[removedPairs][0] = curPet2[removedPairs][0] + pet1x[0][minterm1]
                                    pet1x[0] = pet1x[0].replace(pet1x[0][minterm1],'')
                                    pet1x[comparedTerm] = pet1x[comparedTerm].replace(pet1x[comparedTerm][comparedMinterm],'')
                                    combinations += 1
                                comparedMinterm += 1
                            #SAVING COMBINATION
                            if simplify:
                                curPet2[removedPairs].append(pet1x[0])
                                curPet2[removedPairs][1] = curPet2[removedPairs][1] + pet1x[comparedTerm]
                                pet1x.remove(pet1x[0])
                                pet1x.remove(pet1x[comparedTerm-1])
                                removedPairs += 1
                                continue
                        #SAVING LAST 2 UNCOMBINED TERMS
                        if len(pet1x)==2 and combinations == 0:
                            curPet2.append(list(set(pet1x[0])))
                            curPet2.append(list(set(pet1x[1])))
                            pet1x.remove(pet1x[0])
                            pet1x.remove(pet1x[0])
                        #SAVING LAST COMBINED TERM
                        elif len(pet1x)==1:
                            curPet2.append(list(set(pet1x[0])))
                            pet1x.remove(pet1x[0])
                        
            #SAVING EACH PERMUTATION
            pet2.append(curPet2)
            pet1x = pet1.copy()
            
        #CHOOSING PERMUTATION WITH HIGHEST NUMBER OF COMBINATIONS
        pet2OriginalIndex = 0
        pet2Original = []
        for i in range (len(pet2)-1):
            if len(pet2Original)<len(pet2[i]):
                pet2Original = pet2[i]
        print (pet2Original)        
        #PETRICK ARRAY UPDATE
        print ('F = ',end=' ')
        for i in range (len(pet2Original)):
            print ('(',end=' ')
            for j in range (len(pet2Original[i])):
                print (pet2Original[i][j],end=' ')
                if j != len(pet2Original[i])-1:
                    print ('+',end=' ')
            print (')',end=' ')
        print()

        #DISTRIBUTE (a+bc)(d+be)=ad+bcd+abe+bcbe is equivalent to [[a,bc],[d,be]]=[ad,bcd,abe,bcbe]
        pet3 = pet2Original.copy()
        pet3Temp =[]
        k=0
        for posTerm in range (len(pet3)-1):
            for i in range (len(pet3[0])):
                for j in range (len(pet3[1])):
                    pet3Temp.append(pet3[0][i] + pet3[1][j])
            pet3[0:2] = pet3Temp.copy()
            
        #OMMIT SIMILAR LETTERS IN SAME TERM bcbe = bce
        for i in range (len(pet3)):
            pet3[i] = "".join(set(pet3[i]))
            
        #PRINT UPDATED ARRAY
        print ('F = ',end=' ')
        for i in range (len(pet3)):
            print (pet3[i],end=' ')
            if i != len(pet3)-1:
                print ('+',end=' ')
        print()

        #CHOOSE THE TERM OF LOWEST COST (LENGTH)
        remainingEssentials = '11111111111'
        for i in range (len(pet3)):
            if len(remainingEssentials)>len(pet3[i]):
                remainingEssentials = pet3[i]
        remainingEssentials = set(remainingEssentials)

        #ADD NEW ESSENTIALS TO OUR ESSENTIALS ARRAY AND PRINT THEM
        result1=[]
        for i in (remainingEssentials):
            result.append(PI[int(i)])
            result1.append(PI[int(i)])
            
        print("\nRest of Essentials: ")
        convertVariables(result1)
            
        # PRINT FINAL RESULTS
        print("\nFinal Result: ")
        convertVariables(result)
