import os
import ConfigParser

class Learning:

    def __init__(self):
        pass

    def PrintFilePath(self,path):
        print(path)
        print(os.path.dirname(path))
        print(os.path.abspath(path))
        print(os.path.abspath(os.path.dirname(path)))
        print(os.path.dirname(os.path.abspath(path)))

    def ReadConfig(self,fileName,Section,properties):
        pConfig = ConfigParser.ConfigParser()
        output = {}
        pConfig.read(fileName)
        for key in properties:
            output[key] = pConfig.get(Section,key)
        return output


