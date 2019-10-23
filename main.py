from learning_test import Learning



if __name__ == '__main__':
    learn = Learning()
    
    #learn.PrintFilePath(__file__)
    
    animal=learn.ReadConfig("Config/testconfigparser.cfg","Animal",["animal","age","color","born"])
    print(animal)

    
        