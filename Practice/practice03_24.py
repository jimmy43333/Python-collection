# class ats_data:
#     def __init__(self):
#         self.data = "None"
#         self.counting = 0
#         self.total_data_size = 0

#     def __call__(self):
#         print("ats_data __call__")
#         self.counting += 1

#     def judge_error(self, data):
#         print("ats_data judge_error")
#         self.total_data_size += len(data)

#     @classmethod
#     def generate(cls):
#         print("ats_data generate")
#         # raise NotImplementedError

#     @staticmethod
#     def throughtput(data_len, duration):
#         print(float(data_len/duration))

# A = ats_data()

class GenericInput(object):
    def read(self):
        raise NotImplementedError
    @classmethod
    def generate(cls, config):
        raise NotImplementedError

class PathInput(GenericInput):
    def __init__(self, path):
        super().__init__()
        self.path = path
    
    def read(self):
        return self.path

    @classmethod
    def generate(cls, config):
        for name in config:
            yield cls(name)

class OwnInput(GenericInput):
    def __init__(self):
        super().__init__()
        self.result = "HAHAHA"
    
    def read(self):
        return self.result
    
    @classmethod
    def generate(cls, config):
        yield cls()

class GenericWorker(object):
    def __init__(self, input_data):
        self.input_data = input_data
        self.result = None

    def handle(self):
        raise NotImplementedError
    
    @classmethod
    def create_worker(cls, input_class, config):
        worker = []
        for data in input_class.generate(config):
            worker.append(cls(data))
        return worker

class LineWork(GenericWorker):
    def __init__(self, input_data):
        super().__init__(input_data)
    
    def handle(self):
        self.result = "Line: "
        self.result += self.input_data.read()
        print(self.result)

class FacebookWork(GenericWorker):
    def __init__(self, input_data):
        super().__init__(input_data)
    
    def handle(self):
        self.result = "FaceBook: "
        self.result += self.input_data.read()
        print(self.result)

def connect(input_class, worker_class, config):
    r = worker_class.create_worker(input_class, config)
    for ele in r:
        ele.handle()

connect(PathInput, LineWork, "ABC")
connect(OwnInput, LineWork, "ABC")
connect(PathInput, FacebookWork, "ABC")
connect(OwnInput, FacebookWork, "ABC")
