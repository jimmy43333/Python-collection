import os
import ConfigParser
import platform

class Learning:

    def __init__(self):
        self.numberInt = 10
        self.numberFloat = 33.33
        self.numberLong = 999999
    
    ### Basic Type ##########################################################
    def BasicOperatorExample(self,a,b,ope):
        # Basic Data Type
        # Numeric type : int, long, float, bool, complex
        # String type
        # Container type : list, set, dict, tuple
        if ope == "/":
            self.numberInt = a / b
        elif ope == "//":
            self.numberInt = a // b
        elif ope == "**":
            self.numberInt = a ** b
        else :
            print("Not valid value ! ")
            return

        printstr = str(a) + ope + str(b) + " = " + str(self.numberInt)
        print(printstr)
        print(type(self.numberInt))
        print("repr:",repr(self.numberInt))
    
    ### find file path #########################################################    
    def PrintFilePath(self,path):
        print(path)
        print(os.path.dirname(path))
        print(os.path.abspath(path))
        print(os.path.abspath(os.path.dirname(path)))
        print(os.path.dirname(os.path.abspath(path)))

    ### read the config ######################################################## 
    def ReadConfigDict(self,fileName,Section,properties):
        pConfig = ConfigParser.ConfigParser()
        output = {}
        pConfig.read(fileName)
        for key in properties:
            output[key] = pConfig.get(Section,key)
        return output

    ### print computer information #############################################
    def PrintSystem(self):
        print(platform.uname())
        print(platform.system())

    


