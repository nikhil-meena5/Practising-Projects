#Task 4.1:
#File organizer (Day 1–2) Given a messy folder, move files into subfolders: Images, PDFs, Documents, Videos, Others.
#Skills: os, shutil, pathlib.
#How to check:
#Make a test folder with 20 mixed files (never a real folder!). Run it. 
#Every file lands in the right subfolder, nothing is lost.

import os 
import shutil
from pathlib import Path

#main folder 
folder = Path(__file__).resolve().parent / "Test-Input"

#create subfolder 
folders = {
    "Images":[".jpg", ".jpeg", ".png", ".gif"],
    "PDFs":[".pdf"],
    "Documents":[".doc", ".docx", ".txt", ".xlsx", ".csv"],
    "Videos":[".mp4", ".mkv", ".avi"],
    "Others":[]
    }

#create folders if they don't exist
for name in folders: 
    (folder/name).mkdir(parents = True,exist_ok=True)

#organize files
for file in folder.iterdir():

    if file.is_file():

        moved = False


        for folder_name,extensions in folders.items(): 


            if file.suffix.lower() in extensions:
                destination = folder / folder_name / file.name
                shutil.move(str(file),str(destination))
                moved = True
                print(file.name,"moved to",folder_name)
                break

        if not moved:
            destination = folder/ "Others" / file.name
            shutil.move(str(file),str(destination))
            print(file.name, "moved to Others")


print("\nAll files organized successfully!") 