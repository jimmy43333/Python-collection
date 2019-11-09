#from learning_test import Learning
import logging
from TGlog import setuplog

if __name__ == '__main__':
    setuplog("./Log/infoLog.log",'a',logging.INFO)
    setuplog("./Log/errorLog.log",'w',logging.ERROR)
    
    logging.debug("Debug from main")
    logging.info("Info from main")
    logging.warning("Warning from main")
    logging.error("Error from main")
    logging.critical("Critical from main")

    logger1 = logging.getLogger("Testing01")
    logger2 = logging.getLogger("Testing02")
    logger1.info("Info by Testing01")
    logger2.info("Info by Testing02")
    
    handler = logging.FileHandler("./Log/TestLog.log")
    formatter = logging.Formatter('%(asctime)s %(name)-12s %(levelname)-8s %(message)s')
    handler.setLevel(logging.WARNING)
    handler.setFormatter(formatter)
    logger1.addHandler(handler)
    logger1.warning("Warning by Testing01")
    
    #learn = Learning()
    #learn.PrintFilePath(__file__)
    
    '''
    animal=learn.ReadConfig("Config/testconfigparser.cfg","Animal",["animal","age","color","born"])
    print(animal)
    '''
    '''
    learn.BasicOperatorExample(10,3.0,"/")
    learn.BasicOperatorExample(10,3,"//")
    learn.BasicOperatorExample(10,3.0,"//")
    learn.BasicOperatorExample(10,3.0,"**")
    learn.BasicOperatorExample(10,3.0,"&")
    '''
    #learn.PrintSystem()
    #for item in []:
    #    print str(item) + "no exits"
        
