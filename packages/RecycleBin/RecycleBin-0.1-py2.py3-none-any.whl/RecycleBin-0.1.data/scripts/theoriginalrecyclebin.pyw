import pyhk
import pythoncom
import subprocess

 
def recycle():
    subprocess.Popen('explorer "C:\$Recycle.Bin\S-1-5-21-1189420014-1910659693-944285204-1002"')



#create pyhk class instance
hot = pyhk.pyhk()

 
#add hotkey
hot.addHotkey(['Ctrl', 'Alt','R'],recycle)
 
#start looking for hotkey.
hot.start()
