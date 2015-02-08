# #
# #
# #  To use this filter, type the desired "header fields"
# #  in the "ExtractValues" array OR type the desired 
# #  column numberin the "ExtractColumns" array and 
# #  the code will do the rest! (Default: "ExtractValues")
# #
# #  -Seth Chase 11/22/08
# #
# #

ExtractValues = ["EV", "Type", "E1", "Y3"]
ExtractColumns = []  # [0,4,5,11]

# #
# #

ExtractedData = []
tempData = []

# #This part finds all simulation files in current directory with cleanResults.py
import os
batchFiles = []
dirContents = []
workingDir = os.getcwd()
dirContents = os.listdir(workingDir)
for i, item in enumerate(dirContents):
    if "Sim" in item:
        batchFiles.append(dirContents[i])
for j, item in enumerate(dirContents):        
    if "MIN_Sim" in item:
        batchFiles.remove(dirContents[j])
batchFiles.sort()
loop = len(batchFiles)

for t in range(0, loop):
    filename = batchFiles[t]
    filename = filename.rstrip(".rtf")
    filename = filename.rstrip(".txt")
    filename = "MIN_" + filename + ".txt"
    fin = open(batchFiles[t], 'r')
    print "File to cut from ", batchFiles[t]
    data = fin.readlines()
    end = len(data)
    finished = False
    for i in range(0, end):
        str = data[i]
        for value in str.split():
            # print value
            if value == "zip01":
                dirtySpot = value
                finished = True;
                break
        if finished == True:
            dirtyLine = i
            break
    fin.close()
    
# # Delete "zip01" at beginning
    try:
        del data[0:dirtyLine + 1]
    except NameError:
        data = data

# # Extract Column number from values given above
    headerRow = data[0]
    allcolumns = headerRow.split()
    endcolumn = len(allcolumns)      
    totalExtract = len(ExtractValues)
    if totalExtract != 0:
        ExtractColumns = []
        for points in range(0, totalExtract):
            for headers in range(0, endcolumn):
                if allcolumns[headers] == ExtractValues[points]:
                    ExtractColumns.append(headers)
    if totalExtract == 0:
        totalExtract = len(ExtractColumns)
        if totalExtract == 0:
            print "No values or columns selected!"

# # Delete header row at beginning
    if allcolumns[0] == 'EV':
        try:
            del data[0:1]
        except NameError:
            data = data

    fmin = open(filename, "w")
    endline = len(data)
    foundColumnNum = False
    for line in range(0, endline):
        row = data[line]
        allcolumns = row.split()
        endcolumn = len(allcolumns)                           
        for i in range(0, totalExtract):
            dataColumn = ExtractColumns[i]
            x = allcolumns[dataColumn]
            tempData.append(x)
        ExtractedData.append(tempData)
        tempData = []
        
    for i in range(0, endline):
        for j in range(0, totalExtract):
            tempData.append(ExtractedData[i][j])
        for k in range(0, totalExtract - 1):
            tempData.insert(2 * k + 1, '\t')
        fmin.writelines(tempData)
        fmin.writelines('\n')
        tempData = []
        
    ExtractedData = []
    # print ExtractColumns
    fmin.close()
    data = []
    print "Created the file ", filename, " !!"
    # print ExtractedData[2][1]
    # print ExtractedData[2][0]

print "ALL DONE!!"

