from chimerax.core.commands import run
import os
"""
This file contains code to produce 2 tables. 
One is to view Rosetta energy scores for the entire protein.
The other is to view individual Rosetta scores for a each residue.
"""

def getLabelsAndWeights(fileName):
    #open the file
    with open(fileName) as f:
        lines = f.readlines()
        #i is the index of the line in the PDB file the reader is currently at
        #table_index is the index where the data begins
        i = -1
        table_index = -1
        for line in lines:
            i += 1
            if ("pose" in line.lower()) and ("table" in line.lower()):
                table_index = i
                break
    if (table_index != -1):
        labelList = lines[table_index+1].split() #string of space separated labels to list of labels
        print(lines[table_index+2])
        print(lines[table_index+3])
        print(lines[table_index+4])
        weightsList = lines[table_index+3].split() #string of space separated weights to list of weights
        f.close()
        return labelList, weightsList

    else:
        f.close()
        print("Did not find where the table information is located in the document")

def pdbFileName(filePath):
    #find index of last "/"
    start = filePath.rfind("/") + 1
    #find index of last "."
    end = filePath.rfind(".")
    return filePath[start:end]

def formRow(filePath):
    pdb_name = pdbFileName(filePath)
    row = "<tr><td>"+pdb_name+"</td>"

    labelList, weightsList = getLabelsAndWeights(filePath)
    for j in weightsList[1:]: #add the weights to the row for that protein
        row += "<td>" + j + "</td>"

    row += "</tr>"
    return row

def getFiles(rootFolder):
    dir_list = os.listdir(rootFolder)
    filePaths = [rootFolder + "/" + i for i in dir_list if not i.startswith(".") ] 
    return filePaths

def makeWeightTables(session, rootFolder):
    #initialize the two sections of the table
    filePaths = getFiles(rootFolder)

    print(filePaths)
    table_header = "<tr>\n" 
    table_rows = ""

    #retrieve the labelList and the weightslist for the table header 
    labelList, _ = getLabelsAndWeights(filePaths[0])

    for i in labelList: #append labels to the header
        table_header += "<th>" + i + "</th>"

    table_header += "</tr>" #close off the table_header

    for pdb_file in filePaths:
        row = formRow(pdb_file) #<tr><td>filename</td> ... <td>fa_intra_rep</td> ... <td>total</td></tr>
        table_rows += row

    table_string = "<table>" + table_header + table_rows + "</table>"

    log_command = "log html " + table_string 

    run(session, log_command) 

def register_command(logger):
    from chimerax.core.commands import register, CmdDesc, StringArg

    desc = CmdDesc(required = [('rootFolder', StringArg)], 
                   synopsis='takes root directory and shows scores')
    register('makeWeightTables', desc, makeWeightTables, logger=logger)

register_command(session.logger)

print("done")

