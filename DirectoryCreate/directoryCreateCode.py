#################################
# List all non-standard packages to be imported by your 
# script here (only missing packages will be installed)
from ayx import Package
#Package.installPackages(['pandas','numpy'])


#################################
from ayx import Alteryx
import os
import pandas as pd


dfInput = Alteryx.read('#1')


# Check if the dataframe has the required fields
lstInputFields = list(dfInput.columns.values)
if not('RootFolder' in lstInputFields):
    raise ValueError('RootFolder column does not exist on input columns')
if not('FinalFolder' in lstInputFields):
    raise ValueError('FinalFolder column does not exist on input columns')    

# Create a flag for the new folder
dfInput['FolderCreated'] = False



#################################
for index,row in dfInput.iterrows():
    #get values from data frame
    folderRoot = row['RootFolder']
    finalFolder = row['FinalFolder']

    # validate if the root folder exists
    if not(os.path.isdir(folderRoot)):
        raise NotADirectoryError("Root folder " + folderRoot + " does not exist")

    # Create the sub-folder
    if os.path.isdir(finalFolder):
        #folder already exists
        dfInput.loc[index, 'FolderCreated'] = True
    else:
        try:
            os.makedirs(finalFolder)
        except:
            raise NotADirectoryError("Subfolder " + finalFolder + " cannot be created")
            dfInput.loc[index, 'FolderCreated'] = False
        else:
            dfInput.loc[index, 'FolderCreated'] = True


            


#################################
Alteryx.write(dfInput,1)