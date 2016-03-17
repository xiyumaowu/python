#!/usr/bin/python3
# _*_ encoding: utf-8 _*_

import os


_R_path = "/home/ezhonju/python/testkget"  
_W_EX_Path = "/home/ezhonju/python/kget1.txt" 
_W_O_Path = "/home/ezhonju/python/kget2.txt"  

_Count_File = 0

def _Find_Str (_path) :
    _f = open(_path,"r")
    _All_Line = _f.readlines() 
    _f.close()
    _Count_Line = 0
    _Len_Line = len(_All_Line)

    _Ex_Str = ""

    print("--> ongoing...")

    while _Count_Line < _Len_Line :
        _Str = _All_Line[_Count_Line]
        if "EUtranCellTDD=" in _Str and "Proxy" in _All_Line[_Count_Line - 1] :
            _Ex_Str += _All_Line[_Count_Line - 2] + _All_Line[_Count_Line -1 ] + _Str + _All_Line[_Count_Line + 1]
 
            _Count_Line += 1   
            while _Count_Line < _Len_Line :
                if "=====" in _All_Line[_Count_Line  + 1] :
#                    _Ex_Str += _All_Line[_Count_Line + 1]

                    _Count_Line += 1
                    break
                else:
                    _Ex_Str +=_All_Line[_Count_Line + 1]
                    _Count_Line += 1
        else :
            _Count_Line += 1

    #filter celltdd
    if _Ex_Str != "" :

        #save verifying file
        _file = open(_W_EX_Path,"a")
        _file.write(_Ex_Str+"\n")
        _file.close()
        '''
        _O_file = open(_W_O_Path,"a")
        #save verified file
        for _Over_Str in _All_Line:
            _O_file.write(_Over_Str)  
        _O_file.close()
        '''
    #if this file inexist, then create a file

    else: 
#        _O_file = open(_W_O_Path,"a")
        _All_Str = open(_path,"r")

        #save verified file
#       _O_file.write(_All_Str.read())  
#       _O_file.close()        
        _All_Str.close()

def _Get_Files():
    global _Count_File
    if os.path.lexists(_R_path) == False:
        print("-->your file is not exist")
        exit(0)
    for _root,_dirs,_files in os.walk(_R_path):
            for _file in _files: 
                print("-->managing "+ os.path.join(_root, _file))
                try:
                    _Find_Str(os.path.join(_root,_file))
                except Exception:
                    print("\n-----------manage "+os.path.join(_root,_file)+"file Exception-----------") 
                    exit(0)
                print("-->"+os.path.join(_root,_file)+" manage done!")
                _Count_File += 1
                print("-->managed "+str(_Count_File)+" files now\n------------------------------")

_Get_Files()
print("managed done, and the counter is:"+str(_Count_File))
exit(0)
