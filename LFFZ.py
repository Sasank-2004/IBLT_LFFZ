import mmh3 #Murmur3 Hash function.
import csv
import time
import numpy as np

############Global Variables

############IBLT Variables
keySum = ["0".zfill(36)] ##IBLT Variable
count = [0] ##IBLT Variable
valueSum = [0] ##IBLT Variable
mapping_matrix = [] ## Mapping matrix to find hash indices
universeSize = 1000

############functional variables
extractedValues = [] ##contains the extraced / decoded elements from the IBLT
inputList = [] ##contains the list of input elements read from the dataset
maliciousItems = [] ##contains the malicious items

############UTILITY FUNCTIONS############
####################################

###########Function to XOR Two strings
def xor_strings(str1, str2):
    result = hex(int(str1, 16) ^ int(str2, 16))[2:].zfill(36)
    return result


############Check purecell count############
def checkPurecell(sizeIBLT):
    global count
    purecells= count.count(1)
    # print("Purecell count = {}".format(purecells)) 
    return purecells
    # for i in range(0,sizeIBLT):
    #     if count[i] == 1:
    #         purecells=purecells+1
        # print("{} = {}".format(keySum[i],count[i]))

    
############IBLT FUNCTONS############
#####################################

############Function to perform SingleDecode#############
def singleDecode(sizeIBLT):
    # print("inside singleDecode")
    global count
    global keySum
    global extractedValues

    while checkPurecell(sizeIBLT) > 0:
        for i in range(sizeIBLT):
            if count[i] == 1:
                key = keySum[i]
                extractedValues.append(str(key))
                column = int(abs(mmh3.hash(key))) % universeSize
                hashIndices = np.where(mapping_matrix[:, column] == 1)[0]
                for j in hashIndices:
                    keySum[j] = xor_strings(keySum[j],key)
                    count[j] -= 1
    
############Function to insert an element into the IBLT#############
def insertIBLT(key):
    # print("inside insertIBLT")
    global keySum
    global count

    column = int(abs(mmh3.hash(key))) % universeSize
    hashIndices = np.where(mapping_matrix[:, column] == 1)[0]
    
    for i in hashIndices:
        keySum[i] = xor_strings(keySum[i],key)
        count[i] += 1
    
    
############Function to create the IBLT#############
def createIBLT(sizeIBLT):
    # print("inside Create IBLT")
    
    #######IBLT Created
    global keySum
    global count
    global valueSum
    keySum = ["0".zfill(42)] * sizeIBLT
    count = [0] * sizeIBLT
    valueSum = [0] * sizeIBLT

def read_mapping_matrix(filename):
    global mapping_matrix
    global sizeIBLT
    global universeSize

    matrix = []
    # Read the CSV file
    with open(filename, newline='') as csvfile:
        csvreader = csv.reader(csvfile)
        for row in csvreader:
            # Convert each row to a list of integers and add it to the matrix
            matrix.append([float(value) for value in row])

    mapping_matrix = np.array(matrix)
    sizeIBLT = len(mapping_matrix)
    universeSize = len(mapping_matrix[0])

####################################################################
####################################################################
############MAIN FLOW OF OF THE PROGRAM#############################
####################################################################
####################################################################

dataset = "Listguard/txtDataset/_00000_20180315130100.txt"
csv_file = "matrix_1000_30.csv"

read_mapping_matrix(csv_file)
createIBLT(sizeIBLT)

##reading elements from the dataset
with open(dataset, 'r') as file:
    #First we read the elements and then we insert
    cnt = 0
    for line in file:
        val = line.strip() #Print each line after stripping newline characters. The type is string
        inputList.append(val) #add the dataset to an in memory list
        cnt += 1
        if cnt >= 1000: break

############Insert Items into the IBLT
cnt = 0
for key in inputList:
    insertIBLT(key)
    if checkPurecell(sizeIBLT) != 0: cnt += 1

print(f'No.of input flows : {len(inputList)}')

start = time.time()
############Perfrom SingleDecode process
singleDecode(sizeIBLT)
end = time.time()

print(f'No.of Extracted values : {len(extractedValues)} ')
print(f'Time taken to decode : {end-start}')